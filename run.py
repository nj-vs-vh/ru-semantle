from aiohttp import web
from backend.server import create_app
from backend import config


web.run_app(create_app(), port=config.PORT)
