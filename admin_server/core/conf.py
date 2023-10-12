# default
import os

# libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
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
class Settings(BaseSettings):
    IS_DEV_ENV: bool = False
    DATABASE_URL: str


settings = Settings()

# basic config
app = FastAPI(
    title="BETTERME.NEWS API",
    version="0.1.0",
    docs_url="/api/docs",
    openapi_url="/openapi.json",
)

allow_origins = (
    ["*"]
    if settings.IS_DEV_ENV
    else ["https://admin.betterme.news", "http://admin.betterme.news"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="frontend/templates")
TemplateResponse = templates.TemplateResponse
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/scrap", StaticFiles(directory="scrap"), name="scrap")
