from datetime import datetime
import json
import logging
from redis import Redis
import asyncio
import pytz

from backend.game.types import SemantleGame, TopWord
from backend.game.generate import generate_game


logger = logging.getLogger(__name__)


class GameStorage:
    CURRENT_GAME_KEY = "ru-semantle-current-game"
    GAME_TZ = pytz.timezone("Asia/Tbilisi")

    def __init__(self, redis: Redis):
        self.redis = redis
        self._parse_game(self._load_game())

    def _parse_game(self, game: SemantleGame):
        self.top_word_count = game[0]
        self.answer = game[1][0]
        self.top_words = game[1]
        self.top_words_by_str = {tw["word"]: tw for tw in self.top_words}

    async def daily_game_update(self):
        while True:
            now_utc = pytz.utc.localize(datetime.utcnow())
            now_local = now_utc.astimezone(self.GAME_TZ)
            logger.info(f"Current datetime in Tbilisi: {now_local}")
            elapsed_since_midnight_sec = now_local.second + now_local.minute * 60 + now_local.hour * 3600
            to_midnight_sec = max(86400 - elapsed_since_midnight_sec, 10)
            to_midnight_hrs = to_midnight_sec / 3600
            logger.info(f"Next game will be generated in {to_midnight_hrs:.5f} hours")
            await asyncio.sleep(to_midnight_sec)
            self._parse_game(self._new_game())

    def reset_game(self):
        self._parse_game(self._new_game())

    def _new_game(self) -> SemantleGame:
        game = generate_game()
        dump = json.dumps(game, ensure_ascii=False)
        dump = dump.encode("utf-8")
        self.redis.set(self.CURRENT_GAME_KEY, dump)
        return game

    def _load_game(self) -> SemantleGame:
        game_dump = self.redis.get(self.CURRENT_GAME_KEY)
        if game_dump is None:
            return self._new_game()
        game_size, top_words = json.loads(game_dump.decode("utf-8"))
        return game_size, top_words
