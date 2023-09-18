import pytest
import tempfile

from binypt import Binypt

pytest.mark.filterwarnings("ignore::pytest.PytestAssertRewriteWarning")
binypt_instance = None


@pytest.fixture
def binypt():
    global binypt_instance
    if binypt_instance is None:
        binypt_instance = Binypt()
    return binypt_instance


def test_setting_argument(binypt):
    arguments = {
        "trading_pair": "BTCUSDT",
        "interval": "3d",
        "open_date": "01/01/2023-00:00:00",
        "close_date": "01/03/2023-00:00:00",
    }
    binypt.set_arguments(**arguments)


def test_logging(binypt):
    binypt.set_verbosity(show_log=True)


def test_retrieving_data(binypt):
    binypt.retrieve_data()


def test_adding_human_readable_date(binypt):
    binypt.add_human_readable_time()


def test_exporting(binypt):
    with tempfile.NamedTemporaryFile() as tmp:
        binypt.export(tmp.name)
