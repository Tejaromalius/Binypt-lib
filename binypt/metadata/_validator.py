import datetime

from .. import logger
from ._metadata import metadata


def trading_pair_exists(trading_pair: str):
    """
    Check if given trading pair exists in metadata.

    Arguments:
        trading_pair (str): The abbreviated trading pair (e.g., "BTCUSDT").
    """
    trading_pairs = metadata.get("trading_pairs")
    if not trading_pairs.count(trading_pair):
        raise ValueError(f"`{trading_pair}` not found in metadata!")
    logger.debug(f"Trading pair `{trading_pair}` is valid.")
    return trading_pair


def interval_exists(interval: str):
    """
    Check if given interval exists in metadata.

    Arguments:
        interval (str): The interval abbreviation (e.g., "1h", "5m").
    """
    intervals = metadata.get("intervals")
    if not intervals.get(interval, False):
        raise ValueError(f"`{interval}` not found in metadata!")
    logger.debug(f"Interval `{interval}` is valid.")
    return interval


def date_is_correct_format(date: str):
    """
    Compare given date string to the valid format.

    Arguments:
        date: The date string to be checked.
    """
    date_format = metadata.get("date_format")
    datetime.datetime.strptime(date, date_format).timestamp()
    logger.debug(f"`{date}` is of valid format.")
    return date
