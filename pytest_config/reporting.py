import logging
import re
from datetime import datetime
from typing import Any, Generator, Optional

import pytest
from config.config import Config
from src.Core.utilities import GoogleSheets, Reports

logger = logging.getLogger(__name__)


# ============================================================================
# SESSION NOTIFICATIONS
# ============================================================================


@pytest.fixture(scope="session", autouse=True)
def session_notifications() -> Generator[None, None, None]:
    yield

    from pytest_config.hooks import test_results

    if not test_results:
        logger.warning("No test results to send notifications")
        return

    total_tests = len(test_results)
    passed = sum(1 for test in test_results if test["status"] == "passed")
    failed = sum(1 for test in test_results if test["status"] == "failed")
    pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
    execution_time = sum(test.get("duration", 0) for test in test_results)
    try:
        _send_notifications(total_tests, passed, failed, pass_rate, execution_time)
    except Exception as e:
        logger.error(f"Failed to send notifications: {e}")


def _send_notifications(
    total: int, passed: int, failed: int, pass_rate: float, duration: float
) -> None:
    try:
        logger.info("Sending test notifications...")
        reports = Reports()
        message = _create_detailed_report_message(
            total, passed, failed, pass_rate, duration
        )
        if hasattr(Config, "TELEGRAM_BOT_TOKEN") and hasattr(
            Config, "TELEGRAM_CHAT_IDS"
        ):
            if Config.TELEGRAM_BOT_TOKEN and Config.TELEGRAM_CHAT_IDS:
                reports.send_telegram_message(
                    message, Config.TELEGRAM_BOT_TOKEN, Config.TELEGRAM_CHAT_IDS
                )
                logger.info("Telegram notification sent")

        if hasattr(Config, "TEAMS_CONVERSATION_IDS") and Config.TEAMS_CONVERSATION_IDS:
            reports.send_teams_message(message, Config.TEAMS_CONVERSATION_IDS)
            logger.info("Teams notification sent")

        if hasattr(Config, "SLACK_BOT_TOKEN") and hasattr(Config, "SLACK_CHANNEL_ID"):
            if Config.SLACK_BOT_TOKEN and Config.SLACK_CHANNEL_ID:
                reports.send_message_to_slack(message)
                logger.info("Slack notification sent")
            else:
                logger.info("Slack credentials not configured, skipping notification")
        else:
            logger.info("Slack configuration missing, skipping notification")

    except Exception as e:
        logger.error(f"Failed to send notifications: {e}")


def _create_detailed_report_message(
    total: int, passed: int, failed: int, pass_rate: float, duration: float
) -> str:
    from pytest_config.hooks import test_results

    suite_name = "Unknown"
    if test_results:
        suite_name = test_results[0]["file"].replace(".py", "").replace("_", " ")

    if failed == 0:
        status = "PASSED"
        emoji = "✅"
    else:
        status = "FAILED"
        emoji = "❌"

    # format message: [SITE] - [ENV] - [TESTSUITES_NAME] - [STATUS + EMOJI] - [DURATION]
    message = f"[{Config.SITE.upper()}] - [{Config.ENVIRONMENT.upper()}] - [{suite_name}] - [{status} {emoji}] - [{duration:.1f}s]"

    return message


# ============================================================================
# GOOGLE SHEETS INTEGRATION
# ============================================================================


