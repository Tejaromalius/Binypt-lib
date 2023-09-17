import os
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


def test_functionality(binypt_instance):
    assert (
        isinstance(binypt_instance, Binypt),
        "Object could not be initialized",
    )


def test_exporting(binypt_instance):
    output_path = "test_file.csv"
    binypt_instance.export(output_path)
    assert (
        os.path.exists(output_path)
        and os.path.getsize(output_path) != 0,
        "Test file could not be written",
    )
    os.remove(output_path)
