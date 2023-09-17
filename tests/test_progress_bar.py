import pytest

from binypt.progress_bar_wrapper import ProgressBarWrapper


@pytest.fixture
def bar_size():
    yield 10


def test_active_progress_bar(bar_size):
    bar = ProgressBarWrapper(True)
    bar.start(bar_size)
    for _ in range(bar_size):
        bar.next() is None, "ProgressBar failed to run next()"
    bar.goto(0) is None, "ProgressBar failed to run goto()"
    bar.finish() is None, "ProgressBar failed to run finish()"
    del bar


def test_disabled_progress_bar(bar_size):
    bar = ProgressBarWrapper(False)
    bar.start(bar_size)
    bar.next() is None, "ProgressBar failed to run next()"
    bar.goto(0) is None, "ProgressBar failed to run goto()"
    bar.finish() is None, "ProgressBar failed to run finish()"
    del bar
