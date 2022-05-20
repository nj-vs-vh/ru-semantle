from aiohttp import web
import logging

from backend.server import create_app
from backend import config

run_kwargs = dict()
if config.IS_PROD:
    run_kwargs["access_log"] = None

logging.basicConfig(level=logging.INFO)
config.log_config()
web.run_app(create_app(), port=config.PORT, **run_kwargs)
