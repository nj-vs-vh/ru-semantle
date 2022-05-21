import asyncio
import logging
import random
from aiohttp import web, hdrs
from redis import Redis

from aiohttp.typedefs import Handler

from backend.dependencies import get_navec_model
from backend.game.generate import normalize_word
from backend.game.types_ import GameConfig, Word
from backend.game.storage import GameStorage
from backend.admin import requires_admin_token
from backend import config


logger = logging.getLogger(__name__)


def create_app() -> web.Application:
    logger.info("Creating backend app")

    app = web.Application(client_max_size=512)

    # additional resources initialization

    async def init_game_storage(app: web.Application):
        game_config = GameConfig(n_top_words=1000, local_dimensions=2)
        game_storage = GameStorage(config=game_config, redis=Redis.from_url(config.REDIS_URL))
        loop = asyncio.get_event_loop()
        loop.create_task(game_storage.daily_game_update())
        app["storage"] = game_storage
        app["config"] = game_config

    app.on_startup.append(init_game_storage)

    # CORS stuff

    @web.middleware
    async def cors_middleware(request: web.Request, handler: Handler):
        resp = await handler(request)
        allowed_origin = "https://ru-semantle.surge.sh" if config.IS_PROD else "http://localhost:8080"
        resp.headers[hdrs.ACCESS_CONTROL_ALLOW_ORIGIN] = allowed_origin
        resp.headers[hdrs.ACCESS_CONTROL_ALLOW_HEADERS] = "Content-Type"
        # not actually true but whatever :)
        resp.headers[hdrs.ACCESS_CONTROL_ALLOW_METHODS] = "POST, GET, OPTIONS"
        return resp

    async def preflight(request: web.Request) -> web.Response:
        return web.Response()

    app.router.add_options("/{wildcard:.*}", preflight)
    app.middlewares.append(cors_middleware)

    # routes

    @requires_admin_token
    async def reset_game(request: web.Request) -> web.Response:
        storage: GameStorage = app["storage"]
        storage.reset_game()
        return web.Response(text="Reset")

    async def metadata(request: web.Request) -> web.Response:
        config: GameConfig = app["config"]
        storage: GameStorage = app["storage"]
        return web.json_response(
            {
                "config": config.to_json(),
                "game_number": storage.cached.game_no,
                "clues": storage.cached.clues.to_json(),
            }
        )

    async def give_up(request: web.Request) -> web.Response:
        storage: GameStorage = app["storage"]
        return web.json_response(storage.cached.top_words)

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
            return web.Response(status=404, text="В нашем словаре нет такого слова :(")

        storage: GameStorage = app["storage"]
        top_word = storage.cached.top_words_by_str.get(guess)
        if top_word is not None:
            return web.json_response(data=top_word)

        answer = storage.cached.answer["word"]
        return web.json_response(data=Word(word=guess, similarity=float(navec.sim(answer, guess))))

    async def hint(request: web.Request) -> web.Response:
        try:
            json = await request.json()
            current_best_rating = json.get("current_best_rating", None)
        except Exception:
            return web.Response(status=400, text="JSON payload expected")
        storage: GameStorage = app["storage"]
        if current_best_rating is None:
            return web.json_response(storage.cached.top_words[-1])
        else:
            return web.json_response(storage.cached.top_words[max(0, current_best_rating - 2)])

    async def random_words(request: web.Request) -> web.Response:
        words = []
        for word in random.choices(get_navec_model().vocab.words, k=100):
            normalized = normalize_word(word)
            if normalized:
                words.append(normalized)
        return web.json_response(words)

    app.router.add_get("/metadata", metadata)
    app.router.add_get("/random-words", random_words)
    app.router.add_post("/guess", guess)
    app.router.add_post("/hint", hint)
    app.router.add_get("/give-up", give_up)
    app.router.add_post("/admin/reset", reset_game)

    return app
