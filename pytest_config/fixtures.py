import logging
from pathlib import Path
from typing import Generator, Any

import pytest
from playwright.sync_api import Page
from config.config import Config
from src.Action.action_common import ActionCommon

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def browser_type_launch_args(
    browser_type_launch_args: dict[str, Any],
) -> dict[str, Any]:
    base_args = ["--no-sandbox", "--disable-dev-shm-usage"]

    if not Config.HEADLESS:
        base_args.extend(
            [
                "--start-maximized",
                f"--window-size={Config.VIEWPORT_WIDTH},{Config.VIEWPORT_HEIGHT}",
                "--window-position=0,0",
            ]
        )

    return {
        **browser_type_launch_args,
        "headless": Config.HEADLESS,
        "args": base_args,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict[str, Any]) -> dict[str, Any]:
    viewport_config = {"width": Config.VIEWPORT_WIDTH, "height": Config.VIEWPORT_HEIGHT}
    base_url = Config.URLS[Config.SITE][Config.ENVIRONMENT]["url"]

    return {
        **browser_context_args,
        "viewport": viewport_config,
        "screen": viewport_config,
        "ignore_https_errors": True,
        "accept_downloads": True,
        "base_url": base_url,
    }


@pytest.fixture(autouse=True)
def auto_login(page: Page) -> Generator[None, None, None]:
    action = ActionCommon(page)
    action.login()
    yield


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment() -> Generator[None, None, None]:
    logger.info("Setting up test environment")
    for directory in [
        "test-results/screenshots",
        "test-results/reports",
        "test-results/logs",
        "test-results/failures",
    ]:
        Path(directory).mkdir(parents=True, exist_ok=True)
    logger.info(
        f"Environment: {Config.ENVIRONMENT} | Site: {Config.SITE} | Headless: {Config.HEADLESS}"
    )

    yield

    logger.info("Test environment cleanup completed")
