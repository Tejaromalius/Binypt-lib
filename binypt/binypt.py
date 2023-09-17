import os
import re
import pandas as pd
import datetime

from . import logger
from .retriever import Retriever
from .metadata.client import Client as MetadataClient
from .progress_bar_wrapper import ProgressBarWrapper


class Decorators:
    def run_if_arguments_set(method):
        def wrapper(self, *args, **kwargs):
            assert self.trading_pair is not None \
                and self.interval is not None \
                and self.open_time is not None \
                and self.close_time is not None, \
                "Set arguments first before fetching!"

            return method(self, *args, **kwargs)

        return wrapper

    def run_if_data_retrieved(method):
        def wrapper(self, *args, **kwargs):
            assert len(self.data) != 0, "No data set to operate on!"
            return method(self, *args, **kwargs)

        return wrapper

    def run_if_arguments_valid(method):
        def wrapper(
            self,
            trading_pair: str,
            interval: str,
            open_date: str,
            close_date: str,
        ):
            tp_exists = self.metadata.check_trading_pair_exists(trading_pair)
            assert tp_exists is True, \
                "Trading pair is not found in the metadata!"

            assert self.metadata.get_interval(interval) is not None, \
                "Interval is invalid!"

            assert self.metadata.get_date_timestamp(open_date) is not None, \
                "Start date is of wrong format!"

            assert self.metadata.get_date_timestamp(close_date) is not None, \
                "Start date is of wrong format!"

            return method(self, trading_pair, interval, open_date, close_date)

        return wrapper


class Binypt:
    """
    Binypt is a library for fetching cryptocurrency price data from Binance.

    Methods:
    __init__(): Initialize Binypt object.
    set_arguments(): Set trading pair, interval, open date, and close date.
    retrieve_data(): Fetch cryptocurrency price data from Binance API.
    export(): Export downloaded data to a file.
    add_human_readable_time(): Add human-readable timestamps to the data.
    set_verbosity(): Set verbosity options.
    """

    def __init__(self):
        self.metadata = MetadataClient()
        self.retriever = Retriever(self)
        self.bar = ProgressBarWrapper()

        self.batched_timelines = list()
        self.data = pd.DataFrame(
            columns=self.metadata.get_chart_columns(),
            dtype=float,
        )

    @Decorators.run_if_arguments_valid
    def set_arguments(
        self,
        trading_pair: str,
        interval: str,
        open_date: str,
        close_date: str,
    ):
        """
        Set trading pair, interval, open date, and close date.

        Arguments:
            trading_pair (str): Cryptocurrency pair (e.g., "BTCUSDT").
            interval (str): Time interval (e.g., "1h" for 1-hour).
            open_date (str): Start date (format: "dd/mm/yyyy-HH:MM:SS").
            close_date (str): End date (format: "dd/mm/yyyy-HH:MM:SS").
        """

        self.interval = interval
        self.trading_pair = trading_pair
        self.open_time = self.metadata.get_date_timestamp(open_date)
        self.close_time = self.metadata.get_date_timestamp(close_date)
        logger.info("API arguments are set")

    @Decorators.run_if_arguments_set
    def retrieve_data(self):
        """ Fetch cryptocurrency price data from Binance API. """
        logger.debug("Fetching new data from Binance API")
        self.retriever.run()
        logger.info("Data is downloaded and set")

    @Decorators.run_if_data_retrieved
    def get_data(self):
        return self.data

    @Decorators.run_if_data_retrieved
    def export(self, output_path: str):
        """
        Export downloaded data to a file.

        Arguments:
            output_path (str): absolute path to a non-existing file.
                possible file extensions: '.csv', '.excel', '.pickle'.
        """
        output_path = os.path.expanduser(output_path)
        logger.debug(f"Output file specified as: {output_path}")
        file_format = re.search("(csv)|(excel)|(pickle)$", output_path).group()

        if file_format == "csv":
            self.data.to_csv(output_path)
            logger.debug(f"Data is written to `{output_path}`")

        elif file_format == "excel":
            self.data.to_excel(output_path)
            logger.debug(f"Data is written to `{output_path}`")

        elif file_format == "pickle":
            self.data.to_pickle(output_path)
            logger.debug(f"Data is written to `{output_path}`")

        else:
            assert "Output path does not specify a file format!"

    @Decorators.run_if_data_retrieved
    def add_human_readable_time(self):
        """ Add human-readable timestamps to the data. """
        miliseconds = 1000
        self.data["open_date"] = [
            datetime.datetime.fromtimestamp(open_time / miliseconds)
            for open_time in self.data["open_time"]
        ]
        self.data["close_date"] = [
            datetime.datetime.fromtimestamp(close_time / miliseconds)
            for close_time in self.data["close_time"]
        ]
        logger.debug("Human-readable timestamp is added to data")

    def set_verbosity(self, show_bar: bool = False, show_log: bool = False):
        """
        Set verbosity options.

        Arguments:
            show_bar (bool, optional): Whether to show a progress bar.
                Default is False.
            show_log (bool, optional): Whether to show log messages.
                Default is False.
        """
        self.bar.change_status(True if show_bar else False)
        if show_log:
            logger.enable("binypt")
