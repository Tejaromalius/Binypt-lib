from progress.bar import Bar


class ProgressBar:
    def __init__(self, total_timelines: int = 10, is_active: bool = False):
        self.is_active = is_active
        if is_active:
            self.bar = Bar(
                "Downloaded: ",
                max=total_timelines,
                suffix=" retrieved %(index)d/%(max)d",
            )

    def next(self, jump: int = 1):
        if self.is_active:
            self.bar.next(jump)
            return True

    def goto(self, index: int = 0):
        if self.is_active:
            self.bar.goto(index)
            return True

    def finish(self):
        if self.is_active:
            self.bar.finish()
            return True
