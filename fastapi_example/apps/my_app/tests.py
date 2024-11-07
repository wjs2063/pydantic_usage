import pytest
from apps.my_app.schema import Tournament_Pydantic
from contextlib import asynccontextmanager
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator, Tuple
from asgi_lifespan import LifespanManager
from pathlib import Path

try:
    from main import app
    # from main_custom_timezone import app as app_east
    from apps.my_app.models import Tournament
except ImportError:
    if (cwd := Path.cwd()) == (parent := Path(__file__).parent):
        dirpath = "."
    else:
        dirpath = str(parent.relative_to(cwd))
    print(f"You may need to explicitly declare python path:\n\nexport PYTHONPATH={dirpath}\n")
    raise

# AsyncGenerator[yield Type , SendType]
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


@pytest.mark.anyio
async def test_home(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


@pytest.mark.anyio
async def test_search_tournaments(client):
    # there is no tournament object in db
    response = await client.get("/tournaments/search/{hello}")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.anyio
async def test_post_tournament(client):
    tournament = await Tournament.create(name="test_tournament")
    tournament_schema = await Tournament_Pydantic.from_tortoise_orm(tournament)
    response = await client.post("/tournaments/", json=tournament_schema.dict())

    assert response.status_code == 201
    assert response.json() == tournament_schema.dict()
