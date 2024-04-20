from aiogram import types

from bot_app import messages
from bot_app.app import dp, bot
from bot_app.keybords import inline_answer_to_main, inline_answer_to_settings_crypto
from bot_app.states import GoStates


def get_btc_state():
    with open("bot_app/admin/settings/btc_state.txt", "r") as on_off:
        return on_off.read() == 'on'


# Settings Crypto
@dp.callback_query_handler(lambda c: c.data == "settings_crypto", state=GoStates.setting)
async def button_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        "Управление включения и выключения обмена монет",
        reply_markup=inline_answer_to_settings_crypto,
    )


# Turn on BTC
@dp.callback_query_handler(lambda c: c.data == "turn_on_btc", state=GoStates.setting)
async def button_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    with open("bot_app/admin/settings/btc_state.txt", "w", encoding="utf-8") as turn_on:
        turn_on.write("on")

    await bot.send_message(
        callback_query.from_user.id,
        messages.BOT_TURN_ON_BTC,
        reply_markup=inline_answer_to_main,
    )


# Turn off BTC
@dp.callback_query_handler(lambda c: c.data == "turn_off_btc", state=GoStates.setting)
async def button_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    with open("bot_app/admin/settings/btc_state.txt", "w", encoding="utf-8") as turn_off:
        turn_off.write("off")

    await bot.send_message(
        callback_query.from_user.id,
        messages.BOT_TURN_OFF_BTC,
        reply_markup=inline_answer_to_main,
    )

