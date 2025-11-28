import logging
import allure
from datetime import datetime
from typing import Any, Generator

import pytest
from playwright.sync_api import Page
from config.config import Config

logger = logging.getLogger(__name__)
test_results: list[dict[str, Any]] = []


@pytest.fixture(autouse=True)
def test_execution_wrapper(
    request: pytest.FixtureRequest,
) -> Generator[None, None, None]:
    test_name = request.node.name
    start_time = datetime.now()

    yield

    duration = (datetime.now() - start_time).total_seconds()

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        logger.error(f"[FAIL] {test_name} - Duration: {duration:.2f}s")
        _handle_test_failure(request, test_name)


def _handle_test_failure(request: pytest.FixtureRequest, test_name: str) -> None:
    if not Config.SCREENSHOT_ON_FAILURE:
        return

    try:
        page = None
        for fixture_name in request.fixturenames:
            if fixture_name == "page":
                page = request.getfixturevalue("page")
                break

        if page:
            _take_failure_screenshot(page, test_name)
    except Exception as e:
        logger.error(f"Failed to handle test failure for {test_name}: {e}")


def _take_failure_screenshot(page: Page, test_name: str) -> str:
    try:
        Config.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = (
            Config.SCREENSHOTS_DIR / f"{test_name}_failure_{timestamp}.png"
        )

        page.screenshot(
            path=str(screenshot_path), full_page=Config.FULL_PAGE_SCREENSHOT
        )

        if Config.ALLURE_ENABLED:
            try:
                with open(screenshot_path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name=f"Screenshot: {test_name}",
                        attachment_type=allure.attachment_type.PNG,
                    )

                page_html = page.content()
                allure.attach(
                    page_html,
                    name=f"Page HTML: {test_name}",
                    attachment_type=allure.attachment_type.HTML,
                )

                page_url = page.url
                allure.attach(
                    page_url,
                    name="Page URL",
                    attachment_type=allure.attachment_type.URI_LIST,
                )
            except ImportError:
                logger.warning("Allure enabled but not installed")

        return str(screenshot_path)
    except Exception as e:
        logger.error(f"Failed to take screenshot: {e}")
        return ""


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[None]
) -> Generator[None, pytest.TestReport, None]:
    outcome = yield
    rep = outcome.get_result()

    setattr(item, "rep_" + rep.when, rep)

    if Config.ALLURE_ENABLED and rep.when == "call":
        try:
            import allure

            if hasattr(item, "cls") and item.cls:
                allure.dynamic.feature(item.cls.__name__)

            tc_marker = item.get_closest_marker("tc_id")
            if tc_marker:
                tc_id = tc_marker.args[0] if tc_marker.args else "Unknown"
                allure.dynamic.label("tc_id", tc_id)
                allure.dynamic.link(
                    f"https://docs.google.com/spreadsheets/d/{Config.GOOGLE_SHEETS_ID}",
                    name=f"Test Case: {tc_id}",
                )

            allure.dynamic.parameter("Environment", Config.ENVIRONMENT)
            allure.dynamic.parameter("Site", Config.SITE)
            allure.dynamic.parameter("Headless", Config.HEADLESS)
        except ImportError:
            logger.warning("Allure enabled but not installed")

    if rep.when in ("call", "setup"):
        test_result = {
            "name": item.name,
            "class": item.cls.__name__ if item.cls else "Function",
            "file": str(item.fspath.basename),
            "status": "passed" if rep.passed else "failed" if rep.failed else "skipped",
            "duration": rep.duration,
            "timestamp": datetime.now().isoformat(),
            "error": str(rep.longrepr) if rep.failed else None,
            "environment": Config.ENVIRONMENT,
            "site": Config.SITE,
            "phase": rep.when,
        }

        if rep.when == "call" or (rep.when == "setup" and rep.failed):
            test_results.append(test_result)
            tc_marker = item.get_closest_marker("tc_id")
            if tc_marker and Config.GOOGLE_SHEETS_ENABLED:
                from pytest_config.reporting import update_test_case_status_in_sheets

                update_test_case_status_in_sheets(test_result, item)
