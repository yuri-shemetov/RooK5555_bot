from decimal import *

# Current bitcoin rate, commission (fees) and percentage


def rate_for_one_bit():
    with open("bot_app/admin/settings/currency_rate.txt", "r") as file_rate:
        now_rate = file_rate.read()
        CURRENCY_RATE_FOR_ONE_BITCON = Decimal(now_rate)
    return CURRENCY_RATE_FOR_ONE_BITCON


def fees():
    with open("bot_app/admin/settings/fees.txt", "r") as file_fees:
        now_fees = file_fees.read()
        FEES = Decimal(now_fees)
    return FEES


def percent():
    with open("bot_app/admin/settings/percent.txt", "r") as file_percent:
        now_percent = file_percent.read()
        PERCENT = Decimal(now_percent)
    return PERCENT


def byn():
    with open("bot_app/admin/settings/byn.txt", "r") as file_byn:
        now_byn = file_byn.read()
        BYN = Decimal(now_byn)
    return BYN
