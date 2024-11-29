import pytest
from contextlib import asynccontextmanager
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator, Tuple
from asgi_lifespan import LifespanManager
from pathlib import Path
from apps.lottos.models import Lotto
from unittest.mock import patch
from unittest import IsolatedAsyncioTestCase

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


# @pytest.mark.anyio
# async def test_lotto_update(client):
#     lotto = {"drw_no": 1, "drw_no_date": "test_date",
#              "number_1": 1,
#              "number_2": 2, "number_3": 3,
#              "number_4": 4, "number_5": 5,
#              "number_6": 6, "bonus_number": 7}
#     await Lotto.create(**lotto)
#     response = await client.get("/lotto/update")
#     assert response.status_code == 200


class TestLotto(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client_manager = client_manager(app)
        self.client = await self.client_manager.__aenter__()


    # 주의 할점 : 대상 함수가있는경로가아니라, 대상함수를 사용하는 경로를 지정해주어야한다.
    @patch("apis.routes.lottos.get_lotto_number",return_value=None)
    async def test_lotto_update(self, mock_get_lotto_number):
        assert None == mock_get_lotto_number.return_value
        lotto_1 = {"drw_no": 1, "drw_no_date": "test_date1",
                 "number_1": 1,
                 "number_2": 2, "number_3": 3,
                 "number_4": 4, "number_5": 5,
                 "number_6": 6, "bonus_number": 7}
        lotto_2 = {"drw_no": 2, "drw_no_date": "test_date2",
                 "number_1": 1,
                 "number_2": 2, "number_3": 3,
                 "number_4": 4, "number_5": 5,
                 "number_6": 6, "bonus_number": 7}
        await Lotto.create(**lotto_1)
        await Lotto.create(**lotto_2)
        response = await self.client.get("/lotto/update")
        assert response.status_code == 200
        assert response.json() == {"마지막회차": 2}
    async def test_hello(self):
        assert 1 == 1
