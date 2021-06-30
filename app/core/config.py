from starlette.config import Config

DOCS_URL = "/__docs"
REDOC_URL = None

VERSION = "0.1.0"

PROJECT_NAME = "instorify-api"

MAX_CONN_TRY = 5
COOKIE_PATH = '../cache'


config = Config(".env")

LOGIN: str = config("LOGIN")
PASS: str = config("PASS")

REDIS_URL: str = config("REDIS_URL")

NO_ROUTES_CACHE: bool = config("NO_ROUTES_CACHE")
ROUTES_CACHE_EXPIRES_TIME = 0 if NO_ROUTES_CACHE else 180
