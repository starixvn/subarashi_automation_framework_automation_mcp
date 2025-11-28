"""Unit tests for src/Core/database/query.py"""

from unittest.mock import Mock

import pytest

from src.Core.exceptions import AutomationError
from src.Core.database.connection import Connection
from src.Core.database.query import Query


class TestExecuteSelect:
    """Test execute_select method."""

    def test_execute_select_success(self, db_connection: Mock, db_cursor: Mock) -> None:
        """Test successful SELECT execution."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)

        results = query.execute_select("SELECT * FROM users")

        assert isinstance(results, list)
        assert len(results) == 2

    def test_execute_select_with_params(
        self, db_connection: Mock, db_cursor: Mock
    ) -> None:
        """Test SELECT with parameters."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)

        query.execute_select("SELECT * FROM users WHERE id = ?", (1,))

        db_cursor.execute.assert_called_once()

    def test_execute_select_not_connected(self) -> None:
        """Test execute_select raises error when not connected."""
        connection = Connection()
        connection.is_connected = False
        query = Query(connection)

        with pytest.raises(AutomationError, match="Not connected"):
            query.execute_select("SELECT 1")


class TestExecuteInsert:
    """Test execute_insert method."""

    def test_execute_insert_success(self, db_connection: Mock, db_cursor: Mock) -> None:
        """Test successful INSERT execution."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)

        rows = query.execute_insert(
            "INSERT INTO users VALUES (?, ?)", ("test", "test@example.com")
        )

        assert isinstance(rows, int)


class TestExecuteUpdate:
    """Test execute_update method."""

    def test_execute_update_success(self, db_connection: Mock, db_cursor: Mock) -> None:
        """Test successful UPDATE execution."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)

        rows = query.execute_update(
            "UPDATE users SET name = ? WHERE id = ?", ("New Name", 1)
        )

        assert isinstance(rows, int)


class TestExecuteDelete:
    """Test execute_delete method."""

    def test_execute_delete_success(self, db_connection: Mock, db_cursor: Mock) -> None:
        """Test successful DELETE execution."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)

        rows = query.execute_delete("DELETE FROM users WHERE id = ?", (1,))

        assert isinstance(rows, int)


class TestExecuteScalar:
    """Test execute_scalar method."""

    def test_execute_scalar_success(self, db_connection: Mock, db_cursor: Mock) -> None:
        """Test successful scalar query."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True
        db_cursor.fetchone.return_value = (42,)

        query = Query(connection)

        result = query.execute_scalar("SELECT COUNT(*) FROM users")

        assert result == 42


class TestExecuteStoredProcedure:
    """Test execute_stored_procedure method."""

    def test_execute_stored_procedure_success(
        self, db_connection: Mock, db_cursor: Mock
    ) -> None:
        """Test execute stored procedure."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)

        results = query.execute_stored_procedure("sp_GetUsers")

        assert isinstance(results, list)


class TestQueryHelpers:
    """Test helper query methods."""

    def test_count_records_success(self, db_connection: Mock) -> None:
        """Test count records."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_connection.cursor.return_value
        connection.is_connected = True
        # Mock with count column
        connection.cursor.description = [("count", None, None, None, None, None, None)]
        connection.cursor.fetchall.return_value = [(5,)]  # Tuple with count value

        query = Query(connection)

        count = query.count_records("users")

        assert isinstance(count, int)
        assert count == 5

    def test_get_table_info_success(self, db_connection: Mock, db_cursor: Mock) -> None:
        """Test get table info."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)

        info = query.get_table_info("users")

        assert isinstance(info, list)

    def test_query_success(self, db_connection: Mock, db_cursor: Mock) -> None:
        """Test query method with select."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)
        result = query.query("SELECT * FROM users", "select")

        assert isinstance(result, list)

    def test_query_and_get_all_success(
        self, db_connection: Mock, db_cursor: Mock
    ) -> None:
        """Test query_and_get_all method."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)
        results = query.query_and_get_all("SELECT * FROM users")

        assert isinstance(results, list)

    def test_get_value_in_column_success(self, db_connection: Mock) -> None:
        """Test get_value_in_column method."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_connection.cursor.return_value
        connection.is_connected = True
        connection.cursor.description = [("name", None, None, None, None, None, None)]
        connection.cursor.fetchall.return_value = [("User1",), ("User2",)]

        query = Query(connection)
        values = query.get_value_in_column("SELECT name FROM users", "name")

        assert isinstance(values, list)
        assert len(values) == 2

    def test_insert_data_to_table_success(
        self, db_connection: Mock, db_cursor: Mock
    ) -> None:
        """Test insert_data_to_table method."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)
        data = {"name": "Test", "email": "test@example.com"}

        query.insert_data_to_table("users", data)

        db_cursor.execute.assert_called_once()

    def test_execute_batch_success(self, db_connection: Mock, db_cursor: Mock) -> None:
        """Test execute_batch method."""
        connection = Connection()
        connection.connection = db_connection
        connection.cursor = db_cursor
        connection.is_connected = True

        query = Query(connection)
        queries = [
            {
                "sql": "INSERT INTO users VALUES (?, ?)",
                "params": ("User1", "user1@example.com"),
            },
            {
                "sql": "INSERT INTO users VALUES (?, ?)",
                "params": ("User2", "user2@example.com"),
            },
        ]

        results = query.execute_batch(queries)

        assert isinstance(results, list)
        assert len(results) == 2
