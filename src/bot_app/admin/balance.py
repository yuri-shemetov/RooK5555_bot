from aiogram import types

from bot_app.app import dp, bot
from bot_app.keybords import inline_answer_to_main
from bot_app.states import GoStates
from bot_app.transactions import get_balance_bitcoins


# Balance BTC
@dp.callback_query_handler(lambda c: c.data == "balance", state=GoStates.setting)
async def button_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    balance = get_balance_bitcoins()

    await bot.send_message(
        callback_query.from_user.id,
        f"Текущий баланс: {balance} BTC",
        reply_markup=inline_answer_to_main,
    )
