"""Unit tests for src/Core/api/extractor.py"""

from unittest.mock import Mock

from src.Core.api.extractor import Extractor


class TestBasicExtraction:
    """Test basic extraction methods."""

    def test_text_success(self, api_response_json: Mock) -> None:
        """Test extract text from response."""
        result = Extractor.text(api_response_json)
        assert isinstance(result, str)
        assert "Test User" in result

    def test_json_success(self, api_response_json: Mock) -> None:
        """Test extract JSON from response."""
        result = Extractor.json(api_response_json)
        assert isinstance(result, dict)
        assert result["id"] == 1

    def test_status_code_success(self, api_response_json: Mock) -> None:
        """Test extract status code."""
        result = Extractor.status_code(api_response_json)
        assert result == 200

    def test_headers_success(self, api_response_json: Mock) -> None:
        """Test extract headers."""
        result = Extractor.headers(api_response_json)
        assert isinstance(result, dict)
        assert "content-type" in result


class TestHeaderExtraction:
    """Test header extraction methods."""

    def test_header_value_success(self, api_response_json: Mock) -> None:
        """Test extract specific header value."""
        result = Extractor.header_value(api_response_json, "content-type")
        assert result is not None

    def test_header_value_case_insensitive(self, api_response_json: Mock) -> None:
        """Test header extraction is case insensitive."""
        result = Extractor.header_value(api_response_json, "Content-Type")
        assert result is not None

    def test_header_value_not_found(self, api_response_json: Mock) -> None:
        """Test header_value returns None when not found."""
        result = Extractor.header_value(api_response_json, "nonexistent")
        assert result is None


class TestJSONFieldExtraction:
    """Test JSON field extraction methods."""

    def test_json_field_simple(self, api_response_json: Mock) -> None:
        """Test extract simple JSON field."""
        result = Extractor.json_field(api_response_json, "id")
        assert result == 1

    def test_json_field_nested(self, api_response_json: Mock) -> None:
        """Test extract nested JSON field."""
        result = Extractor.json_field(api_response_json, "metadata.created")
        assert result == "2024-01-01"

    def test_json_field_array_index(self, api_response_json: Mock) -> None:
        """Test extract array element by index."""
        result = Extractor.json_field(api_response_json, "roles.0")
        assert result == "admin"

    def test_json_field_not_found(self, api_response_json: Mock) -> None:
        """Test json_field returns None when not found."""
        result = Extractor.json_field(api_response_json, "nonexistent")
        assert result is None


class TestRegexExtraction:
    """Test regex extraction methods."""

    def test_regex_match_success(self, api_response_json: Mock) -> None:
        """Test regex match extraction."""
        result = Extractor.regex_match(api_response_json, r"Test (\w+)", 1)
        assert result == "User"

    def test_regex_match_no_match(self, api_response_json: Mock) -> None:
        """Test regex_match returns None when no match."""
        result = Extractor.regex_match(api_response_json, r"xyz123")
        assert result is None

    def test_regex_match_all_success(self, mock_api_response: Mock) -> None:
        """Test regex match all."""
        mock_api_response.text.return_value = "test1 test2 test3"
        result = Extractor.regex_match_all(mock_api_response, r"test\d")
        assert len(result) == 3


class TestJSONUtilities:
    """Test JSON utility methods."""

    def test_json_string_to_dict_success(self) -> None:
        """Test convert JSON string to dict."""
        json_str = '{"key": "value"}'
        result = Extractor.json_string_to_dict(json_str)
        assert isinstance(result, dict)
        assert result["key"] == "value"

    def test_url_success(self, api_response_json: Mock) -> None:
        """Test extract URL."""
        result = Extractor.url(api_response_json)
        assert result == "https://api.example.com/users"

    def test_content_type_success(self, api_response_json: Mock) -> None:
        """Test extract content type."""
        result = Extractor.content_type(api_response_json)
        assert "json" in result.lower()


class TestAdvancedExtraction:
    """Test advanced extraction methods."""

    def test_json_keys_success(self, api_response_json: Mock) -> None:
        """Test extract JSON keys."""
        result = Extractor.json_keys(api_response_json, "")
        assert isinstance(result, list)
        assert "id" in result

    def test_json_array_field_success(self, api_response_json: Mock) -> None:
        """Test extract array field by index."""
        result = Extractor.json_array_field(api_response_json, "roles", 0)
        assert result == "admin"
