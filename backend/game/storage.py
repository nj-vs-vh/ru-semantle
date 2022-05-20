from dataclasses import dataclass
from datetime import date, datetime
import json
import logging
from redis import Redis
import asyncio
import pytz

from typing import Optional

from backend.game.types_ import GameConfig, SemantleGame, TopWord
from backend.game.generate import generate_game


logger = logging.getLogger(__name__)


@dataclass
class CachedSemantleGame:
    """Semantle game loaded into RAM for fast access"""

    top_word_count: int
    answer: str
    top_words: list[TopWord]
    top_words_by_str: dict[str, TopWord]
    cached_on: date


class GameStorage:
    CURRENT_GAME_KEY = "ru-semantle-current-game"
    CURRENT_GAME_GENERATED_AT_KEY = "ru-semantle-current-game-generated-at"

    def __init__(self, config: GameConfig, redis: Redis):
        self.config = config
        self.redis = redis
        self._cache(self._synchronize_game())

    def _cache(self, game: SemantleGame):
        self._cached = CachedSemantleGame(
            top_word_count=game[0],
            answer=game[1][0],
            top_words=game[1],
            top_words_by_str={tw["word"]: tw for tw in game[1]},
            cached_on=local_date(),
        )

    @property
    def cached(self) -> CachedSemantleGame:
        if self._cached.cached_on < local_date():
            logger.info("Found old game in cache, synchronizing")
            self._cache(self._synchronize_game())
        return self._cached

    async def daily_game_update(self):
        logger.info("Running periodic game synchronization")
        while True:
            await asyncio.sleep(300)
            self._cache(self._synchronize_game())

    def reset_game(self):
        self._cache(self._new_game())

    def _new_game(self) -> SemantleGame:
        game = generate_game(n_top_words=self.config.n_top_words, local_dimensions=self.config.local_dimensions)
        dump = json.dumps(game, ensure_ascii=False)
        dump = dump.encode("utf-8")
        self.redis.set(self.CURRENT_GAME_KEY, dump)
        self.redis.set(self.CURRENT_GAME_GENERATED_AT_KEY, local_datetime().isoformat())
        return game

    def _synchronize_game(self) -> SemantleGame:
        try:
            game_dump: Optional[bytes] = self.redis.get(self.CURRENT_GAME_KEY)
            game_generated_at_dump: Optional[bytes] = self.redis.get(self.CURRENT_GAME_GENERATED_AT_KEY)
            game_generated_at = datetime.fromisoformat(game_generated_at_dump.decode("utf-8"))
            if local_date() > game_generated_at.date():
                logger.info(f"Found old game in storage (generated on {game_generated_at.date()}, now {local_date()})")
                return self._new_game()
            game_size, top_words = json.loads(game_dump.decode("utf-8"))
            return game_size, top_words
        except Exception:
            return self._new_game()


GAME_TZ = pytz.timezone("Asia/Tbilisi")


def local_datetime() -> datetime:
    now_utc = pytz.utc.localize(datetime.utcnow())
    return now_utc.astimezone(GAME_TZ)


def local_date() -> date:
    return local_datetime().date()
