from tortoise.models import Model
from tortoise import fields


class MarketTradeInfo(Model):
    id = fields.BigIntField(pk=True)
    type = fields.CharField(max_length=256, null=True)
    code = fields.CharField(max_length=256, null=True)
    opening_price = fields.FloatField(null=True)
    high_price = fields.FloatField(null=True)
    low_price = fields.FloatField(null=True)
    trade_price = fields.FloatField(null=True)
    prev_closing_price = fields.FloatField(null=True)
    acc_trade_price = fields.FloatField(null=True)
    change = fields.CharField(max_length=256, null=True)
    signed_change = fields.CharField(max_length=256, null=True)
    change_rate = fields.FloatField(null=True)
    signed_change_rate = fields.FloatField(null=True)
    ask_bid = fields.CharField(max_length=256, null=True)
    trade_volume = fields.FloatField(null=True)
    acc_trade_volume = fields.FloatField(null=True)
    trade_date = fields.BigIntField( null=True)
    trade_time = fields.BigIntField( null=True)
    trade_timestamp = fields.BigIntField( null=True)
    acc_ask_volume = fields.FloatField(null=True)
    acc_bid_volume = fields.FloatField(null=True)
    highest_52_week_price = fields.FloatField(null=True)
    highest_52_week_date = fields.CharField(max_length=256, null=True)
    lowest_52_week_price = fields.FloatField(null=True)
    lowest_52_week_date = fields.CharField(max_length=256, null=True)
    market_state = fields.CharField(max_length=256, null=True)
    delisting_date = fields.BigIntField( null=True)
    market_warning = fields.CharField(max_length=256, null=True)
    timestamp = fields.BigIntField( null=True)
    acc_trade_price_24h = fields.FloatField(null=True)
    acc_trade_volume_24h = fields.FloatField(null=True)
    stream_type = fields.CharField(max_length=256, null=True)
    def __str__(self):
        return f"{self.code}, {self.trade_price}"
