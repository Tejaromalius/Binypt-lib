import os
import time
import numpy as np
import pandas as pd
import requests

from . import logger
from . import metadata
from concurrent.futures import ThreadPoolExecutor
from .progress_bar_wrapper import ProgressBarWrapper


class Retriever:
    _CACHE_PATH = ".data_cache.pkl"
    """
    Retriever is a class responsible for fetching data from Binance API.

    Methods:
        run(): Run the data retrieval process, including:
            interpolation, data download, and data trimming.
    """
    def __init__(self, binypt):
        self.binypt = binypt
        self.bar = None

    def run(self):
        """
        Run the data retrieval process, including:
            interpolation, data download, and data trimming.
        """
        self._interpolate_timelines()
        self._download_data()
        self._trim_data()
        logger.info("Data retrieval process completed successfully.")

    def _interpolate_timelines(self):
        logger.debug("Interpolating timelines...")
        jump = metadata.get_interval_jump(self.binypt.interval)
        current_timeline = self.binypt.open_time - jump

        while current_timeline + jump < self.binypt.close_time:
            self.binypt.timelines.append(
                [
                    (current_timeline + jump),
                    (current_timeline + jump * 2),
                ],
            )
            current_timeline += jump + 1
        self.timelines_size = len(self.binypt.timelines)
        logger.debug(f"Timelines are batched to {self.timelines_size} parts")

    def _download_data(self):
        logger.debug("Downloading batched timelines...")
        self._set_up_bar()
        batch = list()

        for timeline_ix, timeline in enumerate(self.binypt.timelines):
            timelines_finished = (timeline_ix == self.timelines_size - 1)
            batch_reached_limit = (len(batch) == 1000)

            if not timelines_finished and not batch_reached_limit:
                batch.append(timeline)
                continue

            urls = self._get_formatted_links(batch)

            self._append_optimized_batch_to_data(
                self._optimize_batch(
                    self._download_batch(
                        timeline_ix,
                        urls,
                    )
                )
            )

            self._cache()
            batch.clear()

        self.bar.finish()
        self._clear_cache()
        logger.debug("Batched timelines are downloaded.")

    def _set_up_bar(self):
        self.bar = ProgressBarWrapper(self.binypt.bar_active)
        self.bar.start(
            message="Downloaded: ",
            suffix=" retrieved %(index)d/%(max)d",
            max=self.timelines_size,
        )

    def _get_formatted_links(self, batch):
        api_url = (
            "https://api.binance.com/api/v3/klines?symbol="
            + f"{self.binypt.trading_pair}&"
            + f"interval={self.binypt.interval}&limit=1000&"
            + "startTime={}&endTime={}"
        )

        return [api_url.format(timeline[0], timeline[1]) for timeline in batch]

    def _download_batch(self, timeline_ix, urls):
        self.bar.next()

        while True:
            thread_pool = ThreadPoolExecutor(max_workers=os.cpu_count())
            try:
                api_requests = list(
                    thread_pool.submit(
                        lambda url: requests.get(url).json(), (url)
                    )
                    for url in urls
                )

                for request in api_requests:
                    self.bar.next()
                    while request._state == "RUNNING":
                        time.sleep(0.1)

                return list(
                    request.result()
                    for request in api_requests
                    if len(request.result()) != 0
                )

            except Exception as error:
                thread_pool.shutdown(wait=False)
                logger.error(
                    f"Error while downloading batch #{timeline_ix}: "
                    f"{str(error)}",
                )
                self.bar.goto(
                    0 if timeline_ix <= 1000
                    else timeline_ix - 1000
                )
                time.sleep(3)
                continue

    def _optimize_batch(self, downloaded_batch):
        flattened_batch = np.concatenate(downloaded_batch)
        batch_dataframe = pd.DataFrame(
            flattened_batch,
            columns=metadata.get_chart_columns(),
        ).astype(float)

        return batch_dataframe

    def _append_optimized_batch_to_data(self, optimized_batch):
        self.binypt.data = pd.concat(
            [
                self.binypt.data,
                optimized_batch,
            ],
            ignore_index=True,
        )
        logger.debug(f"Data increased to {len(self.binypt.data)} records")

    def _trim_data(self):
        end_ix = 0
        data_len = len(self.binypt.data)
        for ix in range(1, data_len):
            last_close_time = self.binypt.data.iloc[-ix]["close_time"]
            if last_close_time < self.binypt.close_time:
                end_ix = data_len - ix
                break

        self.binypt.data = self.binypt.data.iloc[: end_ix + 1]
        logger.debug("Data is cleared and optimized.")

    def _cache(self):
        self.binypt.data.to_pickle(self._CACHE_PATH)

    def _clear_cache(self):
        os.remove(self._CACHE_PATH)
