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
    def __init__(self, is_active: bool = False):
        self.is_active = is_active
        self._update_masks()

    def change_status(self, is_active: bool):
        """
        Change the status of the progress bar (active or inactive).

        Arguments:
            is_active (bool):
                Indicates whether the progress bar should be active.
        """
        self.is_active = is_active
        self._update_masks()

    def start(self, *args, **kwargs):
        """
        Start the progress bar.

        Args:
            *args, **kwargs
        """
        super().__init__(*args, **kwargs)

    def _update_masks(self):
        valid_attr_names = [
            attr_name for attr_name in dir(self)
            if not attr_name.startswith("_")
            and attr_name in dir(Bar)
        ]

        for attr_name in valid_attr_names:
            try:
                attr = getattr(self, attr_name)
            except Exception:
                attr = getattr(Bar, attr_name)
            if inspect.ismethod(attr):
                setattr(self, attr_name, self._run_if_active(attr))

    def _run_if_active(self, method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            if self.is_active:
                return method(*args, **kwargs)
            else:
                pass
        return wrapper
