import pytest

from binypt import Binypt


pytest.mark.filterwarnings("ignore::pytest.PytestAssertRewriteWarning")


@pytest.fixture
def binypt_instance():
    binypt = Binypt()
    binypt.set_arguments(
        "BTCUSDT",
        "3d",
        "01/01/2023-00:00:00",
        "01/03/2023-00:00:00",
    )
    binypt.retrieve_data()
    yield binypt


def test_logging(binypt_instance):
    binypt_instance.set_verbosity(show_log=True)
    binypt_instance.retrieve_data()
