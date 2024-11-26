from pydantic import BaseModel
from datetime import datetime


class LottoSchema(BaseModel):
    detail: str
    number_1: int
    number_2: int
    number_3: int
    number_4: int
    number_5: int
    number_6: int
    bonus_number: int
    created_at: datetime
