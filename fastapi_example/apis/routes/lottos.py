from fastapi import APIRouter, Request
from starlette.responses import JSONResponse
from apps.lottos.service.utils import get_lotto_number
from apps.lottos.models import Lotto
import redis.asyncio as redis
from fastapi import Depends
from db.db_config import redis_config, get_redis_client
import json
import random

lotto_router = APIRouter()


@lotto_router.get("/update")
async def update_lotto_number(request: Request):
    """
    drwNoDate : 로또 추첨 일자
    drwNo : 추첨 회차
    drwtNo1 : 첫번째
    drwtNo2 : 두번째
    drwtNo3 : 세번째
    drwtNo4 : 네번째
    drwtNo5 : 다섯번째
    drwtNo6 : 여섯번째
    bnusNo : 보너스
    :param request:
    :return: JSONResponse
    """
    latest_lotto_info = await Lotto.all().order_by('-drw_no').first()
    drwNo = latest_lotto_info.drw_no + 1 if latest_lotto_info else 1
    for _drwNo in range(drwNo, 1300):
        response = await get_lotto_number(_drwNo)
        if response is None: break
        await Lotto.create(**response)
        drwNo += 1
    return JSONResponse(content={"마지막회차": drwNo - 1})


@lotto_router.get("/cache")
async def cache_lotto_datas(request: Request, _redis=Depends(get_redis_client)):
    lotto_store = {num: 0 for num in range(1, 45 + 1)}
    # load lotto_number from db
    lotto_datas = await Lotto.all()
    for lotto_data in lotto_datas:
        lotto_store[lotto_data.number_1] += 1
        lotto_store[lotto_data.number_2] += 1
        lotto_store[lotto_data.number_3] += 1
        lotto_store[lotto_data.number_4] += 1
        lotto_store[lotto_data.number_5] += 1
        lotto_store[lotto_data.number_6] += 1
        lotto_store[lotto_data.bonus_number] += 1
    tot_cnt = sum(lotto_store.values())
    lotto_ratio = {k: v / tot_cnt for k, v in lotto_store.items()}
    await _redis.set("lotto_ratio", json.dumps(lotto_ratio))
    return json.loads(await _redis.get("lotto_ratio"))


@lotto_router.get("/extract-number/naive")
async def extract_lotto_number(request: Request, _redis=Depends(get_redis_client)):
    """
    This API Retunrs naive lotto_number
    로또 통계에 따라 단순 숫자별 확률로 랜덤하게 추출
    :param request:
    :return:
    """
    lotto_latio = await _redis.get("lotto_ratio")
    if lotto_latio is None:
        lotto_latio = await cache_lotto_datas(request=request, _redis=_redis)
    lotto_latio = json.loads(lotto_latio) if isinstance(lotto_latio, bytes) else lotto_latio
    numbers = list(map(int, lotto_latio.keys()))
    probability = list(lotto_latio.values())
    selected_numbers = []
    for _ in range(6):
        chosen = random.choices(numbers, weights=probability, k=1)[0]
        selected_numbers.append(chosen)
        idx = numbers.index(chosen)
        del numbers[idx]
        del probability[idx]

    return sorted(selected_numbers)


@lotto_router.get("/reset-cache")
async def reset_cache(request: Request, _redis=Depends(get_redis_client)):
    await _redis.delete("lotto_ratio")
    return {"msg": "lotto_ratio reset"}
