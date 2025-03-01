from decimal import *

from bot_app.app import db_settings

# Current bitcoin rate, commission (fees) and percentage


def rate_for_one_bit(name="settings_for_byn"):
    now_rate = db_settings.get_min_rate(name)[0]
    CURRENCY_RATE_FOR_ONE_BITCON = Decimal(now_rate)
    return CURRENCY_RATE_FOR_ONE_BITCON


def fees(name="settings_for_byn"):
    now_fees = db_settings.get_fees(name)[0]
    FEES = Decimal(now_fees)
    return FEES


def percent(name="settings_for_byn"):
    now_percent = db_settings.get_percent(name)[0]
    PERCENT = Decimal(now_percent)
    return PERCENT


def byn(name="settings_for_byn"):
    now_byn = db_settings.get_one_usd_rate(name)[0]
    BYN = Decimal(now_byn)
    return BYN


def min_amount(name="settings_for_byn"):
    min_amount = db_settings.get_min_amount(name)[0]
    MIN = Decimal(min_amount)
    return MIN


def max_amount(name="settings_for_byn"):
    max_amount = db_settings.get_max_amount(name)[0]
    MAX = Decimal(max_amount)
    return MAX
