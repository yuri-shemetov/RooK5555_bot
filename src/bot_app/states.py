from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_app.open_settings import min_amount


class GoStates(StatesGroup):
    address = State()
    apply = State()
    ban = State()
    btc = State()
    byn = State()
    everybody_users = State()
    fees = State()
    go = State()
    max_amount = State()
    min_amount = State()
    pay = State()
    percent = State()
    photo = State()
    photo_ok = State()
    start = State()
    setting = State()
    turn_off = State()
    rate = State()
    requisiters = State()
    usd = State()
    usd_byn = State()
    user_registred = State()
    wait = State()
    wait_approve = State()
