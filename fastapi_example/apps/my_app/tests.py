import pytest
from starlette.testclient import TestClient
from tortoise import Tortoise
from tortoise.contrib.test import finalizer, initializer
from fastapi_example.apps.my_app.models import Tournament
from contextlib import asynccontextmanager
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
from httpx import AsyncClient

TEST_DB_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.sqlite",  # SQLite 엔진 사용
            "credentials": {
                "file_path": ":memory:",  # 메모리 내 데이터베이스
            }
        }
    },
    # 등록된 앱 지정
    "apps": {
        "my_app": {
            "models": ["apps.my_app.models"],  # 모델 경로
            "default_connection": "default",
        },
        "blogs": {
            "models": ["apps.blogs.models"],  # 모델 경로
            "default_connection": "default",
        }
    },
    "use_tz": False,  # 타임존 사용 여부
    "timezone": "UTC"  # 타임존 설정
}


@asynccontextmanager
async def custom_lifespan(app: FastAPI):
    await Tortoise.init(config=TEST_DB_CONFIG)
    await Tortoise.generate_schemas()
    try:
        yield
    finally:
        await Tortoise.close_connections()


@pytest.fixture(scope="module", autouse=True)
async def client():
    app = FastAPI(title="test_app", lifespan=custom_lifespan)
    register_tortoise(app=app, config=TEST_DB_CONFIG, generate_schemas=False, add_exception_handlers=True)
    async with AsyncClient(app=app) as async_client:
        yield async_client




@pytest.mark.asyncio
async def test_create_tournaments(client):
    tournaments = await Tournament.create(id=1, name="test_tournaments")
    tournaments_from_db = await Tournament.get(name="test_tournaments")

    assert tournaments_from_db.id == 1
    assert tournaments_from_db.name == "test_tournaments"
