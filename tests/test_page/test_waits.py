"""Unit tests for src/Core/page/waits.py"""

from unittest.mock import Mock

from src.Core.page.waits import Waits


class TestWaitForElement:
    """Test wait for element methods."""

    def test_for_element_success(self, mock_page: Mock) -> None:
        """Test wait for element visible."""
        waits = Waits(mock_page)
        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        waits.for_element("#element")

        mock_locator.wait_for.assert_called_once()

    def test_for_element_with_timeout(self, mock_page: Mock) -> None:
        """Test wait for element with custom timeout."""
        waits = Waits(mock_page)
        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        waits.for_element("#element", timeout=10.0)

        mock_locator.wait_for.assert_called_once()

    def test_for_element_visible(self, mock_page: Mock) -> None:
        """Test wait for element visible."""
        waits = Waits(mock_page)
        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        waits.for_element_visible("#element")

        mock_locator.wait_for.assert_called_once()

    def test_for_element_hidden(self, mock_page: Mock) -> None:
        """Test wait for element hidden."""
        waits = Waits(mock_page)
        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        waits.for_element_hidden("#element")

        mock_locator.wait_for.assert_called_once()

    def test_for_element_attached(self, mock_page: Mock) -> None:
        """Test wait for element attached."""
        waits = Waits(mock_page)
        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        waits.for_element_attached("#element")

        mock_locator.wait_for.assert_called_once()

    def test_for_element_detached(self, mock_page: Mock) -> None:
        """Test wait for element detached."""
        waits = Waits(mock_page)
        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator

        waits.for_element_detached("#element")

        mock_locator.wait_for.assert_called_once()


class TestWaitForPage:
    """Test wait for page methods."""

    def test_for_page_load_success(self, mock_page: Mock) -> None:
        """Test wait for page load."""
        waits = Waits(mock_page)

        waits.for_page_load()

        mock_page.wait_for_load_state.assert_called_once()

    def test_for_network_idle_success(self, mock_page: Mock) -> None:
        """Test wait for network idle."""
        waits = Waits(mock_page)

        waits.for_network_idle()

        mock_page.wait_for_load_state.assert_called_once()

    def test_for_dom_ready_success(self, mock_page: Mock) -> None:
        """Test wait for DOM ready."""
        waits = Waits(mock_page)

        waits.for_dom_ready()

        mock_page.wait_for_load_state.assert_called_once()


class TestWaitForSelector:
    """Test wait for selector methods."""

    def test_for_selector_success(self, mock_page: Mock) -> None:
        """Test wait for selector."""
        waits = Waits(mock_page)

        waits.for_selector("#element")

        mock_page.wait_for_selector.assert_called_once()

    def test_for_url_change_success(self, mock_page: Mock) -> None:
        """Test wait for URL change."""
        waits = Waits(mock_page)

        waits.for_url_change("https://example.com")

        mock_page.wait_for_url.assert_called_once()


class TestWaitForFunction:
    """Test wait for function methods."""

    def test_for_function_success(self, mock_page: Mock) -> None:
        """Test wait for function."""
        waits = Waits(mock_page)

        waits.for_function("() => true")

        mock_page.wait_for_function.assert_called_once()

    def test_for_response_success(self, mock_page: Mock) -> None:
        """Test wait for response."""
        waits = Waits(mock_page)

        waits.for_response("/api/data")

        mock_page.wait_for_event.assert_called_once()

    def test_for_request_success(self, mock_page: Mock) -> None:
        """Test wait for request."""
        waits = Waits(mock_page)

        waits.for_request("/api/data")

        mock_page.wait_for_event.assert_called_once()


class TestWaitForTimeout:
    """Test wait for timeout methods."""

    def test_for_timeout_success(self, mock_page: Mock) -> None:
        """Test wait for timeout."""
        waits = Waits(mock_page)

        waits.for_timeout(2.0)

        mock_page.wait_for_timeout.assert_called_once_with(2000)


class TestWaitForElementState:
    """Test wait for element state methods."""

    def test_for_element_enabled_success(self, mock_page: Mock) -> None:
        """Test wait for element enabled."""
        waits = Waits(mock_page)

        waits.for_element_enabled("#element")

        mock_page.wait_for_function.assert_called_once()

    def test_for_element_clickable_success(self, mock_page: Mock) -> None:
        """Test wait for element clickable."""
        waits = Waits(mock_page)
        mock_locator = Mock()
        mock_locator.is_enabled.return_value = True
        mock_page.locator.return_value = mock_locator

        waits.for_element_clickable("#element")

        mock_locator.wait_for.assert_called_once()

    def test_for_text_present_success(self, mock_page: Mock) -> None:
        """Test wait for text present."""
        waits = Waits(mock_page)

        waits.for_text_present("test")

        mock_page.wait_for_function.assert_called_once()


class TestWaitFrameMethods:
    """Test wait for frame methods."""

    def test_for_element_on_frame_success(self, page_with_frames: Mock) -> None:
        """Test wait for element on frame."""
        waits = Waits(page_with_frames)
        mock_frame_locator = Mock()
        mock_element = Mock()
        mock_frame_locator.locator.return_value = mock_element
        page_with_frames.frame_locator.return_value = mock_frame_locator

        waits.for_element_on_frame("//iframe", "#element")

        mock_element.wait_for.assert_called_once()

    def test_for_element_visible_on_frame_success(self, page_with_frames: Mock) -> None:
        """Test wait for element visible on frame."""
        waits = Waits(page_with_frames)
        mock_frame_locator = Mock()
        mock_element = Mock()
        mock_frame_locator.locator.return_value = mock_element
        page_with_frames.frame_locator.return_value = mock_frame_locator

        waits.for_element_visible_on_frame("//iframe", "#element")

        mock_element.wait_for.assert_called_once()

    def test_for_element_hidden_on_frame_success(self, page_with_frames: Mock) -> None:
        """Test wait for element hidden on frame."""
        waits = Waits(page_with_frames)
        mock_frame_locator = Mock()
        mock_element = Mock()
        mock_frame_locator.locator.return_value = mock_element
        page_with_frames.frame_locator.return_value = mock_frame_locator

        waits.for_element_hidden_on_frame("//iframe", "#element")

        mock_element.wait_for.assert_called_once()

    def test_for_element_attached_on_frame_success(
        self, page_with_frames: Mock
    ) -> None:
        """Test wait for element attached on frame."""
        waits = Waits(page_with_frames)
        mock_frame_locator = Mock()
        mock_element = Mock()
        mock_frame_locator.locator.return_value = mock_element
        page_with_frames.frame_locator.return_value = mock_frame_locator

        waits.for_element_attached_on_frame("//iframe", "#element")

        mock_element.wait_for.assert_called_once()

    def test_for_frame_load_success(self, mock_page: Mock) -> None:
        """Test wait for frame load."""
        waits = Waits(mock_page)
        mock_frame = Mock()
        mock_page.frame.return_value = mock_frame

        waits.for_frame_load("frame-name")

        mock_frame.wait_for_load_state.assert_called_once()
