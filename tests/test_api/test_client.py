"""Unit tests for src/Core/api/client.py"""

from unittest.mock import Mock

import pytest

from src.Core.exceptions import AutomationError
from src.Core.api.client import Client


class TestClientGet:
    """Test Client.get method."""

    def test_get_success(self, mock_api_request_context: Mock) -> None:
        """Test successful GET request."""
        client = Client(mock_api_request_context)

        response = client.get("https://api.example.com/users")

        assert response.status == 200
        mock_api_request_context.get.assert_called_once()

    def test_get_with_path(self, mock_api_request_context: Mock) -> None:
        """Test GET with path parameter."""
        client = Client(mock_api_request_context)

        client.get("https://api.example.com", path="/users")

        mock_api_request_context.get.assert_called_once()

    def test_get_with_headers(self, mock_api_request_context: Mock) -> None:
        """Test GET with headers."""
        client = Client(mock_api_request_context)
        headers = {"Authorization": "Bearer token"}

        client.get("https://api.example.com", headers=headers)

        mock_api_request_context.get.assert_called_once()

    def test_get_with_params(self, mock_api_request_context: Mock) -> None:
        """Test GET with query parameters."""
        client = Client(mock_api_request_context)
        params = {"page": 1, "limit": 10}

        client.get("https://api.example.com", params=params)

        mock_api_request_context.get.assert_called_once()

    def test_get_error(self, mock_api_request_context: Mock) -> None:
        """Test GET raises AutomationError on failure."""
        client = Client(mock_api_request_context)
        mock_api_request_context.get.side_effect = Exception("Network error")

        with pytest.raises(AutomationError, match="GET request failed"):
            client.get("https://api.example.com")


class TestClientPost:
    """Test Client.post method."""

    def test_post_success(self, mock_api_request_context: Mock) -> None:
        """Test successful POST request."""
        client = Client(mock_api_request_context)

        response = client.post("https://api.example.com/users")

        assert response.status == 200
        mock_api_request_context.post.assert_called_once()

    def test_post_with_data(self, mock_api_request_context: Mock) -> None:
        """Test POST with JSON data."""
        client = Client(mock_api_request_context)
        data = {"name": "Test User"}

        client.post("https://api.example.com", data=data)

        mock_api_request_context.post.assert_called_once()

    def test_post_with_form_data(self, mock_api_request_context: Mock) -> None:
        """Test POST with form data."""
        client = Client(mock_api_request_context)
        form_data = {"username": "test", "password": "pass"}

        client.post("https://api.example.com", form_data=form_data)

        mock_api_request_context.post.assert_called_once()

    def test_post_error(self, mock_api_request_context: Mock) -> None:
        """Test POST raises AutomationError on failure."""
        client = Client(mock_api_request_context)
        mock_api_request_context.post.side_effect = Exception("Error")

        with pytest.raises(AutomationError, match="POST request failed"):
            client.post("https://api.example.com")


class TestClientPut:
    """Test Client.put method."""

    def test_put_success(self, mock_api_request_context: Mock) -> None:
        """Test successful PUT request."""
        client = Client(mock_api_request_context)

        response = client.put("https://api.example.com/users/1")

        assert response.status == 200

    def test_put_with_data(self, mock_api_request_context: Mock) -> None:
        """Test PUT with data."""
        client = Client(mock_api_request_context)
        data = {"name": "Updated"}

        client.put("https://api.example.com/users/1", data=data)

        mock_api_request_context.put.assert_called_once()


class TestClientPatch:
    """Test Client.patch method."""

    def test_patch_success(self, mock_api_request_context: Mock) -> None:
        """Test successful PATCH request."""
        client = Client(mock_api_request_context)

        response = client.patch("https://api.example.com/users/1")

        assert response.status == 200


class TestClientDelete:
    """Test Client.delete method."""

    def test_delete_success(self, mock_api_request_context: Mock) -> None:
        """Test successful DELETE request."""
        client = Client(mock_api_request_context)

        response = client.delete("https://api.example.com/users/1")

        assert response.status == 200


class TestClientOtherMethods:
    """Test other HTTP methods."""

    def test_head_success(self, mock_api_request_context: Mock) -> None:
        """Test successful HEAD request."""
        client = Client(mock_api_request_context)

        response = client.head("https://api.example.com")

        assert response.status == 200

    def test_options_success(self, mock_api_request_context: Mock) -> None:
        """Test successful OPTIONS request."""
        client = Client(mock_api_request_context)

        response = client.options("https://api.example.com")

        assert response.status == 200

    def test_request_custom_method(self, mock_api_request_context: Mock) -> None:
        """Test custom request method."""
        client = Client(mock_api_request_context)

        response = client.request("CUSTOM", "https://api.example.com")

        assert response.status == 200
