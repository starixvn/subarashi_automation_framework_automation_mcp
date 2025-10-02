from playwright.sync_api import APIRequestContext
from .assertions import Assertions
from .client import Client
from .extractor import Extractor


class APIManager(Client, Assertions, Extractor):
    def __init__(self, api_context: APIRequestContext):
        Client.__init__(self, api_context)


__all__ = [
    "Assertions",
    "Client",
    "Extractor",
    "APIManager",
]
