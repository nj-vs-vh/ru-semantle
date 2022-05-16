import asyncio
import logging
from aiohttp import web
from redis import Redis

from backend.dependencies import get_navec_model
from backend.game.types_ import GameConfig, Word
from backend.game.storage import GameStorage
from backend.admin import requires_admin_token
from backend import config


def create_app() -> web.Application:
    logging.basicConfig(level=logging.INFO)

    app = web.Application(client_max_size=512)

    async def init_game_storage(app: web.Application):
        game_config = GameConfig(n_top_words=1000, local_dimensions=2)
        game_storage = GameStorage(config=game_config, redis=Redis.from_url(config.REDIS_URL))
        loop = asyncio.get_event_loop()
        loop.create_task(game_storage.daily_game_update())
        app["storage"] = game_storage
        app["config"] = game_config

    app.on_startup.append(init_game_storage)

    @requires_admin_token
    async def reset_game(request: web.Request) -> web.Response:
        storage: GameStorage = app["storage"]
        storage.reset_game()
        return web.Response(text="Reset")

    async def dump_config(request: web.Request) -> web.Response:
        config: GameConfig = app["config"]
        return web.json_response(config.to_json())

    async def dump_top_words(request: web.Request) -> web.Response:
        storage: GameStorage = app["storage"]
        return web.json_response(storage.top_words)

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

        storage: GameStorage = app["storage"]
        top_word = storage.top_words_by_str.get(guess)
        if top_word is not None:
            return web.json_response(data=top_word)

        answer = storage.answer["word"]
        return web.json_response(data=Word(word=guess, similarity=float(navec.sim(answer, guess))))

    app.router.add_post("/guess", guess)
    app.router.add_get("/game-config", dump_config)
    app.router.add_get("/top-words", dump_top_words)
    app.router.add_post("/reset", reset_game)

    return app