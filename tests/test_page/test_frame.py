"""
Unit tests for src/Core/page/frame.py

Tests the Frame class and its _get_frame_element method for handling
various frame scenarios including direct page, frame locators, child frames,
and latest frames.
"""

from unittest.mock import Mock

from src.Core.page.frame import Frame


class TestFrame:
    """Test Frame class functionality."""

    def test_direct_page_locator_empty_frame_xpath(self, mock_page: Mock) -> None:
        """Test direct page locator when frame_xpath is empty."""
        frame = Frame(mock_page)
        selector = "#test-element"

        result = frame._get_frame_element("", selector)

        mock_page.locator.assert_called_once_with(selector)
        assert result == mock_page.locator.return_value

    def test_direct_page_locator_no_indices(self, mock_page: Mock) -> None:
        """Test direct page locator when no indices are provided."""
        frame = Frame(mock_page)
        selector = ".test-class"

        frame._get_frame_element("", selector, None, None)

        mock_page.locator.assert_called_once_with(selector)

    def test_frame_locator_with_xpath(self, mock_page: Mock) -> None:
        """Test frame locator when frame_xpath is provided."""
        frame = Frame(mock_page)
        frame_xpath = "//iframe[@id='test-frame']"
        selector = "#element"

        # Mock frame_locator
        mock_frame_locator = Mock()
        mock_locator = Mock()
        mock_frame_locator.locator.return_value = mock_locator
        mock_page.frame_locator.return_value = mock_frame_locator

        result = frame._get_frame_element(frame_xpath, selector)

        mock_page.frame_locator.assert_called_once_with(frame_xpath)
        mock_frame_locator.locator.assert_called_once_with(selector)
        assert result == mock_locator

    def test_frame_locator_with_xpath_no_indices(self, mock_page: Mock) -> None:
        """Test frame locator with xpath and no indices."""
        frame = Frame(mock_page)
        frame_xpath = "iframe[name='content']"
        selector = "button"

        mock_frame_locator = Mock()
        mock_page.frame_locator.return_value = mock_frame_locator

        frame._get_frame_element(frame_xpath, selector, None, None)

        mock_page.frame_locator.assert_called_with(frame_xpath)

    def test_child_frame_by_index(self, mock_page: Mock) -> None:
        """Test child frame access by index."""
        frame = Frame(mock_page)
        selector = "#test"

        # Setup mock frames
        main_frame = Mock()
        child_frame_1 = Mock()
        child_frame_2 = Mock()
        child_locator = Mock()

        child_frame_2.locator.return_value = child_locator
        main_frame.child_frames = [child_frame_1, child_frame_2]
        mock_page.frames = [mock_page, main_frame]

        result = frame._get_frame_element("", selector, idx_child_frame=1)

        child_frame_2.locator.assert_called_once_with(selector)
        assert result == child_locator

    def test_child_frame_index_zero(self, mock_page: Mock) -> None:
        """Test child frame with index 0."""
        frame = Frame(mock_page)

        child_frame = Mock()
        child_locator = Mock()
        child_frame.locator.return_value = child_locator

        main_frame = Mock()
        main_frame.child_frames = [child_frame]
        mock_page.frames = [mock_page, main_frame]

        result = frame._get_frame_element("", "#test", idx_child_frame=0)

        assert result == child_locator

    def test_latest_frame_by_index(self, mock_page: Mock) -> None:
        """Test latest frame access by index."""
        frame = Frame(mock_page)
        selector = ".element"

        # Setup mock frames list
        frame1 = Mock()
        frame2 = Mock()
        frame3 = Mock()
        target_locator = Mock()

        frame2.locator.return_value = target_locator
        mock_page.frames = [frame1, frame2, frame3]

        result = frame._get_frame_element("", selector, None, idx_latest_frame=1)

        frame2.locator.assert_called_once_with(selector)
        assert result == target_locator

    def test_latest_frame_last_index(self, mock_page: Mock) -> None:
        """Test accessing last frame in frames list."""
        frame = Frame(mock_page)

        frame1 = Mock()
        frame2 = Mock()
        last_locator = Mock()
        frame2.locator.return_value = last_locator

        mock_page.frames = [frame1, frame2]

        result = frame._get_frame_element("", "#last", None, idx_latest_frame=1)

        assert result == last_locator

    def test_fallback_to_page_locator(self, mock_page: Mock) -> None:
        """Test fallback to page locator when conditions don't match."""
        frame = Frame(mock_page)
        selector = "#fallback"

        # This shouldn't happen in practice but tests the fallback
        frame._get_frame_element("", selector)

        mock_page.locator.assert_called_with(selector)

    def test_empty_selector(self, mock_page: Mock) -> None:
        """Test with empty selector string."""
        frame = Frame(mock_page)

        frame._get_frame_element("", "")

        mock_page.locator.assert_called_with("")

    def test_xpath_selector(self, mock_page: Mock) -> None:
        """Test with XPath selector."""
        frame = Frame(mock_page)
        xpath = "//div[@class='test']"

        frame._get_frame_element("", xpath)

        mock_page.locator.assert_called_with(xpath)

    def test_css_selector(self, mock_page: Mock) -> None:
        """Test with CSS selector."""
        frame = Frame(mock_page)
        css = "div.container > p#main"

        frame._get_frame_element("", css)

        mock_page.locator.assert_called_with(css)

    def test_text_selector(self, mock_page: Mock) -> None:
        """Test with text selector."""
        frame = Frame(mock_page)
        text_sel = "text=Click Me"

        frame._get_frame_element("", text_sel)

        mock_page.locator.assert_called_with(text_sel)

    def test_multiple_frames_on_page(self, mock_page: Mock) -> None:
        """Test with multiple frames on page."""
        frame = Frame(mock_page)

        # Create multiple frames
        frames = [Mock() for _ in range(5)]
        mock_page.frames = frames

        target_locator = Mock()
        frames[3].locator.return_value = target_locator

        result = frame._get_frame_element("", "#test", None, idx_latest_frame=3)

        assert result == target_locator

    def test_nested_frames(self, mock_page: Mock) -> None:
        """Test with nested frame structure."""
        frame = Frame(mock_page)

        # Parent frame with child frames
        parent_frame = Mock()
        child_frame = Mock()
        nested_locator = Mock()

        child_frame.locator.return_value = nested_locator
        parent_frame.child_frames = [child_frame]
        mock_page.frames = [mock_page, parent_frame]

        result = frame._get_frame_element("", "#nested", idx_child_frame=0)

        assert result == nested_locator

    def test_frame_with_none_parameters(self, mock_page: Mock) -> None:
        """Test with explicitly None parameters."""
        frame = Frame(mock_page)

        frame._get_frame_element("", "#test", None, None)

        mock_page.locator.assert_called_with("#test")

    def test_invalid_frame_xpath_empty(self, mock_page: Mock) -> None:
        """Test with empty frame xpath falls back to page."""
        frame = Frame(mock_page)

        frame._get_frame_element("", "#element", None, None)

        mock_page.locator.assert_called_with("#element")

    def test_frame_element_return_type(self, mock_page: Mock) -> None:
        """Test return type is Locator."""
        frame = Frame(mock_page)

        result = frame._get_frame_element("", "#test")

        # Should return what locator() returns
        assert result is not None

    def test_case_1_direct_page(self, mock_page: Mock) -> None:
        """Test Case 1: Direct page locator (empty xpath, no indices)."""
        frame = Frame(mock_page)

        frame._get_frame_element("", "#element", None, None)

        mock_page.locator.assert_called_once()

    def test_case_2_frame_locator(self, mock_page: Mock) -> None:
        """Test Case 2: Frame locator (xpath provided, no indices)."""
        frame = Frame(mock_page)

        mock_frame_loc = Mock()
        mock_page.frame_locator.return_value = mock_frame_loc

        frame._get_frame_element("//iframe", "#element", None, None)

        mock_page.frame_locator.assert_called_once()

    def test_case_3_child_frame(self, mock_page: Mock) -> None:
        """Test Case 3: Child frame by index (idx_child_frame set)."""
        frame = Frame(mock_page)

        child = Mock()
        parent = Mock()
        parent.child_frames = [child]
        mock_page.frames = [mock_page, parent]

        frame._get_frame_element(
            "", "#element", idx_child_frame=0, idx_latest_frame=None
        )

        child.locator.assert_called_once()

    def test_case_4_latest_frame(self, mock_page: Mock) -> None:
        """Test Case 4: Latest frame by index (idx_latest_frame set)."""
        frame = Frame(mock_page)

        frame1 = Mock()
        frame2 = Mock()
        mock_page.frames = [frame1, frame2]

        frame._get_frame_element("", "#element", None, idx_latest_frame=1)

        frame2.locator.assert_called_once()

    def test_frame_initialization(self, mock_page: Mock) -> None:
        """Test Frame class initialization."""
        frame = Frame(mock_page)

        assert frame.page == mock_page
        assert hasattr(frame, "_get_frame_element")
