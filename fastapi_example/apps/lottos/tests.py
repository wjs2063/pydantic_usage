import pytest
from contextlib import asynccontextmanager
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator, Tuple
from asgi_lifespan import LifespanManager
from pathlib import Path
from apps.lottos.models import Lotto

try:
    from main import app
    # from main_custom_timezone import app as app_east
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
async def test_lotto_update(client):
    lotto = {"drw_no": 1, "drw_no_date": "test_date",
             "number_1": 1,
             "number_2": 2, "number_3": 3,
             "number_4": 4, "number_5": 5,
             "number_6": 6, "bonus_number": 7}
    await Lotto.create(**lotto)
    response = await client.get("/lotto/update")
    assert response.status_code == 200
