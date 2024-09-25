from bot_app import currency_usd
from bot_app import open_settings

from decimal import *


def currency_rate(amount=500, btc=0.006):
    try:
        digits = open_settings.byn()
        BTC_USD = currency_usd.currency_rate()
        percent = Decimal((open_settings.percent() / 100) + 1)
        percent_bonus = Decimal((Decimal(open_settings.percent()) - Decimal(0.5)) / 100 + 1)

        if amount >= 500 and btc >= 0.006:
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


def currency_rate_usdt(amount=500, usdt=160):
    try:
        digits = open_settings.byn()
        USDT_USD = 1
        percent = Decimal((open_settings.percent() / 100) + 1)
        percent_bonus = Decimal((Decimal(open_settings.percent()) - Decimal(0.5)) / 100 + 1)

        if amount >= 500 and usdt >= 160:
            byn = (
                Decimal(USDT_USD)
                * Decimal(digits)
                * percent_bonus
            )
        else:
            byn = (
                Decimal(USDT_USD)
                * Decimal(digits)
                * percent
            )

    except:
        byn = "error"
    return byn


def currency_rate_xmr(amount=500, xmr=1):
    try:
        digits = open_settings.byn()
        XMR_USD = currency_usd.currency_rate_xmr()
        percent = Decimal((open_settings.percent() / 100) + 1)
        percent_bonus = Decimal((Decimal(open_settings.percent()) - Decimal(0.5)) / 100 + 1)

        if amount >= 500 and xmr >= 1:
            byn = (
                Decimal(XMR_USD)
                * Decimal(digits)
                * percent_bonus
            )
        else:
            byn = (
                Decimal(XMR_USD)
                * Decimal(digits)
                * percent
            )
    
    except:
        byn = "error"
    return byn
