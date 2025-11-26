import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Generator

import pytest
from playwright.sync_api import Page
from config.config import Config

logger = logging.getLogger(__name__)
test_results: list[dict[str, Any]] = []


# ============================================================================
# TEST EXECUTION HOOKS
# ============================================================================


@pytest.fixture(autouse=True)
def test_execution_wrapper(
    request: pytest.FixtureRequest,
) -> Generator[None, None, None]:
    test_name = request.node.name
    start_time = datetime.now()

    logger.info(f"[START] {test_name}")

    yield

    duration = (datetime.now() - start_time).total_seconds()

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        logger.error(f"[FAIL] {test_name} - Duration: {duration:.2f}s")
        _handle_test_failure(request, test_name)
    else:
        logger.info(f"[PASS] {test_name} - Duration: {duration:.2f}s")


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
        screenshot_dir = Path("test-results/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = screenshot_dir / f"{test_name}_failure_{timestamp}.png"

        page.screenshot(
            path=str(screenshot_path), full_page=Config.FULL_PAGE_SCREENSHOT
        )

        logger.error(f"Failure screenshot: {screenshot_path}")
        return str(screenshot_path)
    except Exception as e:
        logger.error(f"Failed to take screenshot: {e}")
        return ""


# ============================================================================
# TEST RESULT COLLECTION
# ============================================================================


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[None]
) -> Generator[None, pytest.TestReport, None]:
    outcome = yield
    rep = outcome.get_result()

    setattr(item, "rep_" + rep.when, rep)

    if rep.when in ("call", "setup"):
        test_result = {
            "name": item.name,
            "class": item.cls.__name__ if item.cls else "Function",
            "file": str(item.fspath.basename),  # type: ignore[attr-defined]
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

            from pytest_config.reporting import update_test_case_status_in_sheets

            update_test_case_status_in_sheets(test_result, item)
