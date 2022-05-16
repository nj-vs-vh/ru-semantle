import logging
from pathlib import Path
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



CORPUS_URL = "https://ruscorpora.ru/new/ngrams/1grams-3.zip"
CORPUS_ZIP_FILE = MODELS_DIR / "corpus.zip"
CORPUS_FILE = MODELS_DIR / "1grams-3.txt"
N_FREQUENT_WORDS = 100000  # 100K most frequent words in Russian that may be chosen as answers
_FREQUENT_WORDS_CORPUS: Optional[set[str]] = None


def get_frequent_words() -> set[str]:
    global _FREQUENT_WORDS_CORPUS
    if _FREQUENT_WORDS_CORPUS is None:
        _FREQUENT_WORDS_CORPUS = set()
        if not CORPUS_ZIP_FILE.exists():
            logger.info("Downloading RusCorpora word frequency list...")
            wget.download(CORPUS_URL, out=str(CORPUS_ZIP_FILE))
        with zipfile.ZipFile(CORPUS_ZIP_FILE, "r") as zf:
            zf.extractall(MODELS_DIR)
        if not CORPUS_FILE.exists():
            raise RuntimeError("Error downloading and extracting RusCorpora word frequency list")
        with open(CORPUS_FILE, "r") as f:
            for idx, line in enumerate(f):
                if idx > N_FREQUENT_WORDS:
                    break
                word = " ".join(line.split("\t")[1:])
                _FREQUENT_WORDS_CORPUS.add(word.strip().lower())
    return _FREQUENT_WORDS_CORPUS
