import logging
from pathlib import Path
import re
import zipfile
import wget
from typing import Optional

from navec import Navec
from pymorphy2 import MorphAnalyzer


logger = logging.getLogger(__name__)


CUR_DIR = Path(__file__).parent
MODELS_DIR = (CUR_DIR / "../models").resolve()
MODELS_DIR.mkdir(exist_ok=True)


NAVEC_MODEL_URL = 'https://storage.yandexcloud.net/natasha-navec/packs/navec_hudlit_v1_12B_500K_300d_100q.tar'
NAVEC_MODEL_PATH = MODELS_DIR / "navec_hudlit_v1_12B_500K_300d_100q.tar"
_NAVEC_MODEL: Optional[Navec] = None


def get_navec_model() -> Navec:
    global _NAVEC_MODEL
    if _NAVEC_MODEL is None:
        if not NAVEC_MODEL_PATH.exists():
            logger.info("Downloading Navec model...")
            wget.download(NAVEC_MODEL_URL, out=str(NAVEC_MODEL_PATH))
        logger.info("Reading Navec model from disk...")
        _NAVEC_MODEL = Navec.load(NAVEC_MODEL_PATH)
    return _NAVEC_MODEL


_PYMORPH_MODEL: Optional[MorphAnalyzer] = None


def get_pymorph_model() -> MorphAnalyzer:
    global _PYMORPH_MODEL
    if _PYMORPH_MODEL is None:
        _PYMORPH_MODEL = MorphAnalyzer()
    return _PYMORPH_MODEL


CORPUS_URL = "https://ruscorpora.ru/new/ngrams/3grams-3.zip"
RUSCORPORA_3GRAMS_ARCHIVE_FILE = MODELS_DIR / "3grams-3.zip"
RUSCORPORA_3GRAMS_FILE = MODELS_DIR / "3grams-3.txt"
N_FREQUENT_WORDS = 100000  # 100K most frequent words in Russian that may be chosen as answers
FREQUENT_WORDS_FILE = MODELS_DIR / f"{N_FREQUENT_WORDS}-frequent-words.txt"
_FREQUENT_WORDS_CORPUS: Optional[list[str]] = None


def get_frequent_words() -> list[str]:
    global _FREQUENT_WORDS_CORPUS
    if _FREQUENT_WORDS_CORPUS is None:
        if not FREQUENT_WORDS_FILE.exists():
            corpus = set()
            if not RUSCORPORA_3GRAMS_FILE.exists():
                logger.info("No RusCorpora word frequency file...")
                if not RUSCORPORA_3GRAMS_ARCHIVE_FILE.exists():
                    logger.info("Downloading RusCorpora word frequency list...")
                    wget.download(CORPUS_URL, out=str(RUSCORPORA_3GRAMS_ARCHIVE_FILE))
                logger.info(f"Extracting {RUSCORPORA_3GRAMS_ARCHIVE_FILE}...")
                with zipfile.ZipFile(RUSCORPORA_3GRAMS_ARCHIVE_FILE, "r") as zf:
                    zf.extractall(MODELS_DIR)
            if not RUSCORPORA_3GRAMS_FILE.exists():
                raise RuntimeError("Error downloading and extracting RusCorpora word frequency list")
            logger.info(f"Extracting frequent words from {RUSCORPORA_3GRAMS_FILE}")
            wordlike_re = re.compile(r"\w{3,}$")
            with open(RUSCORPORA_3GRAMS_FILE, "r") as f:
                for line in f:
                    for w in line.split("\t")[1:]:
                        w = w.strip()
                        if wordlike_re.match(w):
                            corpus.add(w)
                    if len(corpus) > N_FREQUENT_WORDS:
                        break
            logger.info(f"Writing frequent words to {FREQUENT_WORDS_FILE}")
            with open(FREQUENT_WORDS_FILE, "w") as f:
                for word in corpus:
                    f.write(word)
                    f.write("\n")
        logger.info(f"Reading frequent words from {FREQUENT_WORDS_FILE}")
        _FREQUENT_WORDS_CORPUS = FREQUENT_WORDS_FILE.read_text().splitlines()
    return _FREQUENT_WORDS_CORPUS
