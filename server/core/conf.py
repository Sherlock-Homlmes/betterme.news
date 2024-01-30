# default
import os
from enum import Enum

# libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


# testing
def is_testing():  # pragma: no cover
    """Return whether or not this code is being executed under test env"""
    import sys

    return "pytest" in sys.modules


# env
load_dotenv(override=True, dotenv_path="example.env" if is_testing() else ".env")
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

    DISCORD_BOT_TOKEN: str
    DISCORD_OAUTH_URL: str
    DISCORD_CLIENT_ID: str
    DISCORD_CLIENT_SECRET: str
    DISCORD_REDIRECT_URL: str

    FACEBOOK_ACCESS_TOKEN: str
    FACEBOOK_APP_ID: str
    FACEBOOK_APP_SECRET: str


settings = Settings()
is_dev_env = settings.ENV == ENVEnum.DEV.value

# basic config
app = FastAPI(
    title="BETTERME.NEWS API",
    version="0.1.0",
    docs_url="/api/docs",
    openapi_url="/openapi.json",
)

allow_origins = (
    ["*"]
    if settings.ENV == ENVEnum.DEV
    else ["https://admin.betterme.news", "http://admin.betterme.news"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/api/media", StaticFiles(directory="scrap/data/media"), name="media")
