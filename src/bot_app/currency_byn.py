from bot_app import currency_usd
from bot_app import open_settings

from decimal import *


def currency_rate(amount=500, btc=0.0055):
    try:
        digits = open_settings.byn()
        BTC_USD = currency_usd.currency_rate()
        percent = Decimal((open_settings.percent() / 100) + 1)
        percent_bonus = Decimal((open_settings.percent() - 1) / 100 + 1)

        if amount > 500 or btc > 0.0055:
            byn = (
                Decimal(BTC_USD)
                * Decimal(digits)
                * percent_bonus
            )
        else:
            byn = (
                Decimal(BTC_USD)
                * Decimal(digits)
                * percent
            )

        if Decimal(byn) <= Decimal(open_settings.rate_for_one_bit()):
            byn = open_settings.rate_for_one_bit()
    except:
        byn = "error"
    return byn
