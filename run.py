from aiohttp import web
import logging

from backend.server import create_app
from backend import config

logging.basicConfig(level=logging.INFO)
config.log_config()
web.run_app(create_app(), port=config.PORT)
