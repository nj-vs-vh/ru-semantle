from typing import TypedDict


class Word(TypedDict):
    word: str
    similarity: float  # cosine similarity to answer, scaled up to [0, 100)


class TopWord(Word):
    rating: int  # in the list of top words
    local_euclidian_coord: tuple[float, float]  # used for visualization


SemantleGame = list[TopWord]