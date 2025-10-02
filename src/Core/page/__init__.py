from playwright.sync_api import Page
from .actions import Actions
from .assertions import Assertions
from .browser import BrowserManager
from .waits import Waits


class PageManager(Actions, Assertions, BrowserManager, Waits):
    def __init__(self, page: Page):
        Actions.__init__(self, page)
        Assertions.__init__(self, page)
        BrowserManager.__init__(self, page)
        Waits.__init__(self, page)


__all__ = [
    "Actions",
    "Assertions",
    "BrowserManager",
    "Waits",
    "PageManager",
]
