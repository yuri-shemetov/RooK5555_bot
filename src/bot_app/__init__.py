import logging

from bot_app import commands, byn, btc
from bot_app.admin import (
    settings_admin,
    choice_by_admin,
    choice_requisites,
    balance,
)
from bot_app.app import dp


logging.basicConfig(level=logging.INFO)