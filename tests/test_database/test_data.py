"""Unit tests for src/Core/database/data.py"""

from unittest.mock import Mock

import pytest

from src.Core.exceptions import AutomationError
from src.Core.database.connection import Connection
from src.Core.database.query import Query
from src.Core.database.data import Data


class TestInsertRecord:
    """Test insert_record method."""

    def test_insert_record_success(self, db_connection: Mock, db_cursor: Mock) -> None:
        """Test successful insert record."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)
        data = Data(query)

        rows = data.insert_record(
            "users", {"name": "Test", "email": "test@example.com"}
        )

        assert isinstance(rows, int)

    def test_insert_record_empty_data(self) -> None:
        """Test insert_record raises error with empty data."""
        connection = Connection()
        query = Query(connection)
        data = Data(query)

        with pytest.raises(AutomationError, match="cannot be empty"):
            data.insert_record("users", {})


class TestInsertRecords:
    """Test insert_records method."""

    def test_insert_records_success(self, db_connection: Mock, db_cursor: Mock) -> None:
        """Test successful insert multiple records."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)
        data = Data(query)

        records = [
            {"name": "User1", "email": "user1@example.com"},
            {"name": "User2", "email": "user2@example.com"},
        ]

        rows = data.insert_records("users", records)

        assert isinstance(rows, int)


class TestUpdateRecord:
    """Test update_record method."""

    def test_update_record_success(self, db_connection: Mock, db_cursor: Mock) -> None:
        """Test successful update record."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)
        data = Data(query)

        rows = data.update_record("users", {"name": "Updated"}, "id = ?", (1,))

        assert isinstance(rows, int)


class TestDeleteRecords:
    """Test delete_records method."""

    def test_delete_records_success(self, db_connection: Mock, db_cursor: Mock) -> None:
        """Test successful delete records."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)
        data = Data(query)

        rows = data.delete_records("users", "id = ?", (1,))

        assert isinstance(rows, int)


class TestGetRecords:
    """Test get_records method."""

    def test_get_records_success(self, db_connection: Mock, db_cursor: Mock) -> None:
        """Test successful get records."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)
        data = Data(query)

        records = data.get_records("users")

        assert isinstance(records, list)

    def test_get_record_count_success(self, db_connection: Mock) -> None:
        """Test get record count."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_connection.cursor.return_value
        connection.is_connected = True
        # Mock with count column
        connection.cursor.description = [("count", None, None, None, None, None, None)]
        connection.cursor.fetchall.return_value = [(5,)]  # Tuple with count value

        query = Query(connection)
        data = Data(query)

        count = data.get_record_count("users")

        assert isinstance(count, int)
        assert count == 5


class TestTableOperations:
    """Test table operation methods."""

    def test_table_exists_true(self, db_connection: Mock) -> None:
        """Test table_exists returns True when exists."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_connection.cursor.return_value
        connection.is_connected = True
        # Mock with count column
        connection.cursor.description = [("count", None, None, None, None, None, None)]
        connection.cursor.fetchall.return_value = [(1,)]  # Tuple with count value

        query = Query(connection)
        data = Data(query)

        exists = data.table_exists("users")

        assert exists is True

    def test_get_table_columns_success(self, db_connection: Mock) -> None:
        """Test get table columns."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_connection.cursor.return_value
        connection.is_connected = True
        # Mock with COLUMN_NAME column
        connection.cursor.description = [
            ("COLUMN_NAME", None, None, None, None, None, None)
        ]
        connection.cursor.fetchall.return_value = [
            ("id",),
            ("name",),
            ("email",),
        ]

        query = Query(connection)
        data = Data(query)

        columns = data.get_table_columns("users")

        assert isinstance(columns, list)
        assert columns == ["id", "name", "email"]


class TestBulkOperations:
    """Test bulk operation methods."""

    def test_bulk_insert_success(self, db_connection: Mock, db_cursor: Mock) -> None:
        """Test bulk insert."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)
        data = Data(query)

        records = [{"name": f"User{i}"} for i in range(10)]

        rows = data.bulk_insert("users", records)

        assert isinstance(rows, int)

    def test_insert_data_to_table_success(
        self, db_connection: Mock, db_cursor: Mock
    ) -> None:
        """Test insert_data_to_table method."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)
        data = Data(query)

        params = {"name": "Test User", "email": "test@example.com"}
        data.insert_data_to_table("users", params)

        db_cursor.execute.assert_called()


class TestTableManagement:
    """Test table management methods."""

    def test_truncate_table_success(self, db_connection: Mock, db_cursor: Mock) -> None:
        """Test truncate table."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)
        data = Data(query)

        data.truncate_table("users")

        db_cursor.execute.assert_called_once()

    def test_backup_table_success(self, db_connection: Mock, db_cursor: Mock) -> None:
        """Test backup table."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)
        data = Data(query)

        data.backup_table("users", "users_backup")

        db_cursor.execute.assert_called_once()
