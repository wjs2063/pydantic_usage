from aiohttp import ClientSession
import json


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
