from datetime import datetime

from tortoise.models import Model
from tortoise import fields


class Lotto(Model):
    id = fields.IntField(pk=True)
    drw_no = fields.IntField()
    number_1 = fields.IntField()
    number_2 = fields.IntField()
    number_3 = fields.IntField()
    number_4 = fields.IntField()
    number_5 = fields.IntField()
    number_6 = fields.IntField()
    bonus_number = fields.IntField()
    drw_no_date = fields.CharField(max_length=256)
    created_at = fields.DatetimeField(auto_now=True)
