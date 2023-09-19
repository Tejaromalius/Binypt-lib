import datetime

from .. import logger
from ._metadata import metadata


def get_date_timestamp(date):
    """
    Convert a date string to a timestamp in milliseconds.

    Arguments:
        date: The date string in the specified format.
    """
    date_format = metadata.get("date_format")
    timestamp_ms = int(
        datetime.datetime.strptime(
            date,
            date_format
        ).timestamp()
    ) * 1000  # milliseconds
    logger.debug(f"Converted date {date} to: {timestamp_ms} ms")
    return timestamp_ms


def get_interval_jump(interval: str):
    """
    Get the interval jump duration in milliseconds.

    Arguments:
        interval: The interval string (e.g., "1h" for 1-hour).
    """
    jump_ms = eval(metadata.get("intervals").get(interval))
    logger.debug(
        f"Converted interval {interval} "
        f"to milliseconds: {jump_ms}"
    )
    return jump_ms


def get_chart_columns():
    """ Get the column names for cryptocurrency price chart data. """
    chart_columns = metadata.get("chart_columns")
    logger.debug(f"Retrieved chart columns: {chart_columns}")
    return chart_columns
