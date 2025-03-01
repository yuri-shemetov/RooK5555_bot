from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_app import messages
from bot_app.app import dp, bot, db_settings
from bot_app.keybords import inline_answer_to_main, inline_settings_for_crypto
from bot_app.states import GoStates

NAME = "settings_for_crypto"


# Setting for crypto
@dp.callback_query_handler(lambda c: c.data == NAME, state=GoStates.setting)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)

    result = db_settings.get_full_data(NAME)
    if not result:
        db_settings.add_settings_name(NAME)
        result = db_settings.get_full_data(NAME)

    now_fees, now_percent, now_rate = result[0], result[1], result[2]
    min_amount, max_amount = result[4], result[5]

    await bot.send_message(
        callback_query.from_user.id,
        f"<b>Настройки CRYPTO</b>\n\nМин. курс: {now_rate} USD;\nКомиссия: {now_fees} USD;\nПроцент: {now_percent} %;\
            \nМин. сумма сделки: {min_amount} USD;\nМaкс. сумма сделки: {max_amount} USD"
        + messages.SETTING,
        reply_markup=inline_settings_for_crypto,
        parse_mode="HTML",
        
    )
    await state.finish()
    await GoStates.rate_for_crypto.set()


# Upload Set_Rate
@dp.callback_query_handler(lambda c: c.data == "rate_for_crypto", state=GoStates.rate_for_crypto)
async def button_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите минимальный курс, USD")


# Successful Set_Rate
@dp.message_handler(content_types=["text"], state=GoStates.rate_for_crypto)
async def process_message(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["text"] = message.text
            user_message = int(data["text"])
        db_settings.update_min_rate(user_message, NAME)
        await message.reply("Курс успешно изменен!", reply_markup=inline_answer_to_main)
        await state.finish()
        await GoStates.setting.set()
    except:
        await message.reply("Введите корректно курс")


# Upload Set_Fees
@dp.callback_query_handler(lambda c: c.data == "fees_for_crypto", state=GoStates.rate_for_crypto)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите комиссию, USD")
    await state.finish()
    await GoStates.fees_for_crypto.set()


# Successful Set_Fees
@dp.message_handler(content_types=["text"], state=GoStates.fees_for_crypto)
async def process_message(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["text"] = message.text
            user_message = float(data["text"])
        db_settings.update_fees(user_message, NAME)
        await message.reply(
            "Комиссия успешно изменена!", reply_markup=inline_answer_to_main
        )
        await state.finish()
        await GoStates.setting.set()
    except:
        await message.reply(
            "Введите корректно коммисию, десятичную дробь пишите только точкой!"
        )


# Upload Set pecent
@dp.callback_query_handler(lambda c: c.data == "percent_for_crypto", state=GoStates.rate_for_crypto)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите процент, %")
    await state.finish()
    await GoStates.percent_for_crypto.set()


# Successful Set pecent
@dp.message_handler(content_types=["text"], state=GoStates.percent_for_crypto)
async def process_message(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["text"] = message.text
            user_message = float(data["text"])
        db_settings.update_percent(user_message, NAME)
        await message.reply(
            "Процент успешно изменен!", reply_markup=inline_answer_to_main
        )
        await state.finish()
        await GoStates.setting.set()
    except:
        await message.reply(
            "Введите корректно процент, десятичную дробь пишите только точкой!"
        )


# Upload Set_min_amount
@dp.callback_query_handler(lambda c: c.data == "min_amount_for_crypto", state=GoStates.rate_for_crypto)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id, "Введите минимальную сумму сделки, USD"
    )
    await state.finish()
    await GoStates.min_amount_for_crypto.set()


# Successful Set_min_amount
@dp.message_handler(content_types=["text"], state=GoStates.min_amount_for_crypto)
async def process_message(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["text"] = message.text
            user_message = int(data["text"])
        db_settings.update_min_amount(user_message, NAME)

        await message.reply(
            "Минимальная сумма сделки успешно изменена!",
            reply_markup=inline_answer_to_main,
        )
        await state.finish()
        await GoStates.setting.set()
    except:
        await message.reply("Введите корректно сумму")


# Upload Set_max_amount
@dp.callback_query_handler(lambda c: c.data == "max_amount_for_crypto", state=GoStates.rate_for_crypto)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id, "Введите максимальную сумму сделки, USD"
    )
    await state.finish()
    await GoStates.max_amount_for_crypto.set()


# Successful Set_max_amount
@dp.message_handler(content_types=["text"], state=GoStates.max_amount_for_crypto)
async def process_message(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["text"] = message.text
            user_message = int(data["text"])
        db_settings.update_max_amount(user_message, NAME)

        await message.reply(
            "Максимальная сумма сделки успешно изменена!",
            reply_markup=inline_answer_to_main,
        )
        await state.finish()
        await GoStates.setting.set()
    except:
        await message.reply("Введите корректно сумму")
