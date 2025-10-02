from .assertions import Assertions
from .crypto import Crypto
from .files import Files
from .google_sheets import GoogleSheets
from .reports import Reports


class UtilitiesManager(Assertions, Crypto, Files, Reports):
    def __init__(self):
        Assertions.__init__(self)
        Reports.__init__(self)
        self._google_sheets = None

    @property
    def google_sheets(self):
        if self._google_sheets is None:
            self._google_sheets = GoogleSheets()
        return self._google_sheets


__all__ = [
    "Assertions",
    "Crypto",
    "Files",
    "GoogleSheets",
    "Reports",
    "UtilitiesManager",
]
