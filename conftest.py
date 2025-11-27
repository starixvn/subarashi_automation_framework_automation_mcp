import logging

from config.config import Config

Config.LOGS_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Config.LOGS_DIR / "automation.log"),
    ],
)
logger = logging.getLogger(__name__)

from pytest_config.config_options import *
from pytest_config.fixtures import *
from pytest_config.hooks import *
from pytest_config.reporting import *
