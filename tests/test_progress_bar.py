from binypt.progress_bar_wrapper import ProgressBarWrapper


def test_active_progress_bar(bar_size: int = 10):
    bar = ProgressBarWrapper()
    bar.change_status(True)
    bar.start(
        message="Downloaded: ",
        suffix=" retrieved %(index)d/%(max)d",
        max=bar_size,
    )
    for _ in range(bar_size):
        bar.next()
    bar.goto(0)
    bar.finish()
