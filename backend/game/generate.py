import random
import logging
from typing import Optional
from tqdm import tqdm

from pymorphy2.analyzer import Parse

from backend.dependencies import get_frequent_words, get_navec_model, get_pymorph_model
from backend.game.types import Word, TopWord, SemantleGame


logger = logging.getLogger(__name__)


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
            return None
        return parse.normalized.word
    except Exception as e:
        logger.warning(f"Unexpected error normalizing word '{word}': {e}")
        return None


def generate_answer() -> str:
    navec = get_navec_model()
    frequent_words = get_frequent_words()
    for attempt in range(10000):
        answer = random.choice(frequent_words)
        answer = normalize_word(answer)
        if answer is not None and answer in navec:
            logger.info(f"Answer (generated in {attempt + 1} attempt(s)): {answer}")
            return answer
    else:
        raise RuntimeError("Didn't generate a normalizeable answer in 10000 attempts :(")


def generate_game(n_top_words: int = 1000) -> SemantleGame:
    logger.info("Generating new Semantle game")
    navec = get_navec_model()
    vocab: list[str] = navec.vocab.words
    answer = generate_answer()
    current_threshold_similarity = 0
    current_top_words: list[Word] = []
    for word in tqdm(vocab, unit="w"):
        similarity = navec.sim(word, answer)
        if similarity > current_threshold_similarity:
            current_top_words.append(Word(word=word, similarity=similarity))
            current_top_words.sort(key=lambda w: w.similarity, reverse=True)
            if len(current_top_words) > n_top_words:
                current_top_words.pop(-1)
                current_threshold_similarity = current_top_words[-1].similarity

    return n_top_words, current_top_words


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)


    with open("answers.txt", "w") as f:
        for _ in range(1000):
            print(generate_answer(), file=f)


    with open("games.txt", "w") as f:
        for _ in range(10):
            f.write("\n\n")
            game = generate_game(30)
            for w in game:
                f.write(f"{w.word : >30} {w.similarity}\n")
