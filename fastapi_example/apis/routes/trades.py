from fastapi import APIRouter, WebSocket, Request, BackgroundTasks
from aiohttp import ClientSession
from websockets.asyncio.client import connect
import json
from apps.trades.models import MarketTradeInfo
import websockets

trades_router = APIRouter()


async def fetch_upbit_markets(is_details: bool):
    async with ClientSession() as session:
        async with session.get("https://api.upbit.com/v1/market/all", params={"is_details": is_details}) as resp:
            return await resp.json()


async def fetch_upbit_api(api_url: str, params: dict):
    async with ClientSession() as session:
        async with session.get(url=api_url, params=params) as resp:
            return await resp.json()


async def fetch_realtime_trades_info(market_code: str):
    async for websocket in connect("wss://api.upbit.com/websocket/v1",
                                   additional_headers={"codes": [market_code], "type": "ticker"}):
        try:
            await websocket.send(f'[{{"ticket":"test"}},{{"type":"ticker","codes":["{market_code}"]}}]')
            while True:
                resp = await websocket.recv()
                resp = resp.decode("utf-8")
                market_trade_info = MarketTradeInfo(**json.loads(resp))
                await MarketTradeInfo.create(**json.loads(resp))

        except websockets.exceptions.ConnectionClosedOK as e:
            print(e)


@trades_router.get("/market/all")
async def fetch_possible_markets(is_datails=False):
    markets = await fetch_upbit_markets(is_datails)
    return markets


@trades_router.get("/ticker")
async def fetch_order_book(markets: str, level: float = 0):
    api_url = "https://api.upbit.com/v1/orderbook"
    params = {"markets": markets, "level": str(0) if level == 0 else str(level)}
    resp = await fetch_upbit_api(api_url=api_url, params=params)
    return resp


@trades_router.get("/realtime/ws/{market_code}")
async def fetch_realtime_data(request: Request, background_tasks: BackgroundTasks, market_code: str):
    background_tasks.add_task(fetch_realtime_trades_info, market_code=market_code)
    return {"market_code": market_code, "background_task_status": "started!"}
