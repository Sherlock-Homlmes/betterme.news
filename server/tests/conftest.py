# default

# libraries
import beanie
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient

# local
from core.models import document_models
from core.routes import api_router


app = FastAPI()
app.include_router(api_router)


@pytest.fixture(scope="function", autouse=True)
def client():
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
async def init_db():
    db_client = AsyncMongoMockClient()
    await beanie.init_beanie(database=db_client.betterme_news, document_models=document_models)


@pytest.fixture(scope="function", autouse=True)
async def clean_db(init_db):
    await init_db
    models = document_models

    for model in models:
        await model.get_motor_collection().drop()
        await model.get_motor_collection().drop_indexes()

    return None
