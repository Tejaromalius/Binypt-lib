from binypt import ProgressBar


def test_active_progress_bar():
    iterations = 10
    pb = ProgressBar(iterations, True)
    for _ in range(iterations):
        assert pb.next(), "ProgressBar failed to run next()"
    assert pb.goto(), "ProgressBar failed to run goto()"
    assert pb.finish(), "ProgressBar failed to run finish()"
    del pb


def test_disabled_progress_bar():
    pb = ProgressBar()
    assert pb.next() is None, "ProgressBar failed to run next()"
    assert pb.goto() is None, "ProgressBar failed to run goto()"
    assert pb.finish() is None, "ProgressBar failed to run finish()"
    del pb
