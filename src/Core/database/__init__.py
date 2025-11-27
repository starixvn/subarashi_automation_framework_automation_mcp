from .connection import Connection
from .data import Data
from .query import Query


class DatabaseManager(Connection, Query, Data):  # type: ignore[misc]
    def __init__(
        self,
        server_name: str = "",
        database_name: str = "",
        username: str = "",
        password: str = "",
        driver: str = "SQL Server",
        trusted_connection: bool = True,
    ):
        Connection.__init__(self)
        Query.__init__(self, self)
        Data.__init__(self, self)
        if server_name and database_name:
            self.connect(
                server_name,
                database_name,
                username,
                password,
                driver,
                trusted_connection,
            )


__all__ = [
    "Connection",
    "Data",
    "Query",
    "DatabaseManager",
]
