import inspect

from functools import wraps
from progress.bar import Bar


class ProgressBarWrapper(Bar):
    """
    ProgressBarWrapper is a wrapper class for the progress.bar.Bar.

    Attributes:
        is_active (bool): Indicates whether the progress bar is active.
            Default is False.
        message (str): Message to display on the progress bar.
        suffix (str): Suffix to display on the progress bar.

    Methods:
        change_status():
            Change the status of the progress bar (active or inactive).
        start(): Start the progress bar with a specified size.
    """
    def __init__(
        self,
        is_active: bool = False,
        message: str = "Downloaded: ",
        suffix: str = " retrieved %(index)d/%(max)d",
        *args,
        **kwargs,
    ):

        super().__init__(message=message, suffix=suffix, *args, **kwargs)
        self.is_active = is_active

        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if inspect.isfunction(attr):
                setattr(self, attr_name, self.__run_if_active(attr))

    def change_status(self, is_active: bool):
        """
        Change the status of the progress bar (active or inactive).

        Arguments:
            is_active (bool):
                Indicates whether the progress bar should be active.
        """
        self.is_active = is_active

    def start(self, bar_size):
        """
        Start the progress bar with a specified size.

        Arguments:
            bar_size: Size of the progress bar.
        """
        self.max = bar_size

    def __run_if_active(self, method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            if self.is_active:
                return method(self, *args, **kwargs)
            else:
                pass
        return wrapper
