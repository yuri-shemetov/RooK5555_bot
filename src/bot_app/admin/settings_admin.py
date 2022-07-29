from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_app import messages
from bot_app.app import dp, bot
from bot_app.keybords import inline_answer_to_main, inline_setting
from bot_app.states import GoStates


# Setting
@dp.callback_query_handler(lambda c: c.data == "setting", state=GoStates.setting)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    file_rate = open("bot_app/admin/settings/currency_rate.txt")
    now_rate = file_rate.read()
    file_rate.close()

    file_fees = open("bot_app/admin/settings/fees.txt")
    now_fees = file_fees.read()
    file_fees.close()

    file_percent = open("bot_app/admin/settings/percent.txt")
    now_percent = file_percent.read()
    file_percent.close()

    file_byn = open("bot_app/admin/settings/byn.txt")
    now_byn = file_byn.read()
    file_byn.close()

    await bot.send_message(
        callback_query.from_user.id,
        f"Мин. курс: {now_rate} BYN;\nКомиссия: {now_fees} BYN;\nПроцент: {now_percent} %;\n1USD: {now_byn} BYN;"
        + messages.SETTING,
        reply_markup=inline_setting,
    )
    await state.finish()
    await GoStates.rate.set()


# Upload Set_Rate
@dp.callback_query_handler(lambda c: c.data == "rate", state=GoStates.rate)
async def button_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите минимальный курс, BYN")


# Successful Set_Rate
@dp.message_handler(content_types=["text"], state=GoStates.rate)
async def process_message(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["text"] = message.text
            user_message = int(data["text"])
        file = open("bot_app/admin/settings/currency_rate.txt", "w+")
        file.write(f"{user_message}")
        file.close()
        await message.reply("Курс успешно изменен!", reply_markup=inline_answer_to_main)
        await state.finish()
        await GoStates.setting.set()
    except:
        await message.reply("Введите корректно курс")


# Upload Set_Fees
@dp.callback_query_handler(lambda c: c.data == "fees", state=GoStates.rate)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите комиссию, BYN")
    await state.finish()
    await GoStates.fees.set()


# Successful Set_Fees
@dp.message_handler(content_types=["text"], state=GoStates.fees)
async def process_message(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["text"] = message.text
            user_message = float(data["text"])
        file = open("bot_app/admin/settings/fees.txt", "w+")
        file.write(f"{user_message}")
        file.close()
        await message.reply(
            "Комиссия успешно изменена!", reply_markup=inline_answer_to_main
        )
        await state.finish()
        await GoStates.setting.set()
    except:
        await message.reply(
            "Введите корректно коммисию, десятичную дробь пишите только точкой!"
        )


# Upload Set_Persent
@dp.callback_query_handler(lambda c: c.data == "percent", state=GoStates.rate)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите процент, %")
    await state.finish()
    await GoStates.percent.set()


# Successful Set_Fees
@dp.message_handler(content_types=["text"], state=GoStates.percent)
async def process_message(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["text"] = message.text
            user_message = float(data["text"])
        file = open("bot_app/admin/settings/percent.txt", "w+")
        file.write(f"{user_message}")
        file.close()
        await message.reply(
            "Процент успешно изменен!", reply_markup=inline_answer_to_main
        )
        await state.finish()
        await GoStates.setting.set()
    except:
        await message.reply(
            "Введите корректно процент, десятичную дробь пишите только точкой!"
        )


# Upload Set_1USD=BYN
@dp.callback_query_handler(lambda c: c.data == "usd_byn", state=GoStates.rate)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id, "Введите стоимость доллара, BYN"
    )
    await state.finish()
    await GoStates.usd_byn.set()


# Successful Set_1USD=BYN
@dp.message_handler(content_types=["text"], state=GoStates.usd_byn)
async def process_message(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["text"] = message.text
            user_message = float(data["text"])
        file = open("bot_app/admin/settings/byn.txt", "w+")
        file.write(f"{user_message}")
        file.close()
        await message.reply(
            "Курс доллара успешно изменен!", reply_markup=inline_answer_to_main
        )
        await state.finish()
        await GoStates.setting.set()
    except:
        await message.reply(
            "Введите корректный курс, десятичную дробь пишите только точкой!"
        )
