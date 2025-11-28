"""Unit tests for src/Core/api/assertions.py"""

from unittest.mock import Mock

import pytest

from src.Core.exceptions import AutomationError
from src.Core.api.assertions import Assertions


class TestStatusCodeAssertions:
    """Test status code assertions."""

    def test_status_code_equals_success(self, api_response_json: Mock) -> None:
        """Test status_code_equals passes when equal."""
        Assertions.status_code_equals(api_response_json, 200)

    def test_status_code_equals_failure(self, api_response_json: Mock) -> None:
        """Test status_code_equals raises error when not equal."""
        with pytest.raises(AutomationError, match="Status code mismatch"):
            Assertions.status_code_equals(api_response_json, 404)

    def test_status_code_in_range_success(self, api_response_json: Mock) -> None:
        """Test status_code_in_range passes when in range."""
        Assertions.status_code_in_range(api_response_json, 200, 299)

    def test_status_code_in_range_failure(self, api_response_json: Mock) -> None:
        """Test status_code_in_range raises error when out of range."""
        with pytest.raises(AutomationError, match="not in range"):
            Assertions.status_code_in_range(api_response_json, 300, 399)


class TestTextAssertions:
    """Test text content assertions."""

    def test_response_contains_text_success(self, api_response_json: Mock) -> None:
        """Test response_contains_text passes when text exists."""
        Assertions.response_contains_text(api_response_json, "Test User")

    def test_response_contains_text_failure(self, api_response_json: Mock) -> None:
        """Test response_contains_text raises error when text not found."""
        with pytest.raises(AutomationError, match="does not contain"):
            Assertions.response_contains_text(api_response_json, "nonexistent")

    def test_response_not_contains_text_success(self, api_response_json: Mock) -> None:
        """Test response_not_contains_text passes when text absent."""
        Assertions.response_not_contains_text(api_response_json, "xyz123")

    def test_response_not_contains_text_failure(self, api_response_json: Mock) -> None:
        """Test response_not_contains_text raises error when text found."""
        with pytest.raises(AutomationError, match="should not contain"):
            Assertions.response_not_contains_text(api_response_json, "Test")


class TestJSONFieldAssertions:
    """Test JSON field assertions."""

    def test_json_field_equals_success(self, api_response_json: Mock) -> None:
        """Test json_field_equals passes when equal."""
        Assertions.json_field_equals(api_response_json, "id", 1)

    def test_json_field_not_null_success(self, api_response_json: Mock) -> None:
        """Test json_field_not_null passes when not null."""
        Assertions.json_field_not_null(api_response_json, "name")

    def test_json_field_is_null_success(self, mock_api_response: Mock) -> None:
        """Test json_field_is_null passes when null."""
        mock_api_response.json.return_value = {"field": None}
        Assertions.json_field_is_null(mock_api_response, "field")


class TestHeaderAssertions:
    """Test header assertions."""

    def test_header_exists_success(self, api_response_json: Mock) -> None:
        """Test header_exists passes when header present."""
        Assertions.header_exists(api_response_json, "content-type")

    def test_header_equals_success(self, api_response_json: Mock) -> None:
        """Test header_equals passes when equal."""
        Assertions.header_equals(
            api_response_json, "content-type", "application/json; charset=utf-8"
        )

    def test_content_type_equals_success(self, api_response_json: Mock) -> None:
        """Test content_type_equals passes when equal."""
        Assertions.content_type_equals(
            api_response_json, "application/json; charset=utf-8"
        )


class TestArrayAssertions:
    """Test JSON array assertions."""

    def test_json_array_length_equals_success(self, mock_api_response: Mock) -> None:
        """Test json_array_length_equals passes when equal."""
        mock_api_response.json.return_value = {"items": [1, 2, 3]}
        Assertions.json_array_length_equals(mock_api_response, "items", 3)

    def test_json_array_not_empty_success(self, mock_api_response: Mock) -> None:
        """Test json_array_not_empty passes when not empty."""
        mock_api_response.json.return_value = {"items": [1]}
        Assertions.json_array_not_empty(mock_api_response, "items")
