"""
Unit tests for src/Core/page/actions.py

Tests all action methods including clicks, fills, selections, and frame operations.
Coverage includes success cases, error handling, and edge cases.
"""

from unittest.mock import Mock

import pytest

from src.Core.exceptions import ElementError
from src.Core.page.actions import Actions


class TestActionsBasicOperations:
    """Test basic action methods."""

    def test_click_success(self, mock_page: Mock) -> None:
        """Test successful click action."""
        actions = Actions(mock_page)
        selector = "#submit-btn"

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        actions.click(selector)

        mock_page.locator.assert_called_once_with(selector)
        mock_locator.click.assert_called_once()

    def test_click_element_error(self, mock_page: Mock) -> None:
        """Test click raises ElementError on failure."""
        actions = Actions(mock_page)
        mock_locator = Mock()
        mock_locator.click.side_effect = Exception("Element not found")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Failed to click"):
            actions.click("#missing")

    def test_click_with_special_selector(self, mock_page: Mock) -> None:
        """Test click with special characters in selector."""
        actions = Actions(mock_page)
        selector = "button[data-test='submit-form']"

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        actions.click(selector)

        mock_page.locator.assert_called_with(selector)

    def test_double_click_success(self, mock_page: Mock) -> None:
        """Test successful double click."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        actions.double_click("#element")

        mock_locator.dblclick.assert_called_once()

    def test_double_click_with_retry(self, mock_page: Mock) -> None:
        """Test double click with retry decorator."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        # Fail first time, succeed second time
        mock_locator.dblclick.side_effect = [Exception("Fail"), None]
        mock_page.locator.return_value = mock_locator

        actions.double_click("#element")

        assert mock_locator.dblclick.call_count == 2

    def test_double_click_error(self, mock_page: Mock) -> None:
        """Test double click raises ElementError."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.dblclick.side_effect = Exception("Failed")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Failed to double click"):
            actions.double_click("#element")

    def test_right_click_success(self, mock_page: Mock) -> None:
        """Test successful right click."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        actions.right_click("#context-menu")

        mock_locator.click.assert_called_once_with(button="right")

    def test_right_click_error(self, mock_page: Mock) -> None:
        """Test right click error handling."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.click.side_effect = Exception("Failed")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Failed to right click"):
            actions.right_click("#element")

    def test_fill_success(self, mock_page: Mock) -> None:
        """Test successful fill action."""
        actions = Actions(mock_page)
        selector = "#username"
        text = "testuser"

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        actions.fill(selector, text)

        mock_locator.clear.assert_called_once()
        mock_locator.fill.assert_called_once_with(text)

    def test_fill_with_empty_string(self, mock_page: Mock) -> None:
        """Test fill with empty string."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        actions.fill("#input", "")

        mock_locator.fill.assert_called_with("")

    def test_fill_with_special_characters(self, mock_page: Mock) -> None:
        """Test fill with special characters."""
        actions = Actions(mock_page)
        special_text = "Test@123!#$%"

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        actions.fill("#input", special_text)

        mock_locator.fill.assert_called_with(special_text)

    def test_fill_error(self, mock_page: Mock) -> None:
        """Test fill raises ElementError on failure."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.fill.side_effect = Exception("Cannot fill")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Failed to fill"):
            actions.fill("#input", "text")

    def test_fill_text_calls_fill(self, mock_page: Mock) -> None:
        """Test fill_text calls fill method."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        actions.fill_text("#input", "text")

        # Should call fill internally
        mock_locator.clear.assert_called_once()
        mock_locator.fill.assert_called_once_with("text")

    def test_type_text_success(self, mock_page: Mock) -> None:
        """Test successful type text action."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        actions.type_text("#search", "query")

        mock_locator.type.assert_called_once_with("query")

    def test_type_text_error(self, mock_page: Mock) -> None:
        """Test type text error handling."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.type.side_effect = Exception("Failed")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Failed to type"):
            actions.type_text("#input", "text")

    def test_clear_success(self, mock_page: Mock) -> None:
        """Test successful clear action."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        actions.clear("#input")

        mock_locator.clear.assert_called_once()

    def test_clear_error(self, mock_page: Mock) -> None:
        """Test clear error handling."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.clear.side_effect = Exception("Failed")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Failed to clear"):
            actions.clear("#input")


