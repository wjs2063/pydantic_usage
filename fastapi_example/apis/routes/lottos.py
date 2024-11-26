from fastapi import APIRouter, Request
from aiohttp import ClientSession
from starlette.responses import JSONResponse

from apps.lottos.models import Lotto
import json

lotto_router = APIRouter()


async def get_lotto_number(drwNo: int):
    async with ClientSession() as session:
        async with session.get(f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drwNo}") as resp:
            resp_json = await resp.text()
            resp_json = json.loads(resp_json)
            if resp_json.get("returnValue") == "fail": return None
            lotto = {"drw_no": int(resp_json.get('drwNo')), "drw_no_date": resp_json.get("drwNoDate"),
                     "number_1": resp_json.get("drwtNo1"),
                     "number_2": resp_json.get("drwtNo2"), "number_3": resp_json.get("drwtNo3"),
                     "number_4": resp_json.get("drwtNo4"), "number_5": resp_json.get("drwtNo5"),
                     "number_6": resp_json.get("drwtNo6"), "bonus_number": resp_json.get("bnusNo")}
            return lotto


@lotto_router.get("/")
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
    :return:
    """
    latest_lotto_info = await Lotto.all().order_by('-drw_no').first()
    drwNo = latest_lotto_info.drw_no + 1 if latest_lotto_info else 1
    while True:
        # is_exsist = await Lotto.filter(drw_no=drwNo).exists()
        # if is_exsist: continue
        response = await get_lotto_number(drwNo)
        if response is None: break
        await Lotto.create(**response)
        drwNo += 1
    return JSONResponse(content={"마지막회차": drwNo - 1})
