import os
import pytest

from binypt import Binypt


pytest.mark.filterwarnings("ignore::pytest.PytestAssertRewriteWarning")
binypt = None


@pytest.fixture
def binypt_instance():
    global binypt
    if binypt is None:
        binypt = Binypt()
    yield binypt


def test_functionality(binypt_instance):
    assert isinstance(binypt_instance, Binypt), \
        "Object could not be initialized."


def test_setting_argument(binypt_instance):
    arguments = {
        "trading_pair": "BTCUSDT",
        "interval": "3d",
        "open_date": "01/01/2023-00:00:00",
        "close_date": "01/03/2023-00:00:00",
    }
    binypt_instance.set_arguments(**arguments)


def test_logging(binypt_instance):
    binypt_instance.set_verbosity(show_log=True)


def test_retrieving_data(binypt_instance):
    binypt_instance.retrieve_data()


def test_adding_human_readable_date(binypt_instance):
    binypt_instance.add_human_readable_time()


def test_exporting(binypt_instance):
    output_path = "test_file.csv"
    binypt_instance.export(output_path)
    assert os.path.getsize(output_path) != 0, "Test file could not be written."
    os.remove(output_path)
