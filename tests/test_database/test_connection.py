"""Unit tests for src/Core/database/connection.py"""

from unittest.mock import Mock, patch

import pytest

from src.Core.exceptions import AutomationError
from src.Core.database.connection import Connection


class TestConnectionConnect:
    """Test Connection.connect method."""

    @patch("src.Core.database.connection.pyodbc")
    def test_connect_with_trusted_connection(self, mock_pyodbc: Mock) -> None:
        """Test connect with trusted connection."""
        connection = Connection()
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_pyodbc.connect.return_value = mock_conn

        connection.connect("server", "database", trusted_connection=True)

        assert connection.is_connected is True
        assert connection.connection == mock_conn

    @patch("src.Core.database.connection.pyodbc")
    def test_connect_with_credentials(self, mock_pyodbc: Mock) -> None:
        """Test connect with username and password."""
        connection = Connection()
        mock_conn = Mock()
        mock_pyodbc.connect.return_value = mock_conn

        connection.connect(
            "server", "database", "user", "pass", trusted_connection=False
        )

        assert connection.is_connected is True

    @patch("src.Core.database.connection.pyodbc")
    def test_connect_error(self, mock_pyodbc: Mock) -> None:
        """Test connect raises AutomationError on failure."""
        connection = Connection()
        mock_pyodbc.connect.side_effect = Exception("Connection failed")

        with pytest.raises(AutomationError, match="Failed to connect"):
            connection.connect("server", "database")


class TestConnectionDisconnect:
    """Test Connection.disconnect method."""

    def test_disconnect_success(self) -> None:
        """Test successful disconnect."""
        connection = Connection()
        connection.cursor = Mock()
        connection.connection = Mock()
        connection.is_connected = True

        connection.disconnect()

        assert connection.is_connected is False
        assert connection.cursor is None
        assert connection.connection is None

    def test_close_calls_disconnect(self) -> None:
        """Test close calls disconnect."""
        connection = Connection()
        connection.cursor = Mock()
        connection.connection = Mock()
        connection.is_connected = True

        connection.close()

        assert connection.is_connected is False


class TestConnectionTransactions:
    """Test transaction methods."""

    def test_commit_success(self) -> None:
        """Test commit transaction."""
        connection = Connection()
        connection.is_connected = True
        connection.connection = Mock()

        connection.commit()

        connection.connection.commit.assert_called_once()

    def test_rollback_success(self) -> None:
        """Test rollback transaction."""
        connection = Connection()
        connection.is_connected = True
        connection.connection = Mock()

        connection.rollback()

        connection.connection.rollback.assert_called_once()


class TestConnectionInfo:
    """Test connection info methods."""

    def test_get_connection_info_connected(self) -> None:
        """Test get connection info when connected."""
        connection = Connection()
        connection.is_connected = True
        mock_conn = Mock()
        mock_conn.getinfo.return_value = "TestServer"
        connection.connection = mock_conn

        info = connection.get_connection_info()

        assert info["connected"] is True

    def test_test_connection_success(self) -> None:
        """Test test_connection returns True when connected."""
        connection = Connection()
        connection.is_connected = True
        connection.cursor = Mock()

        result = connection.test_connection()

        assert result is True

    def test_test_connection_failure(self) -> None:
        """Test test_connection returns False when not connected."""
        connection = Connection()
        connection.is_connected = False

        result = connection.test_connection()

        assert result is False


class TestConnectionQueries:
    """Test query info methods."""

    def test_get_tables_success(self) -> None:
        """Test get tables list."""
        connection = Connection()
        connection.is_connected = True
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [("Table1",), ("Table2",)]
        connection.cursor = mock_cursor

        tables = connection.get_tables()

        assert tables == ["Table1", "Table2"]


class TestContextManager:
    """Test context manager protocol."""

    def test_context_manager_enter(self) -> None:
        """Test __enter__ returns self."""
        connection = Connection()

        result = connection.__enter__()

        assert result is connection

    def test_context_manager_exit(self) -> None:
        """Test __exit__ calls disconnect."""
        connection = Connection()
        connection.cursor = Mock()
        connection.connection = Mock()
        connection.is_connected = True

        connection.__exit__(None, None, None)

        assert connection.is_connected is False
