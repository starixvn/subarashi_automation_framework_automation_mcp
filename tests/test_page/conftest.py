"""Pytest fixtures specific to page module tests."""

from unittest.mock import Mock

import pytest


@pytest.fixture
def page_with_elements(mock_page: Mock) -> Mock:
    """Create a mock page with common elements."""

    # Configure locator behavior
    def locator_side_effect(selector: str) -> Mock:
        loc = Mock()
        loc.is_visible.return_value = True
        loc.is_enabled.return_value = True
        loc.is_checked.return_value = False
        loc.is_editable.return_value = True
        loc.count.return_value = 1
        loc.text_content.return_value = f"Text for {selector}"
        loc.inner_text.return_value = f"Inner text for {selector}"
        loc.get_attribute.return_value = "test-value"
        loc.input_value.return_value = "input-value"
        return loc

    mock_page.locator.side_effect = locator_side_effect
    return mock_page


@pytest.fixture
def page_with_frames(mock_page: Mock, mock_frame: Mock) -> Mock:
    """Create a mock page with frames."""
    mock_page.frames = [mock_page, mock_frame, mock_frame]

    # Configure frame_locator
    frame_loc = Mock()
    frame_loc.locator.return_value = Mock()
    mock_page.frame_locator.return_value = frame_loc

    return mock_page