def update_test_case_status_in_sheets(
    test_result: dict[str, Any], test_item: Optional[pytest.Item] = None
) -> None:
    if not getattr(Config, "GOOGLE_SHEETS_ENABLED", False) or not getattr(
        Config, "GOOGLE_SHEETS_ID", None
    ):
        return

    try:
        sheets = GoogleSheets()
        test_name = test_result["name"]
        test_status = test_result["status"].upper()  # PASSED, FAILED, SKIPPED
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tc_id = None
        if test_item:
            tc_id_marker = test_item.get_closest_marker("tc_id")
            if tc_id_marker and tc_id_marker.args:
                tc_id = tc_id_marker.args[0]

        formatted_test_name = test_name.replace("TestCase_", "").replace("_", " ")
        formatted_test_name = re.sub(r"^\d+\s+", "", formatted_test_name)

        sheet_name = "TestCases"  # Default fallback

        if test_item and test_item.cls:
            sheet_name = getattr(test_item.cls, "TEST_CASE_SHEET_NAME", sheet_name)

        elif test_item and hasattr(test_item, "instance") and test_item.instance:
            sheet_name = getattr(test_item.instance, "TEST_CASE_SHEET_NAME", sheet_name)

        logger.info(
            f"Updating test case status: TC_ID={tc_id} | Name={formatted_test_name} -> {test_status} (Sheet: {sheet_name})"
        )
        values = sheets.get_sheet_values(Config.GOOGLE_SHEETS_ID, sheet_name)

        if not values or len(values) < 2:
            logger.warning(f"No test case data found in sheet: {sheet_name}")
            return

        header_row = values[0]
        tc_id_col_index = -1
        auto_status_col_index = -1
        duration_col_index = -1
        last_run_time_col_index = -1
        last_env_col_index = -1

        for i, header in enumerate(header_row):
            header_lower = str(header).strip().lower()
            if header_lower == "tc_id":
                tc_id_col_index = i
            elif header_lower == "auto_status":
                auto_status_col_index = i
            elif header_lower == "duration":
                duration_col_index = i
            elif header_lower == "last_run_time":
                last_run_time_col_index = i
            elif header_lower == "last_env":
                last_env_col_index = i

        if auto_status_col_index == -1:
            logger.error("Auto_Status column not found in Google Sheet")
            return

        matching_row = None

        if tc_id and tc_id_col_index != -1:
            logger.info(f"Searching by TC_ID: {tc_id}")
            for row_idx, row_data in enumerate(values[1:], start=2):
                if len(row_data) > tc_id_col_index:
                    sheet_tc_id = str(row_data[tc_id_col_index]).strip()
                    if sheet_tc_id.lower() == tc_id.lower():
                        matching_row = row_idx
                        logger.info(
                            f"Found match by TC_ID: {tc_id} -> Row {matching_row}"
                        )
                        break
        else:
            logger.warning(
                f"No TC_ID marker found or TC_ID column missing for test: {test_name}"
            )

        if matching_row is None:
            if tc_id:
                logger.warning(f"TC_ID '{tc_id}' not found in Google Sheet")
            else:
                logger.warning(
                    f"Test '{test_name}' has no TC_ID marker - skipping Google Sheets update"
                )
            return

        columns_to_update = []

        if auto_status_col_index != -1:
            columns_to_update.append(
                {
                    "column_index": auto_status_col_index,
                    "value": test_status,
                    "column_name": "Auto_Status",
                }
            )

        if duration_col_index != -1:
            duration_value = f"{test_result['duration']:.2f}s"
            columns_to_update.append(
                {
                    "column_index": duration_col_index,
                    "value": duration_value,
                    "column_name": "Duration",
                }
            )

        if last_run_time_col_index != -1:
            columns_to_update.append(
                {
                    "column_index": last_run_time_col_index,
                    "value": timestamp,
                    "column_name": "Last_Run_Time",
                }
            )

        if last_env_col_index != -1:
            columns_to_update.append(
                {
                    "column_index": last_env_col_index,
                    "value": test_result["environment"].upper(),
                    "column_name": "Last_Env",
                }
            )

        update_summary = []
        for col_info in columns_to_update:
            try:
                column_letter = chr(65 + col_info["column_index"])
                cell_range = f"{column_letter}{matching_row}"

                sheets.update_sheet_values(
                    Config.GOOGLE_SHEETS_ID,
                    sheet_name,
                    [[col_info["value"]]],
                    cell_range,
                )

                update_summary.append(f"{col_info['column_name']}: {col_info['value']}")

            except Exception as col_error:
                logger.warning(
                    f"Failed to update {col_info['column_name']} column: {col_error}"
                )

        if update_summary:
            logger.info(f"Updated {formatted_test_name}: {' | '.join(update_summary)}")

    except Exception as e:
        logger.warning(f"Failed to update test case data in Google Sheets: {e}")
