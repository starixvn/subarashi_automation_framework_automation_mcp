import logging
import pytest
from config.config import Config

logger = logging.getLogger(__name__)


# ============================================================================
# COMMAND LINE OPTIONS
# ============================================================================


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--env", default=None, help="Environment: local, uat, prod")
    parser.addoption("--site", default=None, help="Site: lrf, lap")
    parser.addoption("--headless", default=None, help="Headless mode: true, false")


def pytest_configure(config: pytest.Config) -> None:
    env_option = config.getoption("--env")
    if env_option is not None:
        Config.ENVIRONMENT = env_option

    site_option = config.getoption("--site")
    if site_option is not None:
        Config.SITE = site_option

    headless_option = config.getoption("--headless")
    if headless_option is not None:
        Config.HEADLESS = headless_option.lower() == "true"

    logger.info(
        f"Pytest configuration completed - ENV: {Config.ENVIRONMENT}, SITE: {Config.SITE}, HEADLESS: {Config.HEADLESS}"
    )
