import asyncio
from typing import TypedDict
from aiohttp import web
from redis import Redis

from backend.dependencies import get_navec_model
from backend.game.types import Word
from backend.game.storage import GameStorage
from backend import config


class AppExtensions(TypedDict):
    storage: GameStorage


class Application(web.Application, AppExtensions):
    pass


def create_app() -> Application:
    app: Application = web.Application(client_max_size=512)

    async def init_game_storage(app: Application):
        redis = Redis.from_url(config.REDIS_URL)
        game_storage = GameStorage(redis)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(game_storage.daily_game_update())
        app["storage"] = game_storage

    app.on_startup.append(init_game_storage)

    async def guess(request: web.Request) -> web.Response:
        try:
            json = await request.json()
            guess = json["guess"]
            assert isinstance(guess, str)
        except Exception:
            return web.Response(status=400, text="JSON payload with guess field expected")
        navec = get_navec_model()
        guess = guess.lower()
        if guess not in navec:
            return web.Response(status=404, text="Unknown word :(")
        
        top_word = app["storage"].top_words_by_str.get(guess)
        if top_word is not None:
            return web.json_response(data=top_word)

        answer = app["storage"].answer
        return web.json_response(data=Word(word=guess, similarity=navec.sim(answer, guess)))

    app.router.add_post("/guess", guess)
