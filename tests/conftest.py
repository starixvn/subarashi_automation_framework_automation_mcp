"""
Pytest configuration and fixtures for Core module unit tests.

This module provides common fixtures and mocks used across all test modules.
"""

from typing import Any, Dict, Generator
from unittest.mock import Mock

import pytest


# ============================================================================
# PLAYWRIGHT MOCKS
# ============================================================================


@pytest.fixture
def mock_page() -> Mock:
    """Create a mock Playwright Page object."""
    page = Mock()
    page.url = "https://example.com"
    page.title.return_value = "Test Page"
    page.content.return_value = "<html><body>Test Content</body></html>"
    page.frames = []
    page.context = Mock()
    page.context.request = Mock()
    return page


@pytest.fixture
def mock_locator() -> Mock:
    """Create a mock Playwright Locator object."""
    locator = Mock()
    locator.is_visible.return_value = True
    locator.is_enabled.return_value = True
    locator.is_checked.return_value = False
    locator.is_editable.return_value = True
    locator.count.return_value = 1
    locator.text_content.return_value = "Sample Text"
    locator.inner_text.return_value = "Sample Text"
    locator.inner_html.return_value = "<div>Sample Text</div>"
    locator.input_value.return_value = "Sample Value"
    locator.get_attribute.return_value = "sample-attribute"
    return locator


@pytest.fixture
def mock_frame() -> Mock:
    """Create a mock Playwright Frame object."""
    frame = Mock()
    frame.url = "https://example.com/frame"
    frame.name = "test-frame"
    frame.content.return_value = "<html><body>Frame Content</body></html>"
    frame.child_frames = []
    return frame


@pytest.fixture
def mock_frame_locator() -> Mock:
    """Create a mock Playwright FrameLocator object."""
    frame_locator = Mock()
    frame_locator.locator = Mock(return_value=Mock())
    return frame_locator


@pytest.fixture
def mock_api_response() -> Mock:
    """Create a mock Playwright APIResponse object."""
    response = Mock()
    response.status = 200
    response.ok = True
    response.url = "https://api.example.com/test"
    response.headers = {
        "content-type": "application/json",
        "content-length": "100",
    }
    response.text.return_value = '{"message": "success"}'
    response.json.return_value = {
        "message": "success",
        "data": {"id": 1, "name": "test"},
    }
    return response


@pytest.fixture
def mock_api_request_context() -> Mock:
    """Create a mock Playwright APIRequestContext object."""
    api_context = Mock()

    # Mock response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.ok = True
    mock_response.url = "https://api.example.com/test"
    mock_response.headers = {"content-type": "application/json"}
    mock_response.text.return_value = '{"message": "success"}'
    mock_response.json.return_value = {"message": "success"}

    # Set all HTTP methods to return the mock response
    api_context.get.return_value = mock_response
    api_context.post.return_value = mock_response
    api_context.put.return_value = mock_response
    api_context.patch.return_value = mock_response
    api_context.delete.return_value = mock_response
    api_context.head.return_value = mock_response
    api_context.fetch.return_value = mock_response

    return api_context


# ============================================================================
# DATABASE MOCKS
# ============================================================================


@pytest.fixture
def mock_pyodbc_connection() -> Mock:
    """Create a mock pyodbc Connection object."""
    connection = Mock()
    connection.cursor.return_value = Mock()
    connection.commit = Mock()
    connection.rollback = Mock()
    connection.close = Mock()
    connection.setencoding = Mock()

    # Mock getinfo for connection info
    connection.getinfo = Mock(
        side_effect=lambda x: {
            1: "TestServer",  # SQL_SERVER_NAME
            2: "TestDB",  # SQL_DATABASE_NAME
            6: "SQL Server",  # SQL_DRIVER_NAME
        }.get(x, "Unknown")
    )

    return connection


@pytest.fixture
def mock_pyodbc_cursor() -> Mock:
    """Create a mock pyodbc Cursor object."""
    cursor = Mock()
    cursor.description = [
        ("id", None, None, None, None, None, None),
        ("name", None, None, None, None, None, None),
    ]
    cursor.fetchall.return_value = [
        (1, "Test 1"),
        (2, "Test 2"),
    ]
    cursor.fetchone.return_value = (1, "Test 1")
    cursor.rowcount = 1
    cursor.execute = Mock()
    cursor.close = Mock()
    return cursor


# ============================================================================
# GOOGLE SHEETS MOCKS
# ============================================================================


