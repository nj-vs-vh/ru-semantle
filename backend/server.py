from typing import TypedDict
from aiohttp import web

from backend.dependencies import get_navec_model
from backend.game.types import TopWord, Word


class AppExtensions(TypedDict):
    semantle_answer: str
    semantle_top_words_by_str: dict[str, TopWord]


class Application(web.Application, AppExtensions):
    pass


def create_app() -> Application:
    app: Application = web.Application(client_max_size=512)

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
        
        top_word = app["semantle_top_words_by_str"].get(guess)
        if top_word is not None:
            return web.json_response(data=top_word)

        answer = app["semantle_answer"]
        return web.json_response(data=Word(word=guess, similarity=navec.sim(answer, guess)))

    app.router.add_post("/guess", guess)
