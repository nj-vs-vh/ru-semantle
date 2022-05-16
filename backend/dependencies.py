import logging
from pathlib import Path
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
