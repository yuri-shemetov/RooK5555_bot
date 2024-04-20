import logging

from bot_app import commands, byn, btc, usdt, byn_usdt
from bot_app.admin import (
    balance,
    black_list,
    users_list,
    choice_by_admin,
    choice_requisites,
    notification,
    settings_admin,
)
from bot_app.app import dp


logging.basicConfig(level=logging.INFO)