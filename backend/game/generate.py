import random
import logging
from typing import Optional
import numpy as np
from tqdm import tqdm

from pymorphy2.analyzer import Parse
from sklearn.decomposition import PCA

from backend.dependencies import get_frequent_words, get_navec_model, get_pymorph_model
from backend.game.types_ import Word, TopWord, SemantleGame


logger = logging.getLogger(__name__)


def _normalize_word(word: str) -> Optional[str]:
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
        answer = _normalize_word(answer)
        if answer is not None and answer in navec:
            logger.info(f"Answer (generated in {attempt + 1} attempt(s)): {answer}")
            return answer
    else:
        raise RuntimeError("Didn't generate a normalizeable answer in 10000 attempts :(")


def enhance_top_words(words: list[Word], local_dimensions: int) -> list[TopWord]:
    navec = get_navec_model()
    # list of 1 x word vector dims numpy arrays
    word_vectors: list[np.ndarray] = [np.expand_dims(navec[w["word"]], 0) for w in words]
    # top words count x word vector dims numpy array
    word_vectors_mat = np.vstack(word_vectors)
    pca = PCA(n_components=local_dimensions)
    local_vectors = pca.fit_transform(word_vectors_mat)
    logger.info(f"PCA explained variance ratio per reduced dimension: {pca.explained_variance_ratio_}")
    local_vectors -= local_vectors[0, :]  # centering at correct answer
    local_vectors /= np.max(np.abs(local_vectors), axis=0)
    return [
        TopWord(
            word=w["word"],
            similarity=w["similarity"],
            rating=(i + 1),
            local_coords=tuple(float(c) for c in local_vectors[i, :]),
        )
        for i, w in enumerate(words)
    ]


def generate_game(n_top_words: int = 1000, local_dimensions: int = 2) -> SemantleGame:
    logger.info("Generating new Semantle game")
    navec = get_navec_model()
    vocab: list[str] = navec.vocab.words
    answer = generate_answer()
    current_threshold_similarity = 0
    top_current_words: list[Word] = []
    for word in tqdm(vocab, unit="w"):
        similarity = navec.sim(word, answer)
        if similarity > current_threshold_similarity:
            top_current_words.append(Word(word=word, similarity=float(similarity)))
            top_current_words.sort(key=lambda w: w["similarity"], reverse=True)
            if len(top_current_words) > n_top_words:
                top_current_words.pop(-1)
                current_threshold_similarity = top_current_words[-1]['similarity']

    return n_top_words, enhance_top_words(top_current_words, local_dimensions)


if __name__ == "__main__":
    import json

    logging.basicConfig(level=logging.INFO)

    # with open("answers.txt", "w") as f:
    #     for _ in range(1000):
    #         print(generate_answer(), file=f)

    # with open("games.txt", "w") as f:
    #     for _ in range(10):
    #         f.write("\n\n")
    #         game = generate_game(30)
    #         for w in game:
    #             f.write(f"{w['word'] : >30} {w['similarity']}\n")

    from matplotlib import pyplot as plt

    _, top_words = generate_game(2000)
    x = [tw["local_coords"][0] for tw in top_words]
    y = [tw["local_coords"][1] for tw in top_words]
    plt.scatter(x, y, marker='.')
    plt.savefig("words.png")
