import os
import logging

logger = logging.getLogger(__name__)


REDIS_URL = os.environ["REDIS_URL"]
PORT = int(os.environ.get("PORT", 8088))
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "dummy")
IS_PROD = ADMIN_TOKEN != "dummy"


def log_config():

    def mask_secret(v: str) -> str:
        open_symbols = len(v) // 2
        return v[:open_symbols] + "*" * (len(v) - open_symbols)

    logger.info(f"REDIS_URL = {mask_secret(REDIS_URL)}")
    logger.info(f"ADMIN_TOKEN = {mask_secret(ADMIN_TOKEN)}")
    logger.info(f"{PORT = }")
    logger.info(f"{IS_PROD = }")
