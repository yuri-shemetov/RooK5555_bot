import imp
from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_app import currency_usd
from bot_app import messages
from bot_app import open_settings
from bot_app.app import dp, bot, db
from bot_app.keybords import inline_answer, inline_cancel
from bot_app.states import GoStates
from bot_app.currency_byn import currency_rate_usdt
from bot_app.open_settings import min_amount, max_amount
from bot_app import transactions_usdt

from datetime import datetime
from decimal import *
from time import time


@dp.callback_query_handler(lambda c: c.data == "usdt", state=GoStates.go)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await callback_query.answer()
    await bot.send_message(
        callback_query.from_user.id, f"Введите количество Tether, USDT:"
    )
    await state.finish()
    await GoStates.usdt.set()


# Here we get the response by indicating the state and passing the user's message
@dp.message_handler(state=GoStates.usdt)
async def process_message(message: types.Message, state: FSMContext):
    if currency_rate_usdt() != "error":
        try:
            async with state.proxy() as data:
                data["text"] = message.text
                user_message = data["text"]
            USDT_BYN = currency_rate_usdt(usdt=Decimal(user_message))
            MIN_BYN = min_amount()
            MIN_USDT = round(
                Decimal((MIN_BYN - Decimal(open_settings.fees()) - Decimal(0.5)) / USDT_BYN),
                0,
            )
            MAX_BYN = max_amount()
            MAX_USDT = round(
                Decimal(
                    (MAX_BYN - Decimal(open_settings.fees()) - Decimal(0.5)) / USDT_BYN
                ),
                0,
            )
            if Decimal(user_message) >= MIN_USDT and Decimal(user_message) <= MAX_USDT:
                balance = transactions_usdt.get_balance()

                if (Decimal(user_message) + Decimal(3)) <= Decimal(balance):
                    money = round(
                        Decimal(user_message) * Decimal(USDT_BYN)
                        + Decimal(open_settings.fees())
                        + Decimal(0.5),
                        0,
                    )

                    await bot.send_message(
                        message.from_user.id,
                        messages.COST_USDT.format(money),
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
                            rate="USDT",
                            price=str(money),
                            translation=user_message,
                            created=str(datetime.now().strftime("%d/%m/%y-%H:%M:%S")),
                            start_timestamp = int(time()),
                        )
                    else:
                        # If user has to DB that update his
                        db.update_subscription(
                            message.from_user.id,
                            rate="USDT",
                            price=str(money),
                            translation=user_message,
                            created=str(datetime.now().strftime("%d/%m/%y-%H:%M:%S")),
                            start_timestamp = int(time()),
                        )
                else:
                    await message.reply(
                        messages.BALANCE_USDT_MESSAGE,
                        reply_markup=inline_cancel,
                    )

            elif Decimal(user_message) > MAX_USDT:
                await message.reply(
                    f"Количество Tether должно быть не более {MAX_USDT} USDT(Нужно больше - обращайся к @RooK5555):"
                )
            else:
                await message.reply(
                    f"Количество Tether должно быть не менее {MIN_USDT} USDT"
                )
        except:
            await message.reply(
                f"Введите корректную сумму (только целые числа): "
            )
    else:
        await message.reply(messages.SERVER_ERROR)
