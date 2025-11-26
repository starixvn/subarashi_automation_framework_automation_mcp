import logging
from pathlib import Path

logs_dir = Path("test-results/logs")
logs_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(logs_dir / "automation.log"),
    ],
)
logger = logging.getLogger(__name__)

from pytest_config.fixtures import *  # noqa: F401, F403
from pytest_config.hooks import *  # noqa: F401, F403
from pytest_config.reporting import *  # noqa: F401, F403
from pytest_config.config_options import *  # noqa: F401, F403
