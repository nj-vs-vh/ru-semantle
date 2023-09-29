from dataclasses import dataclass
from datetime import date, datetime
import json
import logging
from redis import Redis
import asyncio
import pytz

from typing import Optional

from backend.game.types_ import GameClues, GameConfig, SemantleGame, TopWord
from backend.game.generate import generate_game


logger = logging.getLogger(__name__)


@dataclass
class CachedSemantleGame:
    """Semantle game loaded into RAM for fast access"""

    game_no: int
    top_word_count: int
    answer: TopWord
    top_words: list[TopWord]
    top_words_by_str: dict[str, TopWord]
    cached_on: date
    clues: GameClues


GeneratedSemantleGame = tuple[int, SemantleGame]  # game number and the game itself


class GameStorage:
    CURRENT_GAME_KEY = "ru-semantle-current-game"
    CURRENT_GAME_NUMBER_KEY = "ru-semantle-current-game-no"
    CURRENT_GAME_GENERATED_AT_KEY = "ru-semantle-current-game-generated-at"

    def __init__(self, config: GameConfig, redis: Redis):
        self.config = config
        self.redis = redis
        self._cache(self._load_sync_game())

    def _cache(self, game: GeneratedSemantleGame):
        game_no, top_words = game
        self._cached = CachedSemantleGame(
            game_no=game_no,
            top_words=top_words,
            answer=top_words[0],
            top_word_count=len(top_words),
            top_words_by_str={tw["word"]: tw for tw in top_words},
            clues=GameClues(
                next_to_answer_similarity=top_words[1]["similarity"],
                word_10_similarity=top_words[9]["similarity"],
                word_100_similarity=top_words[99]["similarity"],
                last_top_word_similarity=top_words[-1]["similarity"],
            ),
            cached_on=local_datetime(),
        )

    @property
    def cached(self) -> CachedSemantleGame:
        if self._cached.cached_on.date() < local_date():
            logger.info("Found expired game in cache, synchronizing")
            self._cache(self._load_sync_game())
        return self._cached

    async def daily_game_update(self):
        logger.info("Running periodic game synchronization")
        while True:
            await asyncio.sleep(300)
            self._cache(self._load_sync_game())

    def reset_game(self):
        self._cache(self._new_game())

    def _new_game(self) -> GeneratedSemantleGame:
        game = generate_game(n_top_words=self.config.n_top_words, local_dimensions=self.config.local_dimensions)
        dump = json.dumps(game, ensure_ascii=False)
        dump = dump.encode("utf-8")
        self.redis.set(self.CURRENT_GAME_KEY, dump)
        self.redis.set(self.CURRENT_GAME_GENERATED_AT_KEY, local_datetime().isoformat())
        game_number = self.redis.incr(self.CURRENT_GAME_NUMBER_KEY)
        return game_number, game

    def _load_sync_game(self) -> GeneratedSemantleGame:
        try:
            game_dump: Optional[bytes] = self.redis.get(self.CURRENT_GAME_KEY)
            game_generated_at_dump: Optional[bytes] = self.redis.get(self.CURRENT_GAME_GENERATED_AT_KEY)
            game_generated_at = datetime.fromisoformat(game_generated_at_dump.decode("utf-8"))
            if local_date() > game_generated_at.date():
                logger.info(
                    f"Found expired game in storage (generated on {game_generated_at.date()}, now {local_date()})"
                )
                return self._new_game()
            game = json.loads(game_dump.decode("utf-8"))
            assert isinstance(game, list)
            game_number = int(self.redis.get(self.CURRENT_GAME_NUMBER_KEY).decode("utf-8"))
            logger.info(f"Game loaded, {game_number = }, {game_generated_at = }")
            return game_number, game
        except Exception as e:
            logger.info(f"Error reading game from Redis, generating new one: {e}")
            return self._new_game()


GAME_TZ = pytz.timezone("Asia/Tbilisi")  # new game is generatedat midnight in this timezone


def local_datetime() -> datetime:
    now_utc = pytz.utc.localize(datetime.utcnow())
    return now_utc.astimezone(GAME_TZ)


def local_date() -> date:
    return local_datetime().date()
