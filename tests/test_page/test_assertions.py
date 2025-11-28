"""Unit tests for src/Core/page/assertions.py"""

from unittest.mock import Mock

import pytest

from src.Core.exceptions import ElementError
from src.Core.page.assertions import Assertions


class TestElementVisibility:
    """Test element visibility assertions."""

    def test_element_visible_true(self, mock_page: Mock) -> None:
        """Test element_visible returns True when visible."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.is_visible.return_value = True
        mock_page.locator.return_value = mock_locator

        result = assertions.element_visible("#element")

        assert result is True

    def test_element_visible_false(self, mock_page: Mock) -> None:
        """Test element_visible returns False when not visible."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.is_visible.return_value = False
        mock_page.locator.return_value = mock_locator

        result = assertions.element_visible("#element")

        assert result is False

    def test_element_visible_error(self, mock_page: Mock) -> None:
        """Test element_visible raises ElementError on failure."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.is_visible.side_effect = Exception("Failed")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError):
            assertions.element_visible("#element")

    def test_element_hidden_true(self, mock_page: Mock) -> None:
        """Test element_hidden returns True when not visible."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.is_visible.return_value = False
        mock_page.locator.return_value = mock_locator

        result = assertions.element_hidden("#element")

        assert result is True

    def test_element_hidden_false(self, mock_page: Mock) -> None:
        """Test element_hidden returns False when visible."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.is_visible.return_value = True
        mock_page.locator.return_value = mock_locator

        result = assertions.element_hidden("#element")

        assert result is False


class TestElementExistence:
    """Test element existence assertions."""

    def test_element_exists_true(self, mock_page: Mock) -> None:
        """Test element_exists returns True when count > 0."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.count.return_value = 1
        mock_page.locator.return_value = mock_locator

        result = assertions.element_exists("#element")

        assert result is True

    def test_element_exists_false(self, mock_page: Mock) -> None:
        """Test element_exists returns False when count = 0."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.count.return_value = 0
        mock_page.locator.return_value = mock_locator

        result = assertions.element_exists("#element")

        assert result is False

    def test_element_exists_error(self, mock_page: Mock) -> None:
        """Test element_exists raises ElementError on failure."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.count.side_effect = Exception("Failed")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError):
            assertions.element_exists("#element")


class TestElementState:
    """Test element state assertions."""

    def test_element_enabled_true(self, mock_page: Mock) -> None:
        """Test element_enabled returns True when enabled."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.is_enabled.return_value = True
        mock_page.locator.return_value = mock_locator

        result = assertions.element_enabled("#element")

        assert result is True

    def test_element_disabled_true(self, mock_page: Mock) -> None:
        """Test element_disabled returns True when disabled."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.is_disabled.return_value = True
        mock_page.locator.return_value = mock_locator

        result = assertions.element_disabled("#element")

        assert result is True

    def test_element_checked_true(self, mock_page: Mock) -> None:
        """Test element_checked returns True when checked."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.is_checked.return_value = True
        mock_page.locator.return_value = mock_locator

        result = assertions.element_checked("#element")

        assert result is True

    def test_element_editable_true(self, mock_page: Mock) -> None:
        """Test element_editable returns True when editable."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.is_editable.return_value = True
        mock_page.locator.return_value = mock_locator

        result = assertions.element_editable("#element")

        assert result is True


class TestTextAssertions:
    """Test text comparison assertions."""

    def test_element_text_equals_success(self, mock_page: Mock) -> None:
        """Test element_text_equals passes when equal."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.text_content.return_value = "Expected Text"
        mock_page.locator.return_value = mock_locator

        assertions.element_text_equals("#element", "Expected Text")

    def test_element_text_equals_failure(self, mock_page: Mock) -> None:
        """Test element_text_equals raises error when not equal."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.text_content.return_value = "Actual"
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Text mismatch"):
            assertions.element_text_equals("#element", "Expected")

    def test_element_text_contains_success(self, mock_page: Mock) -> None:
        """Test element_text_contains passes when text is contained."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.text_content.return_value = "Hello World"
        mock_page.locator.return_value = mock_locator

        assertions.element_text_contains("#element", "World")

    def test_element_text_contains_failure(self, mock_page: Mock) -> None:
        """Test element_text_contains raises error when not contained."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.text_content.return_value = "Hello"
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="not found in element"):
            assertions.element_text_contains("#element", "World")


class TestValueAssertions:
    """Test value comparison assertions."""

    def test_element_value_equals_success(self, mock_page: Mock) -> None:
        """Test element_value_equals passes when equal."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.input_value.return_value = "test value"
        mock_page.locator.return_value = mock_locator

        assertions.element_value_equals("#input", "test value")

    def test_element_value_equals_failure(self, mock_page: Mock) -> None:
        """Test element_value_equals raises error when not equal."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.input_value.return_value = "actual"
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Value mismatch"):
            assertions.element_value_equals("#input", "expected")


