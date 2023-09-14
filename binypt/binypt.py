# Copyright (c) 2023 ilia tayefi
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import json
import time
import numpy as np
import pandas as pd
import datetime
import requests

from loguru import logger
from typing import TextIO
from .progress_bar import ProgressBar
from concurrent.futures import ThreadPoolExecutor


def formatDateTimestamp(date: str, date_format: str):
    stripped_time = datetime.datetime.strptime(date, date_format).timestamp()
    return int(stripped_time)


class Binypt:
    """
    Binypt is a Python library for fetching cryptocurrency price data from Binance.

    Attributes:
        trading_pair (str): Cryptocurrency pair (e.g., "BTCUSDT").
        interval (str): Time interval (e.g., "1h" for 1-hour).
        starting_date (str): Start date (format: "dd/mm/yyyy-HH:MM:SS").
        ending_date (str): End date (format: "dd/mm/yyyy-HH:MM:SS").
        verbosity (list): List of expected verbosity methods.
            Possible values: [logging, bar]. Default: []

    Methods: export(): Save data as CSV, Excel, or Pickle.
    """

    MILISECONDS = 1000
    DATE_FORMAT = "%d/%m/%Y-%H:%M:%S"
    METADATA_PATH = os.path.join(os.path.dirname(__file__), "metadata.json")

    def __init__(
        self,
        trading_pair: str,
        interval: str,
        starting_date: str,
        ending_date: str,
        verbosity: list = [],
    ):
        self.trading_pair = trading_pair
        self.interval = interval
        self.starting_date = (
            formatDateTimestamp(starting_date, Binypt.DATE_FORMAT) * Binypt.MILISECONDS
        )
        self.ending_date = (
            formatDateTimestamp(ending_date, Binypt.DATE_FORMAT) * Binypt.MILISECONDS
        )
        self.verbosity = verbosity

        if "logging" not in self.verbosity:
            logger.disable(__name__)

        self.metadata = self._importMetadata()
        self.data = pd.DataFrame(
            columns=self.metadata.get("chart_default_columns"), dtype=float
        )
        self.batched_timelines = list()
        self.total_timelines = 0
        self._update()
        logger.info("data is downloaded and set")

    def export(
        self, output_path: TextIO, output_extension: str in ["csv", "excel", "pickle"]
    ):
        """
            Export downloaded data to a file.

            Arguments:
                output_path (str): path to a non-existing file (e.g., "my-file.csv").
                output_extension (str): output file's type.
                    possible values: 'csv', 'excel', 'pickle'.
        """
        if output_extension == "csv":
            self.data.to_csv(output_path)
        elif output_extension == "excel":
            self.data.to_excel(output_path)
        elif output_extension == "pickle":
            self.data.to_pickle(output_path)
        logger.debug(f"data is written to `{output_path}`")

    def _importMetadata(self):
        with open(Binypt.METADATA_PATH, "r") as metadata_file:
            return json.load(metadata_file)
        logger.debug("metadata is imported from local")

    def _update(self):
        logger.debug("updating data")
        self._interpolateTimelines()
        self._downloadData()
        self._optimizeData()
        self._addHRTime()

    def _interpolateTimelines(self):
        jump = eval(self.metadata.get("intervals").get(self.interval))
        last_timeline = self.starting_date - jump

        batch = list()

        while last_timeline + jump < self.ending_date:
            if len(batch) == 1000:
                self.batched_timelines.append(batch)
                batch = list()

            batch.append([(last_timeline + jump), (last_timeline + jump * 2)])

            self.total_timelines += 1
            last_timeline += jump + 1

        if len(batch) != 0:
            self.batched_timelines.append(batch)
        logger.debug(f"timelines are batched to {self.total_timelines} parts")

    def _downloadData(self):
        api_url = (
            "https://api.binance.com/api/v3/klines?symbol="
            + f"{self.trading_pair}&interval={self.interval}&limit=1000&"
            + "startTime={}&endTime={}"
        )
        bar = ProgressBar(
            self.total_timelines, True if "bar" in self.verbosity else False
        )

        def retreiveBatchedData(batch, batch_ix):
            logger.debug("downloading batched timelines")
            while True:
                bar.goto(batch_ix * 1000)
                thread_pool = ThreadPoolExecutor()

                try:
                    urls = list(
                        api_url.format(timeline[0], timeline[1]) for timeline in batch
                    )
                    api_requests = list(
                        thread_pool.submit(lambda url: requests.get(url).json(), (url))
                        for url in urls
                    )

                    for request in api_requests:
                        bar.next()
                        while request._state == "RUNNING":
                            time.sleep(0.25)

                    return list(
                        request.result()
                        for request in api_requests
                        if len(request.result()) != 0
                    )

                except Exception:
                    continue

        for batch_ix, batch in enumerate(self.batched_timelines):
            binance_data = np.array(
                [
                    data
                    for batched_data in retreiveBatchedData(batch, batch_ix)
                    for data in batched_data
                ]
            )
            binance_data_df = pd.DataFrame(
                binance_data,
                columns=self.metadata.get("chart_default_columns"),
            ).astype(float)
            self.data = pd.concat([self.data, binance_data_df], ignore_index=True)
        bar.finish()
        logger.debug("batched timelines are downloaded")

    def _optimizeData(self):
        end_point = 0

        for index in range(1, len(self.data)):
            if self.data.iloc[-index]["close_time"] < self.ending_date:
                end_point = len(self.data) - index
                break

        self.data = self.data.iloc[: end_point + 1]
        logger.debug("data is cleared and optimized")

    def _addHRTime(self):
        self.data["open_time_str"] = [
            datetime.datetime.fromtimestamp(time_record / Binypt.MILISECONDS)
            for time_record in self.data["open_time"]
        ]
        self.data["close_time_str"] = [
            datetime.datetime.fromtimestamp(time_record / Binypt.MILISECONDS)
            for time_record in self.data["close_time"]
        ]
        logger.debug("human readible timestamp is added to data")
