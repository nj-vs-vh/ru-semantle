from dataclasses import asdict, dataclass
from typing import TypedDict


class Word(TypedDict):
    word: str
    similarity: float  # cosine similarity to answer, scaled up to [0, 100)


class TopWord(Word):
    rating: int  # in the list of top words
    local_coords: tuple[float, float]  # used for visualization


SemantleGame = list[TopWord]


@dataclass
class GameConfig:
    n_top_words: int
    local_dimensions: int

    def to_json(self) -> dict:
        return asdict(self)
