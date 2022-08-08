from bot_app import open_settings
from bot_app.currency_byn import currency_rate

from decimal import *



def info_currency():
    BTC_BYN = currency_rate()  
    user_message = 1

    currency = round(
        Decimal(user_message) * Decimal(BTC_BYN)
        + Decimal(open_settings.fees())
        + Decimal(0.5),
        0,
    )
    return currency