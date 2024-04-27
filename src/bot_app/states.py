from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_app.open_settings import min_amount


class GoStates(StatesGroup):
    address = State()
    apply = State()
    ban = State()
    bank_name = State()
    btc = State()
    byn = State()
    delete_user = State()
    everybody_users = State()
    everybody_users_coin = State()
    fees = State()
    go = State()
    max_amount = State()
    min_amount = State()
    notification = State()
    pay = State()
    percent = State()
    photo = State()
    photo_ok = State()
    start = State()
    setting = State()
    turn_off = State()
    turn_off_btc = State()
    rate = State()
    requisiters = State()
    usd = State()
    usd_byn = State()
    usdt = State()
    usdt_byn = State()
    user_registred = State()
    wait = State()
    wait_approve = State()
