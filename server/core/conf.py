# default
import os
from enum import Enum
from functools import lru_cache

# libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


# testing
@lru_cache
def is_testing():  # pragma: no cover
    """Return whether or not this code is being executed under test env"""
    import sys

    return "pytest" in sys.modules


# env
is_test_env = is_testing()
load_dotenv(override=True, dotenv_path="example.env" if is_test_env else ".env")
get_env = os.environ.get


# env var
class ENVEnum(Enum):
    DEV = "DEV"
    ADMIN = "ADMIN"
    USER = "USER"


class Settings(BaseSettings):
    # TODO: change this to ENVEnum when lib support
    ENV: str

    SECRET_KEY: str

    DATABASE_URL: str

    AWS_ACCESS_KEY_ID: str
    AWS_ACCESS_ACCESS_KEY: str
    AWS_BUCKET: str

    TINY_PNG_API_KEY: str

    DISCORD_BOT_TOKEN: str
    DISCORD_OAUTH_URL: str
    DISCORD_CLIENT_ID: str
    DISCORD_CLIENT_SECRET: str
    DISCORD_REDIRECT_URL: str

    FACEBOOK_ACCESS_TOKEN: str
    FACEBOOK_APP_ID: str
    FACEBOOK_APP_SECRET: str

    GEMINI_AI_API_KEY: str


settings = Settings()
is_dev_env = settings.ENV == ENVEnum.DEV.value
is_user_portal = settings.ENV == ENVEnum.USER.value
is_admin_portal = settings.ENV == ENVEnum.ADMIN.value

# basic config
app = FastAPI(
    title="BETTERME.NEWS API",
    version="0.1.0",
    # disable docs in user portal
    docs_url="/api/docs" if not is_user_portal else None,
    openapi_url="/openapi.json" if not is_user_portal else None,
    default_response_class=ORJSONResponse,
)

allow_origins = (
    ["*"]
    if settings.ENV == ENVEnum.DEV.value
    else [
        "https://betterme.news",
        "https://admin.betterme.news",
        "http://betterme.news",
        "http://admin.betterme.news",
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.mount("/api/media", StaticFiles(directory="scrap/data/media"), name="media")