class TestActionsSelectionOperations:
    """Test selection and checkbox operations."""

    def test_select_option_success(self, mock_page: Mock) -> None:
        """Test successful select option."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        actions.select_option("#country", "USA")

        mock_locator.select_option.assert_called_once_with("USA")

    def test_select_option_error(self, mock_page: Mock) -> None:
        """Test select option error handling."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.select_option.side_effect = Exception("Option not found")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Failed to select"):
            actions.select_option("#select", "value")

    def test_check_success(self, mock_page: Mock) -> None:
        """Test successful check action."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        actions.check("#agree")

        mock_locator.check.assert_called_once()

    def test_check_error(self, mock_page: Mock) -> None:
        """Test check error handling."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.check.side_effect = Exception("Cannot check")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Failed to check"):
            actions.check("#checkbox")

    def test_check_checkbox_calls_check(self, mock_page: Mock) -> None:
        """Test check_checkbox calls check method."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        actions.check_checkbox("#terms")

        mock_locator.check.assert_called_once()

    def test_uncheck_success(self, mock_page: Mock) -> None:
        """Test successful uncheck action."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        actions.uncheck("#newsletter")

        mock_locator.uncheck.assert_called_once()

    def test_uncheck_error(self, mock_page: Mock) -> None:
        """Test uncheck error handling."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.uncheck.side_effect = Exception("Cannot uncheck")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Failed to uncheck"):
            actions.uncheck("#checkbox")


class TestActionsInteractionOperations:
    """Test hover, focus, and interaction operations."""

    def test_hover_success(self, mock_page: Mock) -> None:
        """Test successful hover action."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        actions.hover("#menu-item")

        mock_locator.hover.assert_called_once()

    def test_hover_error(self, mock_page: Mock) -> None:
        """Test hover error handling."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.hover.side_effect = Exception("Cannot hover")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Failed to hover"):
            actions.hover("#element")

    def test_focus_success(self, mock_page: Mock) -> None:
        """Test successful focus action."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        actions.focus("#input")

        mock_locator.focus.assert_called_once()

    def test_focus_error(self, mock_page: Mock) -> None:
        """Test focus error handling."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.focus.side_effect = Exception("Cannot focus")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Failed to focus"):
            actions.focus("#element")

    def test_press_key_success(self, mock_page: Mock) -> None:
        """Test successful press key action."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        actions.press_key("#input", "Enter")

        mock_locator.press.assert_called_once_with("Enter")

    def test_press_key_special_keys(self, mock_page: Mock) -> None:
        """Test press key with special keys."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        for key in ["Escape", "Tab", "ArrowDown", "Control+A"]:
            actions.press_key("#input", key)
            mock_locator.press.assert_called_with(key)

    def test_press_key_error(self, mock_page: Mock) -> None:
        """Test press key error handling."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.press.side_effect = Exception("Cannot press")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Failed to press key"):
            actions.press_key("#input", "Enter")

    def test_scroll_to_success(self, mock_page: Mock) -> None:
        """Test successful scroll to element."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        actions.scroll_to("#footer")

        mock_locator.scroll_into_view_if_needed.assert_called_once()

    def test_scroll_to_error(self, mock_page: Mock) -> None:
        """Test scroll to error handling."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.scroll_into_view_if_needed.side_effect = Exception("Cannot scroll")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Failed to scroll"):
            actions.scroll_to("#element")


