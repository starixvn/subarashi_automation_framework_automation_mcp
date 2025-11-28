"""API module specific fixtures."""

from unittest.mock import Mock

import pytest


@pytest.fixture
def api_response_json() -> Mock:
    """Create mock API response with JSON data."""
    response = Mock()
    response.status = 200
    response.ok = True
    response.url = "https://api.example.com/users"
    response.headers = {
        "content-type": "application/json; charset=utf-8",
        "content-length": "250",
        "set-cookie": "session=abc123; Path=/",
    }
    response.text.return_value = (
        '{"id": 1, "name": "Test User", "email": "test@example.com"}'
    )
    response.json.return_value = {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com",
        "roles": ["admin", "user"],
        "metadata": {"created": "2024-01-01"},
    }
    return response


@pytest.fixture
def api_response_text() -> Mock:
    """Create mock API response with text data."""
    response = Mock()
    response.status = 200
    response.url = "https://api.example.com/page"
    response.headers = {"content-type": "text/html"}
    response.text.return_value = "<html><body>Test Page</body></html>"
    response.json.side_effect = ValueError("Not JSON")
    return response


@pytest.fixture
def api_response_error() -> Mock:
    """Create mock API error response."""
    response = Mock()
    response.status = 404
    response.ok = False
    response.url = "https://api.example.com/notfound"
    response.headers = {"content-type": "application/json"}
    response.text.return_value = '{"error": "Not Found"}'
    response.json.return_value = {"error": "Not Found", "code": 404}
    return response
