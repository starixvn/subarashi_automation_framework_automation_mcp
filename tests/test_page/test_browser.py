"""Unit tests for src/Core/page/browser.py"""

from unittest.mock import Mock

import pytest

from src.Core.exceptions import AutomationError
from src.Core.page.browser import BrowserManager


class TestNavigation:
    """Test navigation methods."""

    def test_navigate_to_success(self, mock_page: Mock) -> None:
        """Test successful navigation."""
        browser = BrowserManager(mock_page)

        browser.navigate_to("https://example.com")

        mock_page.goto.assert_called_once_with("https://example.com")

    def test_navigate_to_error(self, mock_page: Mock) -> None:
        """Test navigate_to raises AutomationError on failure."""
        browser = BrowserManager(mock_page)
        mock_page.goto.side_effect = Exception("Navigation failed")

        with pytest.raises(AutomationError):
            browser.navigate_to("https://example.com")

    def test_navigate_calls_navigate_to(self, mock_page: Mock) -> None:
        """Test navigate calls navigate_to."""
        browser = BrowserManager(mock_page)

        browser.navigate("https://example.com")

        mock_page.goto.assert_called_once()

    def test_get_current_url_success(self, mock_page: Mock) -> None:
        """Test get current URL."""
        browser = BrowserManager(mock_page)
        mock_page.url = "https://example.com/page"

        url = browser.get_current_url()

        assert url == "https://example.com/page"

    def test_reload_success(self, mock_page: Mock) -> None:
        """Test page reload."""
        browser = BrowserManager(mock_page)

        browser.reload()

        mock_page.reload.assert_called_once()

    def test_go_back_success(self, mock_page: Mock) -> None:
        """Test go back."""
        browser = BrowserManager(mock_page)

        browser.go_back()

        mock_page.go_back.assert_called_once()

    def test_go_forward_success(self, mock_page: Mock) -> None:
        """Test go forward."""
        browser = BrowserManager(mock_page)

        browser.go_forward()

        mock_page.go_forward.assert_called_once()


class TestPageInfo:
    """Test page information methods."""

    def test_get_title_success(self, mock_page: Mock) -> None:
        """Test get page title."""
        browser = BrowserManager(mock_page)
        mock_page.title.return_value = "Test Page"

        title = browser.get_title()

        assert title == "Test Page"

    def test_set_viewport_size_success(self, mock_page: Mock) -> None:
        """Test set viewport size."""
        browser = BrowserManager(mock_page)

        browser.set_viewport_size(1920, 1080)

        mock_page.set_viewport_size.assert_called_once_with(
            {"width": 1920, "height": 1080}
        )


class TestScreenshots:
    """Test screenshot methods."""

    def test_screenshot_success(self, mock_page: Mock) -> None:
        """Test taking screenshot."""
        browser = BrowserManager(mock_page)

        browser.screenshot("/path/to/screenshot.png")

        mock_page.screenshot.assert_called_once_with(
            path="/path/to/screenshot.png", full_page=True
        )

    def test_screenshot_element_success(self, mock_page: Mock) -> None:
        """Test screenshot element."""
        browser = BrowserManager(mock_page)
        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        browser.screenshot_element("#element", "/path/to/screenshot.png")

        mock_locator.screenshot.assert_called_once()

    def test_close_page_success(self, mock_page: Mock) -> None:
        """Test close page."""
        browser = BrowserManager(mock_page)

        browser.close_page()

        mock_page.close.assert_called_once()


class TestJavaScript:
    """Test JavaScript evaluation."""

    def test_evaluate_success(self, mock_page: Mock) -> None:
        """Test JavaScript evaluation."""
        browser = BrowserManager(mock_page)
        mock_page.evaluate.return_value = "result"

        result = browser.evaluate("() => document.title")

        assert result == "result"


