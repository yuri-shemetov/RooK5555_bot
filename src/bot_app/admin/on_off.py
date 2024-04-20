import os

from aiogram import types

from bot_app import messages
from bot_app.app import dp, bot
from bot_app.keybords import inline_answer_to_main, inline_stop
from bot_app.states import GoStates


def get_on_or_off():
    with open("bot_app/admin/settings/on_off.txt", "r") as on_off:
        return on_off.read()

# Turn on service
@dp.callback_query_handler(lambda c: c.data == "turn_on", state=GoStates.setting)
async def button_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    with open("bot_app/admin/settings/on_off.txt", "w", encoding="utf-8") as turn_on:
        turn_on.write("on")

    await bot.send_message(
        callback_query.from_user.id,
        messages.BOT_TURN_ON_ADMIN,
        reply_markup=inline_answer_to_main,
    )


# Turn off service
@dp.callback_query_handler(lambda c: c.data == "turn_off", state=GoStates.setting)
async def button_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    with open("bot_app/admin/settings/on_off.txt", "w", encoding="utf-8") as turn_off:
        turn_off.write("off")

    await bot.send_message(
        callback_query.from_user.id,
        messages.BOT_TURN_OFF_ADMIN,
        reply_markup=inline_answer_to_main,
    )


# ATTANTION FOR STOP BOT SERVER
@dp.callback_query_handler(
    lambda c: c.data == "stop_bot_server", state=GoStates.setting
)
async def button_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        messages.STOP_BOT_SERVER_ATTENTION,
        reply_markup=inline_stop,
    )


# STOP BOT SERVER
@dp.callback_query_handler(lambda c: c.data == "stop", state=GoStates.setting)
async def button_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        messages.STOP_BOT_SERVER,
    )
    await os._exit(0)
