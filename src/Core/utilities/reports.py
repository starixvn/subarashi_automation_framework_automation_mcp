import os
import json
import logging
import requests
import ssl
from typing import List
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from src.Core import auto_log, AutomationError
from .files import Files
from .google_sheets import GoogleSheets
from datetime import datetime
from config.config import Config

logger = logging.getLogger(__name__)


class Reports:
    def __init__(self, output_dir: str = "test-results/reports"):
        self.output_dir = output_dir
        Files.create_directory(output_dir)

    @auto_log
    def prepare_test_message(
        self, function_name: str, env: str, failed_cases: List[str] = None
    ) -> str:
        try:
            if failed_cases:
                message = f"[Auto] - [{function_name}] - [{env}] - [FAILED]"
                for case in list(dict.fromkeys(failed_cases)):
                    message += f"\n- {str(case).replace('_', ' ')} - [FAILED]"
                return message
            else:
                return f"[Auto] - [{function_name}] - [{env}] - [PASSED]"
        except Exception as e:
            raise AutomationError("Failed to prepare test message", str(e)) from e

    @auto_log
    def send_telegram_message(
        self, message: str, bot_token: str, chat_ids: List[str]
    ) -> None:
        try:
            if not bot_token:
                return

            for chat_id in chat_ids:
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                payload = {
                    "chat_id": chat_id,
                    "parse_mode": "Markdown",
                    "text": message,
                }
                requests.post(url=url, data=payload)
        except Exception as e:
            raise AutomationError("Failed to send Telegram message", str(e)) from e

    @auto_log
    def send_tracelog_to_telegram(
        self, message: str, bot_token: str, chat_ids: List[str]
    ) -> None:
        try:
            if not bot_token:
                return

            for chat_id in chat_ids:
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                payload = {
                    "chat_id": chat_id,
                    "parse_mode": "Markdown",
                    "text": message,
                }
                requests.post(url=url, data=payload)
        except Exception as e:
            raise AutomationError("Failed to send trace log to Telegram", str(e)) from e

    @auto_log
    def send_teams_message(self, message: str, conversation_ids: List[str]) -> None:
        try:
            if not conversation_ids:
                return

            url = "https://api-fanexbot.nexdev.net/api/msteams/send"
            headers = {"Content-Type": "application/json"}

            for conv_id in conversation_ids:
                payload = {"appId": 1021, "conversationId": conv_id, "Content": message}
                requests.post(url=url, headers=headers, data=json.dumps(payload))
        except Exception as e:
            raise AutomationError("Failed to send Teams message", str(e)) from e

    @auto_log
    def send_message_to_slack(self, message: str) -> None:
        try:
            if not Config.SLACK_BOT_TOKEN:
                logger.warning(
                    "SLACK_BOT_TOKEN not configured, skipping Slack notification"
                )
                return

            if not Config.SLACK_CHANNEL_ID:
                logger.warning(
                    "SLACK_CHANNEL_ID not configured, skipping Slack notification"
                )
                return

            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            client = WebClient(token=Config.SLACK_BOT_TOKEN, ssl=ssl_context)

            response = client.chat_postMessage(
                channel=Config.SLACK_CHANNEL_ID,
                text=message,
                parse="full",
                unfurl_links=True,
                unfurl_media=True,
            )

            if response["ok"]:
                logger.info(
                    f"Successfully sent Slack message to channel {Config.SLACK_CHANNEL_ID}"
                )
                logger.info(f"   Message timestamp: {response.get('ts', 'N/A')}")
            else:
                error_msg = response.get("error", "Unknown error")
                logger.error(f"Slack API error: {error_msg}")
                raise AutomationError(f"Slack API returned error: {error_msg}")

        except SlackApiError as e:
            error_details = e.response.get("error", "Unknown Slack API error")
            logger.error(f"Slack API error: {error_details}")
            logger.warning(
                "Continuing test execution despite Slack notification failure"
            )

        except Exception as e:
            logger.error(f"Failed to send Slack message: {str(e)}")
            logger.warning(
                "Continuing test execution despite Slack notification failure"
            )

    @auto_log
    def log_test_result_to_sheet(
        self, spreadsheet_id: str, message: str, run_from: str = "Jenkins"
    ) -> None:
        try:
            sheets = GoogleSheets()
            sheet_name = "Result"
            data_list = [f"{message} - {run_from}"]

            sheets.append_values(spreadsheet_id, sheet_name, [data_list])
        except Exception as e:
            raise AutomationError("Failed to log test result to sheet", str(e)) from e

    @auto_log
    def add_screenshot(self, screenshot_path: str, test_name: str) -> str:
        try:
            if not Files.file_exists(screenshot_path):
                raise AutomationError(f"Screenshot file not found: {screenshot_path}")

            screenshots_dir = os.path.join(self.output_dir, "screenshots")
            Files.create_directory(screenshots_dir)

            new_filename = f"{test_name}.png"
            new_path = os.path.join(screenshots_dir, new_filename)

            with open(screenshot_path, "rb") as src, open(new_path, "wb") as dst:
                dst.write(src.read())

            return new_path
        except Exception as e:
            raise AutomationError("Failed to add screenshot to report", str(e)) from e

    @staticmethod
    @auto_log
    def log_test_failure(test_name: str, error_message: str) -> None:
        try:
            logger = logging.getLogger(__name__)
            logger.error(f"TEST FAILURE - {test_name}: {error_message}")

            failure_dir = "test-results/failures"
            Files.create_directory(failure_dir)

            failure_file = os.path.join(failure_dir, f"{test_name}_failure.log")
            with open(failure_file, "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {test_name}: {error_message}\n")

        except Exception as e:
            logging.getLogger(__name__).warning(f"Failed to log test failure: {e}")
