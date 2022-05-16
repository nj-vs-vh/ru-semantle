from dataclasses import dataclass
import random
import logging
from typing import Optional
from tqdm import tqdm

from pymorphy2.analyzer import Parse

from backend.dependencies import get_navec_model, get_pymorph_model


logger = logging.getLogger(__name__)


@dataclass
class Word:
    word: str
    similarity: float  # cosine similarity to answer, scaled up to [0, 100)


@dataclass
class TopWord(Word):
    rating: int  # in the list of top words
    local_euclidian_coord: tuple[float, float]  # used for visualization


SemantleGame = list[TopWord]


def normalize_word(word: str) -> Optional[str]:
    try:
        ma = get_pymorph_model()
        if not ma.word_is_known(word):
            return None
        parses = ma.parse(word)
        if len(parses) != 1:
            return None  # avoid polysemantic words
        parse: Parse = parses[0]
        if parse.tag.POS not in {"NOUN", "VERB", "ADJF", "INFN", "PRTF", "NUMR", "NPRO"}:
            return None  # restricting to a selected parts of speech
        return parse.normalized.word
    except Exception as e:
        logger.warning(f"Unexpected error normalizing word '{word}': {e}")
        return None


def generate_game(n_top_words: int = 1000) -> SemantleGame:
    logger.info("Generating new Semantle game")
    model = get_navec_model()
    vocab: list[str] = model.vocab.words
    for attempt in range(10000):
        answer = random.choice(vocab)
        answer = normalize_word(answer)
        if answer is not None and answer in vocab:
            break
    else:
        raise RuntimeError("Didn't generate a normalizeable answer in 10000 attempts :(")
    logger.info(f"Answer (generated in {attempt + 1} attempt(s)): {answer}")
    current_threshold_similarity = 0
    current_top_words: list[Word] = []
    for word in tqdm(vocab, unit="w"):
        word_similarity = model.sim(word, answer)
        if word_similarity > current_threshold_similarity:
            current_top_words.append(Word(word, word_similarity))
            current_top_words.sort(key=lambda w: w.similarity, reverse=True)
            if len(current_top_words) > n_top_words:
                current_top_words.pop(-1)
                current_threshold_similarity = current_top_words[-1].similarity

    return current_top_words


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    with open("games.txt", "a") as f:
        for _ in range(10):
            f.write("\n\n")
            game = generate_game(30)
            for w in game:
                f.write(f"{w.word : >50} {w.similarity}\n")
