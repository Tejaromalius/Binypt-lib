import os
import time
import numpy as np
import pandas as pd
import requests

from loguru import logger
from concurrent.futures import ThreadPoolExecutor


class Retriever:
    CACHE_PATH = ".data_cache.pkl"
    """
    Retriever is a class responsible for fetching data from Binance API.

    Methods:
        run(): Run the data retrieval process, including:
            interpolation, data download, and data trimming.
    """
    def __init__(self, binypt):
        self.binypt = binypt

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
        jump = self.binypt.metadata.get_interval(self.binypt.interval)
        last_timeline = self.binypt.open_time - jump

        batch = list()

        while last_timeline + jump < self.binypt.close_time:
            if len(batch) == 1000:
                self.binypt.batched_timelines.append(batch)
                batch = list()

            batch.append([(last_timeline + jump), (last_timeline + jump * 2)])
            last_timeline += jump + 1

        if len(batch) != 0:
            self.binypt.batched_timelines.append(batch)

        logger.debug(
            "Interpolation completed."
            f"{len(self.binypt.batched_timelines)} batches created."
        )

    def _download_data(self):
        bar_size = self.__size_batched_timelines(self.binypt.batched_timelines)
        logger.debug(f"Timelines are batched to {bar_size} parts")
        self.binypt.bar.start(bar_size)
        logger.debug("Downloading batched timelines...")

        for batch_ix, batch in enumerate(self.binypt.batched_timelines):
            urls = self.__get_formatted_links(batch)
            downloaded_data_batch = self.__download_batched_data(
                batch,
                batch_ix,
                urls,
            )
            optimized_data_batch = self.__optimize_data(downloaded_data_batch)
            self.binypt.data = pd.concat(
                [self.binypt.data, optimized_data_batch],
                ignore_index=True
            )
            self.__cache()
        self.__clear_cache()

        self.binypt.bar.finish()
        logger.debug("Batched timelines are downloaded.")

    def _trim_data(self):
        end_point = 0

        for ix in range(1, len(self.binypt.data)):
            last_close_time = self.binypt.data.iloc[-ix]["close_time"]
            if last_close_time < self.binypt.close_time:
                end_point = len(self.binypt.data) - ix
                break

        self.binypt.data = self.binypt.data.iloc[: end_point + 1]
        logger.debug("Data is cleared and optimized.")

    def __size_batched_timelines(self, array: list, stop: bool = False):
        sum = 0
        for li in array:
            if isinstance(li, list) and not stop:
                sum += self.__size_batched_timelines(li, True)
            else:
                sum += 1
        return sum

    def __get_formatted_links(self, batch):
        api_url = (
            "https://api.binance.com/api/v3/klines?symbol="
            + f"{self.binypt.trading_pair}&"
            + f"interval={self.binypt.interval}&limit=1000&"
            + "startTime={}&endTime={}"
        )

        return [api_url.format(timeline[0], timeline[1]) for timeline in batch]

    def __download_batched_data(self, batch, batch_ix, urls):
        while True:
            self.binypt.bar.goto(batch_ix * 1000)
            thread_pool = ThreadPoolExecutor()

            try:
                api_requests = list(
                    thread_pool.submit(
                        lambda url: requests.get(url).json(), (url)
                    )
                    for url in urls
                )
                for request in api_requests:
                    self.binypt.bar.next()
                    while request._state == "RUNNING":
                        time.sleep(0.25)

                return list(
                    request.result()
                    for request in api_requests
                    if len(request.result()) != 0
                )

            except Exception:
                logger.error(
                    f"Error while downloading batch {batch_ix}: {str(e)}"
                )
                continue

    def __optimize_data(self, downloaded_data_batch):
        data_array = np.concatenate(downloaded_data_batch)
        retrieved_data = pd.DataFrame(
            data_array,
            columns=self.binypt.metadata.get_chart_columns(),
        ).astype(float)

        return retrieved_data

    def __cache(self):
        self.binypt.data.to_pickle(self.CACHE_PATH)

    def __clear_cache(self):
        os.remove(self.CACHE_PATH)
