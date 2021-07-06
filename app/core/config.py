from starlette.config import Config

API_DOCS_URL = "/__docs"
API_REDOC_URL = None

API_VERSION = "0.1.1"

API_PROJECT_NAME = "instorify-api"

PLUGINS_ACCOUNTS_MAX_RETRY = 5
PLUGINS_ACCOUNTS_COOKIE_PATH = '../cache'


config = Config(".env")

INSTAGRAM_LOGIN: str = config("INSTAGRAM_LOGIN")
INSTAGRAM_PASS: str = config("INSTAGRAM_PASS")

REDIS_URL: str = config("REDIS_URL")

NO_ROUTES_CACHE: bool = config("NO_ROUTES_CACHE")
ROUTES_CACHE_EXPIRES_TIME = None if NO_ROUTES_CACHE else 180

API_DEBUG: str = config("API_DEBUG")
API_RELOAD: str = config("API_RELOAD")
