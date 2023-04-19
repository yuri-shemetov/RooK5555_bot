import imp
from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_app import currency_usd
from bot_app import messages
from bot_app import open_settings
from bot_app.app import dp, bot, db
from bot_app.keybords import inline_answer, inline_cancel
from bot_app.states import GoStates
from bot_app.currency_byn import currency_rate
from bot_app.open_settings import min_amount, max_amount
from bot_app.transactions import get_balance_bitcoins

from datetime import datetime
from decimal import *
from time import time


@dp.callback_query_handler(lambda c: c.data == "btc", state=GoStates.go)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await callback_query.answer()
    await bot.send_message(
        callback_query.from_user.id, f"Введите количество биткоинов, BTC:"
    )
    await state.finish()
    await GoStates.btc.set()


# Here we get the response by indicating the state and passing the user's message
@dp.message_handler(state=GoStates.btc)
async def process_message(message: types.Message, state: FSMContext):
    if currency_rate() != "error":
        try:
            async with state.proxy() as data:
                data["text"] = message.text
                user_message = data["text"]
            BTC_BYN = currency_rate(btc=Decimal(user_message))
            MIN_BYN = min_amount()
            MIN_BTC = round(
                Decimal((MIN_BYN - Decimal(open_settings.fees()) - Decimal(0.5)) / BTC_BYN),
                8,
            )
            MAX_BYN = max_amount()
            MAX_BTC = round(
                Decimal(
                    (MAX_BYN - Decimal(open_settings.fees()) - Decimal(0.5)) / BTC_BYN
                ),
                8,
            )
            if Decimal(user_message) >= MIN_BTC and Decimal(user_message) <= MAX_BTC:
                
                balance = get_balance_bitcoins()

                BTC_USD = currency_usd.currency_rate()
                ONE_BIT = round(Decimal(3 / BTC_USD), 8)

                if (Decimal(user_message) + Decimal(ONE_BIT)) <= Decimal(balance):
                    money = round(
                        Decimal(user_message) * Decimal(BTC_BYN)
                        + Decimal(open_settings.fees())
                        + Decimal(0.5),
                        0,
                    )

                    await bot.send_message(
                        message.from_user.id,
                        messages.COST_BTC.format(money),
                        reply_markup=inline_answer,
                        parse_mode="HTML",
                    )

                    # Finish conversation
                    await state.finish()
                    await GoStates.pay.set()

                    if not db.subscriber_exists(message.from_user.id):
                        # Add user
                        db.add_subscriber(
                            message.from_user.id,
                            rate="BTC",
                            price=str(money),
                            translation=user_message,
                            created=str(datetime.now().strftime("%d/%m/%y-%H:%M:%S")),
                            start_timestamp = int(time()),
                        )
                    else:
                        # If user has to DB that update his
                        db.update_subscription(
                            message.from_user.id,
                            rate="BTC",
                            price=str(money),
                            translation=user_message,
                            created=str(datetime.now().strftime("%d/%m/%y-%H:%M:%S")),
                            start_timestamp = int(time()),
                        )
                else:
                    await message.reply(
                        messages.BALANCE_BIT_MESSAGE,
                        reply_markup=inline_cancel,
                    )

            elif Decimal(user_message) > MAX_BTC:
                await message.reply(
                    f"Количество биткоинов должно быть не более {MAX_BTC} BTC (Нужно больше BTC - обращайся к @RooK5555):"
                )
            else:
                await message.reply(
                    f"Количество биткоинов должно быть не менее {MIN_BTC} BTC. "
                )
        except:
            await message.reply(
                f"Введите корректную сумму (десятичную часть отделяйте только точкой!): "
            )
    else:
        await message.reply(messages.SERVER_ERROR)
