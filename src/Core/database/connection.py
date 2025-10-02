import pyodbc
from typing import Optional, Dict, Any
from src.Core import auto_log, retry, AutomationError


class Connection:
    def __init__(self):
        self.connection: Optional[pyodbc.Connection] = None
        self.cursor: Optional[pyodbc.Cursor] = None
        self.is_connected = False

    @auto_log
    @retry(max_attempts=3)
    def connect(
        self,
        server_name: str,
        database_name: str,
        username: str = "",
        password: str = "",
        driver: str = "SQL Server",
        trusted_connection: bool = True,
    ) -> None:
        try:
            connection_parts = [
                f"DRIVER={{{driver}}}",
                f"SERVER={server_name}",
                f"DATABASE={database_name}",
            ]
            if trusted_connection:
                connection_parts.append("Trusted_Connection=yes")
            else:
                connection_parts.append(f"UID={username}")
                connection_parts.append(f"PWD={password}")
            connection_string = ";".join(connection_parts)
            self.connection = pyodbc.connect(connection_string)
            self.connection.setencoding("utf-8")
            self.cursor = self.connection.cursor()
            self.is_connected = True
        except Exception as e:
            raise AutomationError(
                f"Failed to connect to database {database_name}", str(e)
            ) from e

    @auto_log
    def disconnect(self) -> None:
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            self.cursor = None
            self.connection = None
            self.is_connected = False
        except Exception as e:
            raise AutomationError("Failed to close database connection", str(e)) from e

    @auto_log
    def close(self) -> None:
        self.disconnect()

    @auto_log
    def begin_transaction(self) -> None:
        if not self.is_connected:
            raise AutomationError("Not connected to database")
        try:
            pass
        except Exception as e:
            raise AutomationError("Failed to begin transaction", str(e)) from e

    @auto_log
    def commit(self) -> None:
        if not self.is_connected:
            raise AutomationError("Not connected to database")
        try:
            self.connection.commit()
        except Exception as e:
            raise AutomationError("Failed to commit transaction", str(e)) from e

    @auto_log
    def rollback(self) -> None:
        if not self.is_connected:
            raise AutomationError("Not connected to database")
        try:
            self.connection.rollback()
        except Exception as e:
            raise AutomationError("Failed to rollback transaction", str(e)) from e

    @auto_log
    def get_connection_info(self) -> Dict[str, Any]:
        if not self.is_connected:
            return {"connected": False}
        try:
            return {
                "connected": True,
                "server": self.connection.getinfo(pyodbc.SQL_SERVER_NAME),
                "database": self.connection.getinfo(pyodbc.SQL_DATABASE_NAME),
                "driver": self.connection.getinfo(pyodbc.SQL_DRIVER_NAME),
            }
        except Exception as e:
            return {"connected": self.is_connected, "error": str(e)}

    @auto_log
    def test_connection(self) -> bool:
        try:
            if not self.is_connected:
                return False
            self.cursor.execute("SELECT 1")
            return True
        except Exception:
            return False

    @auto_log
    def get_server_version(self) -> str:
        if not self.is_connected:
            raise AutomationError("Not connected to database")
        try:
            self.cursor.execute("SELECT @@VERSION")
            result = self.cursor.fetchone()
            return result[0] if result else "Unknown"
        except Exception as e:
            raise AutomationError("Failed to get server version", str(e)) from e

    @auto_log
    def get_database_name(self) -> str:
        if not self.is_connected:
            raise AutomationError("Not connected to database")
        try:
            self.cursor.execute("SELECT DB_NAME()")
            result = self.cursor.fetchone()
            return result[0] if result else "Unknown"
        except Exception as e:
            raise AutomationError("Failed to get database name", str(e)) from e

    @auto_log
    def get_tables(self) -> list:
        if not self.is_connected:
            raise AutomationError("Not connected to database")
        try:
            self.cursor.execute(
                "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
            )
            results = self.cursor.fetchall()
            return [row[0] for row in results]
        except Exception as e:
            raise AutomationError("Failed to get table list", str(e)) from e

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
