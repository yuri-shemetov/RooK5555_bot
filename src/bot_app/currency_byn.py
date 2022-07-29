from bot_app import currency_usd
from bot_app import open_settings

from decimal import *


def currency_rate():
    try:
        digits = open_settings.byn()
        BTC_USD = currency_usd.currency_rate()
        byn = (
            Decimal(BTC_USD)
            * Decimal(digits)
            * Decimal((open_settings.percent() / 100) + 1)
        )
        if Decimal(byn) <= Decimal(open_settings.rate_for_one_bit()):
            byn = open_settings.rate_for_one_bit()
    except:
        byn = "error"
    return byn
