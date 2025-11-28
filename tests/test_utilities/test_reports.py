"""Unit tests for src/Core/utilities/reports.py"""

from unittest.mock import Mock, patch

import pytest

from src.Core.exceptions import AutomationError
from src.Core.utilities.reports import Reports


class TestPrepareTestMessage:
    """Test prepare_test_message method."""

    def test_prepare_test_message_passed(self) -> None:
        """Test prepare message for passed tests."""
        reports = Reports()

        message = reports.prepare_test_message("TestFunction", "UAT")

        assert "TestFunction" in message
        assert "UAT" in message
        assert "PASSED" in message

    def test_prepare_test_message_failed(self) -> None:
        """Test prepare message for failed tests."""
        reports = Reports()

        message = reports.prepare_test_message(
            "TestFunction", "UAT", ["TestCase_001", "TestCase_002"]
        )

        assert "TestFunction" in message
        assert "FAILED" in message
        assert "TestCase 001" in message


class TestSendTelegramMessage:
    """Test send_telegram_message method."""

    @patch("src.Core.utilities.reports.requests.post")
    def test_send_telegram_message_success(self, mock_post: Mock) -> None:
        """Test send Telegram message."""
        reports = Reports()

        reports.send_telegram_message("Test message", "bot_token", ["chat_id"])

        mock_post.assert_called_once()

    def test_send_telegram_message_no_token(self) -> None:
        """Test send Telegram with no token."""
        reports = Reports()

        reports.send_telegram_message("Test", "", ["chat_id"])


class TestSendTeamsMessage:
    """Test send_teams_message method."""

    @patch("src.Core.utilities.reports.requests.post")
    def test_send_teams_message_success(self, mock_post: Mock) -> None:
        """Test send Teams message."""
        reports = Reports()

        reports.send_teams_message("Test message", ["conv_id"])

        mock_post.assert_called_once()


class TestSendSlackMessage:
    """Test send_message_to_slack method."""

    @patch("src.Core.utilities.reports.WebClient")
    @patch("src.Core.utilities.reports.Config")
    def test_send_slack_message_success(
        self, mock_config: Mock, mock_client_class: Mock
    ) -> None:
        """Test send Slack message."""
        mock_config.SLACK_BOT_TOKEN = "xoxb-token"
        mock_config.SLACK_CHANNEL_ID = "C123"
        mock_client = Mock()
        mock_client.chat_postMessage.return_value = {"ok": True, "ts": "123"}
        mock_client_class.return_value = mock_client

        reports = Reports()
        reports.send_message_to_slack("Test message")

        mock_client.chat_postMessage.assert_called_once()

    @patch("src.Core.utilities.reports.Config")
    def test_send_slack_message_no_token(self, mock_config: Mock) -> None:
        """Test send Slack with no token."""
        mock_config.SLACK_BOT_TOKEN = ""
        mock_config.SLACK_CHANNEL_ID = "C123"

        reports = Reports()
        reports.send_message_to_slack("Test")


class TestAddScreenshot:
    """Test add_screenshot method."""

    def test_add_screenshot_success(self, temp_test_file: Mock) -> None:
        """Test add screenshot to report."""
        reports = Reports()

        with patch("src.Core.utilities.reports.Files.file_exists", return_value=True):
            with patch("builtins.open", create=True):
                result = reports.add_screenshot(str(temp_test_file), "test_case")
                assert isinstance(result, str)

    def test_add_screenshot_file_not_found(self) -> None:
        """Test add screenshot with file not found."""
        reports = Reports()

        with pytest.raises(AutomationError, match="not found"):
            reports.add_screenshot("/nonexistent.png", "test")


class TestLogTestFailure:
    """Test log_test_failure static method."""

    @patch("src.Core.utilities.reports.Files.create_directory")
    def test_log_test_failure_success(self, mock_create_dir: Mock) -> None:
        """Test log test failure."""
        with patch("builtins.open", create=True):
            Reports.log_test_failure("TestCase_001", "Assertion failed")
