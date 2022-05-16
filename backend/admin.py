from aiohttp import web

from backend import config


def requires_admin_token(handler):
    async def decorated(request: web.Request) -> web.Response:
        try:
            token = request.headers["token"]
            assert token == config.ADMIN_TOKEN
            return await handler(request)
        except Exception:
            raise web.HTTPUnauthorized(reason="Admin token required")

    return decorated