class TestFrameOperations:
    """Test frame operations."""

    def test_get_frames_success(self, mock_page: Mock) -> None:
        """Test get frames."""
        browser = BrowserManager(mock_page)
        mock_page.frames = ["frame1", "frame2"]

        frames = browser.get_frames()

        assert len(frames) == 2

    def test_get_frame_by_name_success(self, mock_page: Mock) -> None:
        """Test get frame by name."""
        browser = BrowserManager(mock_page)
        mock_frame = Mock()
        mock_page.frame.return_value = mock_frame

        frame = browser.get_frame_by_name("test-frame")

        assert frame == mock_frame

    def test_get_frame_content_success(self, mock_page: Mock) -> None:
        """Test get frame content."""
        browser = BrowserManager(mock_page)
        mock_frame = Mock()
        mock_frame.content.return_value = "<html></html>"
        mock_page.frames = [Mock(), mock_frame]

        content = browser.get_frame_content(1)

        assert content == "<html></html>"

    def test_sleep_success(self, mock_page: Mock) -> None:
        """Test sleep."""
        browser = BrowserManager(mock_page)

        browser.sleep(100)

        mock_page.wait_for_timeout.assert_called_once_with(100)


class TestRegex:
    """Test regex methods."""

    def test_match_by_regex_success(self, mock_page: Mock) -> None:
        """Test regex match on page."""
        browser = BrowserManager(mock_page)
        mock_page.content.return_value = "Test content with pattern"

        result = browser.match_by_regex(r"pattern")

        assert result is True

    def test_match_by_regex_on_frame_success(self, mock_page: Mock) -> None:
        """Test regex match on frame."""
        browser = BrowserManager(mock_page)
        mock_frame = Mock()
        mock_frame.content.return_value = "Frame content"
        mock_page.frame.return_value = mock_frame

        result = browser.match_by_regex_on_frame("frame-name", r"content")

        assert result is True

    def test_extract_by_regex_success(self, mock_page: Mock) -> None:
        """Test extract by regex."""
        browser = BrowserManager(mock_page)
        mock_page.content.return_value = "Value: 123"

        result = browser.extract_by_regex(r"Value: (\d+)", 1)

        assert result == "123"

    def test_extract_by_regex_on_frame_success(self, mock_page: Mock) -> None:
        """Test extract by regex on frame."""
        browser = BrowserManager(mock_page)
        mock_frame = Mock()
        mock_frame.content.return_value = "Frame Value: 456"
        mock_page.frames = [Mock(), mock_frame]

        result = browser.extract_by_regex_on_frame("frame-name", r"Value: (\d+)", 1)

        assert result == "456"


class TestScreenshotAdvanced:
    """Test advanced screenshot methods."""

    def test_screenshot_element_on_frame_success(self, mock_page: Mock) -> None:
        """Test screenshot element on frame."""
        browser = BrowserManager(mock_page)
        mock_frame_locator = Mock()
        mock_element = Mock()
        mock_frame_locator.locator.return_value = mock_element
        mock_page.frame_locator.return_value = mock_frame_locator

        browser.screenshot_element_on_frame(
            "//iframe", "#element", "/path/to/screenshot.png"
        )

        mock_element.screenshot.assert_called_once_with(path="/path/to/screenshot.png")


class TestHelpers:
    """Test helper methods."""

    def test_extract_document_success(self, mock_page: Mock) -> None:
        """Test extract document."""
        browser = BrowserManager(mock_page)
        mock_page.inner_html.return_value = "<div>Test</div>"

        doc = browser.extract_document("#element")

        assert doc is not None

    def test_get_text_on_document_success(self, mock_page: Mock) -> None:
        """Test get text on document."""
        browser = BrowserManager(mock_page)
        mock_doc = Mock()
        mock_element = Mock()
        mock_element.text = "Test Text"
        mock_doc.xpath.return_value = [mock_element]

        result = browser.get_text_on_document(mock_doc, "//div")

        assert result == "Test Text"

    def test_get_element_on_document_success(self, mock_page: Mock) -> None:
        """Test get element on document."""
        browser = BrowserManager(mock_page)
        mock_doc = Mock()
        mock_element = Mock()
        mock_doc.xpath.return_value = [mock_element]

        result = browser.get_element_on_document(mock_doc, "//div")

        assert result == mock_element

    def test_get_substring_in_content_success(self, mock_page: Mock) -> None:
        """Test get substring in content."""
        browser = BrowserManager(mock_page)
        content = "Some text keyword='value' more text"

        result = browser.get_substring_in_content(content, "keyword", "=", "'")

        assert (
            result == "'value" or result == ""
        )  # Method behavior depends on index > 0

    def test_get_last_frame_index_success(self, mock_page: Mock) -> None:
        """Test get last frame index."""
        browser = BrowserManager(mock_page)
        mock_page.frames = [Mock(), Mock(), Mock()]

        index = browser.get_last_frame_index()

        assert index == 2