class TestActionsDragDropAndUpload:
    """Test drag/drop and file upload operations."""

    def test_drag_and_drop_success(self, mock_page: Mock) -> None:
        """Test successful drag and drop."""
        actions = Actions(mock_page)

        source_locator = Mock()
        target_locator = Mock()

        def locator_side_effect(selector: str) -> Mock:
            if selector == "#source":
                return source_locator
            return target_locator

        mock_page.locator.side_effect = locator_side_effect

        actions.drag_and_drop("#source", "#target")

        source_locator.drag_to.assert_called_once_with(target_locator)

    def test_drag_and_drop_error(self, mock_page: Mock) -> None:
        """Test drag and drop error handling."""
        actions = Actions(mock_page)

        source_locator = Mock()
        source_locator.drag_to.side_effect = Exception("Cannot drag")
        mock_page.locator.return_value = source_locator

        with pytest.raises(ElementError, match="Failed to drag"):
            actions.drag_and_drop("#source", "#target")

    def test_upload_file_success(self, mock_page: Mock) -> None:
        """Test successful file upload."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        actions.upload_file("#file-input", "/path/to/file.pdf")

        mock_locator.set_input_files.assert_called_once_with("/path/to/file.pdf")

    def test_upload_file_error(self, mock_page: Mock) -> None:
        """Test upload file error handling."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.set_input_files.side_effect = Exception("Cannot upload")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Failed to upload"):
            actions.upload_file("#input", "/file.pdf")


class TestActionsGetOperations:
    """Test get text, attribute, and value operations."""

    def test_get_text_success(self, mock_page: Mock) -> None:
        """Test successful get text."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.text_content.return_value = "Sample Text"
        mock_page.locator.return_value = mock_locator

        result = actions.get_text("#element")

        assert result == "Sample Text"

    def test_get_text_empty(self, mock_page: Mock) -> None:
        """Test get text returns empty string when None."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.text_content.return_value = None
        mock_page.locator.return_value = mock_locator

        result = actions.get_text("#element")

        assert result == ""

    def test_get_text_error(self, mock_page: Mock) -> None:
        """Test get text error handling."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.text_content.side_effect = Exception("Cannot get text")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Failed to get text"):
            actions.get_text("#element")

    def test_get_attribute_success(self, mock_page: Mock) -> None:
        """Test successful get attribute."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.get_attribute.return_value = "test-value"
        mock_page.locator.return_value = mock_locator

        result = actions.get_attribute("#link", "href")

        assert result == "test-value"
        mock_locator.get_attribute.assert_called_once_with("href")

    def test_get_attribute_none(self, mock_page: Mock) -> None:
        """Test get attribute returns empty string when None."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.get_attribute.return_value = None
        mock_page.locator.return_value = mock_locator

        result = actions.get_attribute("#element", "data-test")

        assert result == ""

    def test_get_attribute_error(self, mock_page: Mock) -> None:
        """Test get attribute error handling."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.get_attribute.side_effect = Exception("Cannot get attribute")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Failed to get attribute"):
            actions.get_attribute("#element", "class")

    def test_get_value_success(self, mock_page: Mock) -> None:
        """Test successful get value."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.input_value.return_value = "input text"
        mock_page.locator.return_value = mock_locator

        result = actions.get_value("#input")

        assert result == "input text"

    def test_get_value_error(self, mock_page: Mock) -> None:
        """Test get value error handling."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.input_value.side_effect = Exception("Cannot get value")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Failed to get value"):
            actions.get_value("#input")


