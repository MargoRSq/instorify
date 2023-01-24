import os
from starlette.config import Config

# FastAPI instance data
API_DOCS_URL = "/__docs"
API_REDOC_URL = None

API_VERSION = "0.1.1"
API_PROJECT_NAME = "instorify-api"

# in case of failed auth on instagram
PLUGINS_ACCOUNTS_MAX_RETRY = 5
PLUGINS_ACCOUNTS_COOKIE_PATH = os.path.join(os.getcwd(), 'cache')

config = Config("../.env")

INSTAGRAM_LOGIN: str = config("INSTAGRAM_LOGIN")
INSTAGRAM_PASS: str = config("INSTAGRAM_PASS")
