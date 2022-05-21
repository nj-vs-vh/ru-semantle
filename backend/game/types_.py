from dataclasses import asdict, dataclass
from typing import TypedDict


class Word(TypedDict):
    word: str
    similarity: float  # cosine similarity to answer, scaled up to [0, 100)


class TopWord(Word):
    rating: int  # in the list of top words
    local_coords: tuple[float, float]  # used for visualization


SemantleGame = list[TopWord]


class Jsonable:
    def to_json(self) -> dict:
        return asdict(self)


@dataclass
class GameConfig(Jsonable):
    n_top_words: int
    local_dimensions: int


@dataclass
class GameClues(Jsonable):
    next_to_answer_similarity: float
    word_10_similarity: float
    word_100_similarity: float
    last_top_word_similarity: float