class TestActionsFrameOperations:
    """Test frame-specific operations."""

    def test_fill_on_frame_success(self, page_with_frames: Mock) -> None:
        """Test successful fill on frame."""
        actions = Actions(page_with_frames)

        mock_frame_locator = Mock()
        mock_element = Mock()
        mock_frame_locator.locator.return_value = mock_element
        page_with_frames.frame_locator.return_value = mock_frame_locator

        actions.fill_on_frame("//iframe", "#input", "text")

        mock_element.clear.assert_called_once()
        mock_element.fill.assert_called_once_with("text")

    def test_fill_on_frame_error(self, page_with_frames: Mock) -> None:
        """Test fill on frame error handling."""
        actions = Actions(page_with_frames)

        mock_frame_locator = Mock()
        mock_element = Mock()
        mock_element.fill.side_effect = Exception("Cannot fill")
        mock_frame_locator.locator.return_value = mock_element
        page_with_frames.frame_locator.return_value = mock_frame_locator

        with pytest.raises(ElementError, match="Failed to fill on frame"):
            actions.fill_on_frame("//iframe", "#input", "text")

    def test_click_on_frame_success(self, page_with_frames: Mock) -> None:
        """Test successful click on frame."""
        actions = Actions(page_with_frames)

        mock_frame_locator = Mock()
        mock_element = Mock()
        mock_frame_locator.locator.return_value = mock_element
        page_with_frames.frame_locator.return_value = mock_frame_locator

        actions.click_on_frame("//iframe", "#button")

        mock_element.click.assert_called_once()

    def test_click_on_frame_error(self, page_with_frames: Mock) -> None:
        """Test click on frame error handling."""
        actions = Actions(page_with_frames)

        mock_frame_locator = Mock()
        mock_element = Mock()
        mock_element.click.side_effect = Exception("Cannot click")
        mock_frame_locator.locator.return_value = mock_element
        page_with_frames.frame_locator.return_value = mock_frame_locator

        with pytest.raises(ElementError, match="Failed to click on frame"):
            actions.click_on_frame("//iframe", "#button")

    def test_get_text_on_frame_success(self, page_with_frames: Mock) -> None:
        """Test successful get text on frame."""
        actions = Actions(page_with_frames)

        mock_frame_locator = Mock()
        mock_element = Mock()
        mock_element.inner_text.return_value = "Frame Text"
        mock_frame_locator.locator.return_value = mock_element
        page_with_frames.frame_locator.return_value = mock_frame_locator

        result = actions.get_text_on_frame("//iframe", "#text")

        assert result == "Frame Text"

    def test_get_text_on_frame_error(self, page_with_frames: Mock) -> None:
        """Test get text on frame error handling."""
        actions = Actions(page_with_frames)

        mock_frame_locator = Mock()
        mock_element = Mock()
        mock_element.inner_text.side_effect = Exception("Cannot get text")
        mock_frame_locator.locator.return_value = mock_element
        page_with_frames.frame_locator.return_value = mock_frame_locator

        with pytest.raises(ElementError, match="Failed to get text on frame"):
            actions.get_text_on_frame("//iframe", "#text")


class TestActionsIndexedOperations:
    """Test operations with element indices."""

    def test_click_element_by_index_success(self, mock_page: Mock) -> None:
        """Test successful click by index."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_nth = Mock()
        mock_locator.nth.return_value = mock_nth
        mock_page.locator.return_value = mock_locator

        actions.click_element_by_index(".item", 2)

        mock_locator.nth.assert_called_once_with(2)
        mock_nth.click.assert_called_once()

    def test_click_element_by_index_error(self, mock_page: Mock) -> None:
        """Test click by index error handling."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_nth = Mock()
        mock_nth.click.side_effect = Exception("Index out of range")
        mock_locator.nth.return_value = mock_nth
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Failed to click element at index"):
            actions.click_element_by_index(".item", 5)

    def test_get_text_by_index_success(self, mock_page: Mock) -> None:
        """Test successful get text by index."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_nth = Mock()
        mock_nth.inner_text.return_value = "Item 3"
        mock_locator.nth.return_value = mock_nth
        mock_page.locator.return_value = mock_locator

        result = actions.get_text_by_index(".item", 2)

        assert result == "Item 3"

    def test_get_attribute_by_index_success(self, mock_page: Mock) -> None:
        """Test successful get attribute by index."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_nth = Mock()
        mock_nth.get_attribute.return_value = "value-3"
        mock_locator.nth.return_value = mock_nth
        mock_page.locator.return_value = mock_locator

        result = actions.get_attribute_by_index(".item", 2, "data-id")

        assert result == "value-3"

    def test_count_elements_success(self, mock_page: Mock) -> None:
        """Test successful count elements."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.count.return_value = 5
        mock_page.locator.return_value = mock_locator

        result = actions.count_elements(".item")

        assert result == 5

    def test_count_elements_zero(self, mock_page: Mock) -> None:
        """Test count elements returns zero."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.count.return_value = 0
        mock_page.locator.return_value = mock_locator

        result = actions.count_elements(".nonexistent")

        assert result == 0

    def test_count_elements_error(self, mock_page: Mock) -> None:
        """Test count elements error handling."""
        actions = Actions(mock_page)

        mock_locator = Mock()
        mock_locator.count.side_effect = Exception("Cannot count")
        mock_page.locator.return_value = mock_locator

        with pytest.raises(ElementError, match="Failed to count elements"):
            actions.count_elements(".item")
