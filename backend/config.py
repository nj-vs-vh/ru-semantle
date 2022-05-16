import os


REDIS_URL = os.environ["REDIS_URL"]
PORT = int(os.environ.get("PORT", 8088))
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "dummy")