class TestAttributeAssertions:
    """Test attribute comparison assertions."""

    def test_element_attribute_equals_success(self, mock_page: Mock) -> None:
        """Test element_attribute_equals passes when equal."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.get_attribute.return_value = "value"
        mock_page.locator.return_value = mock_locator

        assertions.element_attribute_equals("#element", "attr", "value")

    def test_element_attribute_contains_success(self, mock_page: Mock) -> None:
        """Test element_attribute_contains passes when contained."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.get_attribute.return_value = "test value"
        mock_page.locator.return_value = mock_locator

        assertions.element_attribute_contains("#element", "attr", "value")


class TestPageAssertions:
    """Test page-level assertions."""

    def test_page_title_equals_success(self, mock_page: Mock) -> None:
        """Test page_title_equals passes when equal."""
        assertions = Assertions(mock_page)
        mock_page.title.return_value = "Test Page"

        assertions.page_title_equals("Test Page")

    def test_page_title_contains_success(self, mock_page: Mock) -> None:
        """Test page_title_contains passes when contained."""
        assertions = Assertions(mock_page)
        mock_page.title.return_value = "Test Page Title"

        assertions.page_title_contains("Page")

    def test_page_url_equals_success(self, mock_page: Mock) -> None:
        """Test page_url_equals passes when equal."""
        assertions = Assertions(mock_page)
        mock_page.url = "https://example.com"

        assertions.page_url_equals("https://example.com")

    def test_page_url_contains_success(self, mock_page: Mock) -> None:
        """Test page_url_contains passes when contained."""
        assertions = Assertions(mock_page)
        mock_page.url = "https://example.com/page"

        assertions.page_url_contains("example.com")


class TestCountAssertions:
    """Test element count assertions."""

    def test_element_count_equals_success(self, mock_page: Mock) -> None:
        """Test element_count_equals passes when equal."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.count.return_value = 5
        mock_page.locator.return_value = mock_locator

        assertions.element_count_equals(".item", 5)

    def test_element_count_greater_than_success(self, mock_page: Mock) -> None:
        """Test element_count_greater_than passes when greater."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.count.return_value = 5
        mock_page.locator.return_value = mock_locator

        assertions.element_count_greater_than(".item", 3)


class TestPageTextAssertion:
    """Test page_has_text assertion."""

    def test_page_has_text_success(self, mock_page: Mock) -> None:
        """Test page_has_text passes when text exists."""
        assertions = Assertions(mock_page)
        mock_page.content.return_value = "<html>Test Content</html>"

        assertions.page_has_text("Test")


class TestVerifyElementExist:
    """Test verify_element_exist assertion."""

    def test_verify_element_exist_success(self, mock_page: Mock) -> None:
        """Test verify_element_exist passes when visible and exists."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.count.return_value = 1
        mock_locator.is_visible.return_value = True
        mock_page.locator.return_value = mock_locator

        assertions.verify_element_exist("#element")

    def test_does_element_exist_true(self, mock_page: Mock) -> None:
        """Test does_element_exist returns True."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.count.return_value = 1
        mock_page.locator.return_value = mock_locator

        result = assertions.does_element_exist("#element")

        assert result is True

    def test_does_element_exist_false(self, mock_page: Mock) -> None:
        """Test does_element_exist returns False on error."""
        assertions = Assertions(mock_page)
        mock_locator = Mock()
        mock_locator.count.side_effect = Exception("Error")
        mock_page.locator.return_value = mock_locator

        result = assertions.does_element_exist("#element")

        assert result is False


class TestFrameAssertions:
    """Test frame-specific assertions."""

    def test_element_visible_on_frame(self, page_with_frames: Mock) -> None:
        """Test element_visible_on_frame returns visibility state."""
        assertions = Assertions(page_with_frames)
        mock_frame_locator = Mock()
        mock_element = Mock()
        mock_element.is_visible.return_value = True
        mock_frame_locator.locator.return_value = mock_element
        page_with_frames.frame_locator.return_value = mock_frame_locator

        result = assertions.element_visible_on_frame("//iframe", "#element")

        assert result is True

    def test_element_exists_on_frame(self, page_with_frames: Mock) -> None:
        """Test element_exists_on_frame returns existence state."""
        assertions = Assertions(page_with_frames)
        mock_frame_locator = Mock()
        mock_element = Mock()
        mock_element.count.return_value = 1
        mock_frame_locator.locator.return_value = mock_element
        page_with_frames.frame_locator.return_value = mock_frame_locator

        result = assertions.element_exists_on_frame("//iframe", "#element")

        assert result is True

    def test_element_enabled_on_frame(self, page_with_frames: Mock) -> None:
        """Test element_enabled_on_frame returns enabled state."""
        assertions = Assertions(page_with_frames)
        mock_frame_locator = Mock()
        mock_element = Mock()
        mock_element.is_enabled.return_value = True
        mock_frame_locator.locator.return_value = mock_element
        page_with_frames.frame_locator.return_value = mock_frame_locator

        result = assertions.element_enabled_on_frame("//iframe", "#element")

        assert result is True
