import os
import json
import datetime

from loguru import logger

METADATA_PATH = os.path.join(os.path.dirname(__file__), "metadata.json")


class Client:
    """
    Client is responsible for managing cryptocurrency metadata
        and providing utility methods.

    Methods:
        get_trading_pair(): Get the full name of a trading pair.
        get_interval(): Get the interval duration in milliseconds.
        get_chart_columns(): Get the column names for price chart data.
        get_date_timestamp(): Convert a date to a timestamp in milliseconds.
    """
    def __init__(self):
        self.metadata = None
        self._loadMetadata()

    def get_trading_pair(self, trading_pair: str):
        """
        Get the full name of a trading pair.

        Arguments:
            trading_pair (str): The abbreviated trading pair (e.g., "BTCUSDT").
        """
        logger.debug(f"Getting full name for trading pair: {trading_pair}")
        return self.metadata.get(trading_pair, None)

    def get_interval(self, interval):
        """
        Get the interval duration in milliseconds for a given interval string.

        Arguments:
            interval: The interval string (e.g., "1h" for 1-hour).
        """
        intervals = self.metadata.get("intervals", {})
        interval = intervals.get(interval, False)
        if interval:
            interval_ms = eval(interval)
            logger.debug(
                f"Converted interval {interval}"
                f"to milliseconds: {interval_ms}"
            )
            return interval_ms
        else:
            logger.warning(f"Interval {interval} not found in metadata.")
            return None

    def get_chart_columns(self):
        """ Get the column names for cryptocurrency price chart data. """
        chart_columns = self.metadata.get("chart_columns", None)
        if chart_columns:
            logger.debug(f"Retrieved chart columns: {chart_columns}")
        else:
            logger.warning("Chart columns not found in metadata.")
        return chart_columns

    def get_date_timestamp(self, date):
        """
        Convert a date string to a timestamp in milliseconds.

        Arguments:
            date: The date string in the specified format.
        """
        date_format = self.metadata.get("date_format", None)
        try:
            timestamp_ms = int(
                datetime.datetime.strptime(date, date_format).timestamp()
            ) * 1000  # milliseconds
            logger.debug(
                f"Converted date {date} to timestamp:" f"{timestamp_ms} ms"
            )
            return timestamp_ms
        except ValueError:
            logger.error(f"Failed to convert date {date} to timestamp.")
            return None

    def _loadMetadata(self):
        try:
            with open(METADATA_PATH, "r") as file:
                self.metadata = json.load(file)
            logger.info("Metadata loaded successfully.")
        except Exception as e:
            logger.error(
                "Failed to load metadata"
                f"from {METADATA_PATH}: {str(e)}"
            )
