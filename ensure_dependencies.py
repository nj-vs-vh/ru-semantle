import logging
from backend.dependencies import get_navec_model, get_frequent_words, get_pymorph_model

logging.basicConfig(level=logging.INFO)

get_navec_model()
get_frequent_words()
get_pymorph_model()
