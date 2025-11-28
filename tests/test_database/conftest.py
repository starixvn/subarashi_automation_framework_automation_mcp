"""Database module specific fixtures."""

from unittest.mock import Mock

import pytest


@pytest.fixture
def db_connection() -> Mock:
    """Create a configured mock database connection."""
    connection = Mock()
    cursor = Mock()

    cursor.description = [
        ("id", None, None, None, None, None, None),
        ("name", None, None, None, None, None, None),
        ("email", None, None, None, None, None, None),
    ]
    # Return tuples (execute_select will convert to dicts)
    cursor.fetchall.return_value = [
        (1, "User 1", "user1@example.com"),
        (2, "User 2", "user2@example.com"),
    ]
    cursor.fetchone.return_value = (1, "User 1", "user1@example.com")
    cursor.rowcount = 1

    connection.cursor.return_value = cursor
    connection.commit = Mock()
    connection.rollback = Mock()
    connection.close = Mock()
    connection.setencoding = Mock()

    return connection


@pytest.fixture
def db_cursor() -> Mock:
    """Create a configured mock database cursor."""
    cursor = Mock()
    cursor.description = [
        ("id", None, None, None, None, None, None),
        ("value", None, None, None, None, None, None),
    ]
    # Return tuples (execute_select will convert to dicts)
    cursor.fetchall.return_value = [(1, "test"), (2, "data")]
    cursor.fetchone.return_value = (1, "test")
    cursor.rowcount = 2
    cursor.execute = Mock()
    return cursor