@pytest.fixture
def mock_google_service() -> Mock:
    """Create a mock Google Sheets API service."""
    service = Mock()
    spreadsheets = Mock()
    values = Mock()

    # Mock get operation
    get_result = {
        "range": "Sheet1!A1:Z100",
        "values": [
            ["Header1", "Header2", "Header3"],
            ["Value1", "Value2", "Value3"],
        ],
    }
    values.get.return_value.execute.return_value = get_result

    # Mock update operation
    update_result = {
        "updatedCells": 1,
        "updatedRows": 1,
        "updatedColumns": 1,
    }
    values.update.return_value.execute.return_value = update_result

    # Mock append operation
    append_result = {
        "updates": {
            "updatedCells": 3,
            "updatedRows": 1,
        }
    }
    values.append.return_value.execute.return_value = append_result

    # Mock clear operation
    clear_result = {"clearedRange": "Sheet1!A1:Z100"}
    values.clear.return_value.execute.return_value = clear_result

    # Wire everything together
    spreadsheets.values.return_value = values
    spreadsheets.get.return_value.execute.return_value = {
        "spreadsheetId": "test-sheet-id",
        "properties": {"title": "Test Spreadsheet"},
    }
    spreadsheets.batchUpdate.return_value.execute.return_value = {}

    service.spreadsheets.return_value = spreadsheets

    return service


# ============================================================================
# SLACK MOCKS
# ============================================================================


@pytest.fixture
def mock_slack_client() -> Mock:
    """Create a mock Slack WebClient."""
    client = Mock()
    response = {"ok": True, "ts": "1234567890.123456"}
    client.chat_postMessage.return_value = response
    return client


# ============================================================================
# FILE SYSTEM MOCKS
# ============================================================================


@pytest.fixture
def temp_test_file(tmp_path: Any) -> Generator[Any, None, None]:
    """Create a temporary test file."""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Test content")
    yield file_path
    # Cleanup happens automatically with tmp_path


@pytest.fixture
def temp_json_file(tmp_path: Any) -> Generator[Any, None, None]:
    """Create a temporary JSON file."""
    import json

    file_path = tmp_path / "test_data.json"
    data = {"key": "value", "number": 123}
    file_path.write_text(json.dumps(data))
    yield file_path


@pytest.fixture
def temp_excel_file(tmp_path: Any) -> Generator[Any, None, None]:
    """Create a temporary Excel file."""
    import pandas as pd

    file_path = tmp_path / "test_data.xlsx"
    df = pd.DataFrame({"A": [1, 2, 3], "B": ["a", "b", "c"]})
    df.to_excel(file_path, index=False)
    yield file_path


# ============================================================================
# CONFIG MOCKS
# ============================================================================


@pytest.fixture
def mock_config(monkeypatch: Any) -> Dict[str, Any]:
    """Mock Config settings for tests."""
    config_values = {
        "TIMEOUT": 30000,
        "VIEWPORT_WIDTH": 1280,
        "VIEWPORT_HEIGHT": 720,
        "HEADLESS": False,
        "SCREENSHOT_ON_FAILURE": True,
        "FULL_PAGE_SCREENSHOT": True,
        "ALLURE_ENABLED": False,  # Disable Allure for unit tests
        "GOOGLE_SHEETS_ENABLED": False,
        "SLACK_BOT_TOKEN": "",
        "SLACK_CHANNEL_ID": "",
    }

    # Mock Config class attributes
    from config import config as config_module

    for key, value in config_values.items():
        monkeypatch.setattr(config_module.Config, key, value)

    return config_values


# ============================================================================
# UTILITY FIXTURES
# ============================================================================


@pytest.fixture
def sample_html() -> str:
    """Return sample HTML content for testing."""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Test Page</title></head>
    <body>
        <div id="main">
            <h1>Test Header</h1>
            <p class="content">Test content paragraph</p>
            <button id="submit-btn">Submit</button>
            <input type="text" id="username" placeholder="Username" />
        </div>
    </body>
    </html>
    """


@pytest.fixture
def sample_json_data() -> Dict[str, Any]:
    """Return sample JSON data for testing."""
    return {
        "status": "success",
        "code": 200,
        "data": {
            "id": 1,
            "name": "Test User",
            "email": "test@example.com",
            "roles": ["admin", "user"],
            "metadata": {
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-02T00:00:00Z",
            },
        },
        "items": [
            {"id": 1, "value": "first"},
            {"id": 2, "value": "second"},
            {"id": 3, "value": "third"},
        ],
    }


@pytest.fixture(autouse=True)
def reset_logging() -> Generator[None, None, None]:
    """Reset logging configuration for each test."""
    import logging

    # Store original level
    original_level = logging.root.level
    yield
    # Restore original level
    logging.root.setLevel(original_level)
