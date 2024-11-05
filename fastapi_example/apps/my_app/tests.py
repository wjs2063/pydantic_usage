import pytest
from starlette.testclient import TestClient
from tortoise import Tortoise
from tortoise.contrib.test import finalizer, initializer
from fastapi_example.apps.my_app.models import Tournament
from contextlib import asynccontextmanager
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.test import MEMORY_SQLITE
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator, Tuple
from asgi_lifespan import LifespanManager
from pathlib import Path
import os

os.environ["DB_URL"] = MEMORY_SQLITE

try:
    from fastapi_example.main import app
    # from main_custom_timezone import app as app_east
    from fastapi_example.apps.my_app.models import Tournament
except ImportError:
    if (cwd := Path.cwd()) == (parent := Path(__file__).parent):
        dirpath = "."
    else:
        dirpath = str(parent.relative_to(cwd))
    print(f"You may need to explicitly declare python path:\n\nexport PYTHONPATH={dirpath}\n")
    raise

ClientManagerType = AsyncGenerator[AsyncClient, None]


@asynccontextmanager
async def client_manager(app, base_url="http://test", **kw) -> ClientManagerType:
    app.state.testing = True
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url=base_url, **kw) as c:
            yield c


@pytest.fixture(scope="module")
async def client() -> ClientManagerType:
    async with client_manager(app) as c:
        yield c


@asynccontextmanager
async def custom_lifespan(app: FastAPI):
    yield


@pytest.mark.anyio
async def test_create_tournaments(client):
    # await Tournament.all().delete()
    tournaments = await Tournament.create(name="test_tournaments")
    tournaments_from_db = await Tournament.get(id=tournaments.id)

    assert tournaments.id == tournaments_from_db.id
    assert tournaments_from_db.name == "test_tournaments"
