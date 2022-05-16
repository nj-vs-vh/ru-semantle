import os


REDIS_URL = os.environ["REDIS_URL"]
PORT = int(os.environ.get("PORT", 8088))
