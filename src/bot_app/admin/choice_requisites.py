from aiogram import types
from aiogram.dispatcher import FSMContext
from datetime import datetime

from bot_app import messages
from bot_app.app import dp, bot, db_bank
from bot_app.keybords import (
    inline_answer_for_requisiters, 
    inline_answer_to_main, 
    inline_answer_for_requisiters_add, 
    inline_answer_for_is_only_day, 
    inline_answer_for_question_admin
)
from bot_app.states import GoStates


CONTENT_TYPES = [
    "audio",
    "document",
    "photo",
    "sticker",
    "video",
    "video_note",
    "voice",
    "location",
    "contact",
    "new_chat_members",
    "left_chat_member",
    "new_chat_title",
    "new_chat_photo",
    "delete_chat_photo",
    "group_chat_created",
    "supergroup_chat_created",
    "channel_chat_created",
    "migrate_to_chat_id",
    "migrate_from_chat_id",
    "pinned_message",
]


def get_requisiters():
    try:
        is_only_day = True if 8 <= datetime.now().hour < 21 else False
        requisiters_and_amount = db_bank.get_full_data(is_only_day)
        result = min(requisiters_and_amount, key = lambda item: item[2])
        requisiters, name_bank = result[0], result[3]
    except ValueError:
        requisiters, name_bank = "Реквизиты банка не установлены!\nЗа реквизитами обратитесь, пожалуйста,  обратитесь к @RooK5555", ""
    return requisiters, name_bank


def get_full_data():
    try:
        requisiters = db_bank.get_full_data()
    except ValueError:
        requisiters = "Реквизиты банка не установлены!\nЗа реквизитами обратитесь, пожалуйста,  обратитесь к @RooK5555"
    return requisiters


# Show setting requisites
@dp.callback_query_handler(lambda c: c.data == "applications", state=GoStates.setting)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)

    now_requisiters = get_full_data()
    for index, item in enumerate(now_requisiters, start=1):
        is_only_day = "08.00-21.00" if item[1] else "Круглосуточно"
        await bot.send_message(
            callback_query.from_user.id,
            messages.TEXT_FOR_REQUISITERS_ONE_BANK.format(index, item[3], item[2], is_only_day, item[0]),
            parse_mode="HTML",
        )
    await bot.send_message(
        callback_query.from_user.id,
        messages.TEXT_FOR_REQUISITERS.format(len(now_requisiters)),
        reply_markup=inline_answer_for_requisiters,
        parse_mode="HTML",
    )
    await state.finish()
    await GoStates.bank_name.set()


# Add bank name
@dp.callback_query_handler(
    lambda c: c.data == "requisiters_add", state=GoStates.bank_name
)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, messages.TEXT_FOR_BANK_NAME)
    await state.finish()
    await GoStates.bank_name.set()


# Successful a bank name add
@dp.message_handler(content_types=["text"], state=GoStates.bank_name)
async def process_message(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data["text"] = message.text
        bank_name = str(data["text"]).title()
    
    is_exists = db_bank.get_name_bank(bank_name)
    if is_exists or len(bank_name) > 30:
        msg = (
            messages.THE_BANK_NAME_IS_EXISTS.format(bank_name) 
            if is_exists 
            else messages.THE_MESSAGE_IS_TOO_LONG.format(len(bank_name))
        )
        await bot.send_message(
            message.from_user.id,
            msg,
            reply_markup=inline_answer_to_main,
            parse_mode="HTML",
        )
        await state.finish()
        await GoStates.setting.set()
    else:
        db_bank.add_bank_name(bank_name, "new")
        await bot.send_message(
            message.from_user.id,
            messages.BANK_NAME_SUCCESSFULLY.format(bank_name),
            parse_mode="HTML",
            reply_markup=inline_answer_for_requisiters_add,
        )

        await state.finish()
        await GoStates.requisiters.set()


# Add requisiters
@dp.callback_query_handler(
    lambda c: c.data == "requisiters_yes", state=GoStates.requisiters
)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, messages.TEXT_FOR_REMINDER)


# Successful requisiters add
@dp.message_handler(content_types=["text"], state=GoStates.requisiters)
async def process_message(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data["text"] = message.text
        message_requisiters = data["text"]

    db_bank.update_requisiters(message_requisiters)

    await bot.send_message(
        message.from_user.id,
        messages.IS_ONLY_DAY,
        reply_markup=inline_answer_for_is_only_day,
        parse_mode="HTML",
    )

    await state.finish()
    await GoStates.is_only_day.set()


# is not 24/7
@dp.callback_query_handler(lambda c: c.data == "is_only_day_yes", state=GoStates.is_only_day)
async def button_click_call_back(callback_query: types.CallbackQuery):
    db_bank.update_is_only_day(True)
    await callback_query.answer()
    await bot.send_message(
        callback_query.from_user.id,
        messages.REQUISITERS_SUCCESSFULLY,
        parse_mode="HTML",
        reply_markup=inline_answer_to_main,
    )

    await GoStates.setting.set()

# is 24/7
@dp.callback_query_handler(lambda c: c.data == "is_only_day_no", state=GoStates.is_only_day)
async def button_click_call_back(callback_query: types.CallbackQuery):
    db_bank.update_is_only_day(False)
    await callback_query.answer()
    await bot.send_message(
        callback_query.from_user.id,
        messages.REQUISITERS_SUCCESSFULLY,
        parse_mode="HTML",
        reply_markup=inline_answer_to_main,
    )

    await GoStates.setting.set()


# Remove bank name
@dp.callback_query_handler(
    lambda c: c.data == "remove_bank_name", state=GoStates.bank_name
)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Удаляем реквизиты!\n" + messages.TEXT_FOR_BANK_NAME)
    await state.finish()
    await GoStates.remove_requisiters_bank.set()


# Remove requisiters bank
@dp.message_handler(content_types=["text"], state=GoStates.remove_requisiters_bank)
async def process_message(message: types.Message, state: FSMContext):

    try:
        async with state.proxy() as data:
            data["text"] = message.text
            name_bank = str(data["text"]).title()
        db_bank.remove_requisiters(name_bank)

        await bot.send_message(
            message.from_user.id,
            messages.REMOVE_REQUISITERS_SUCCESSFULLY.format(name_bank),
            reply_markup=inline_answer_to_main,
            parse_mode="HTML",
        )
    except Exception as exc:
        if "no such column: name_bank" in str(exc):
            await bot.send_message(
                message.from_user.id,
                messages.REMOVE_REQUISITERS_UNSUCCESSFULLY.format(name_bank),
                reply_markup=inline_answer_to_main,
                parse_mode="HTML",
            )

    await state.finish()
    await GoStates.setting.set()


# question for resetting the amount to zero
@dp.callback_query_handler(
    lambda c: c.data == "bank_zero_question", state=GoStates.bank_name
)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id, 
        messages.TEXT_FOR_BANK_THE_AMOUNT_ZERO, 
        reply_markup=inline_answer_for_question_admin
    )
    await state.finish()
    await GoStates.bank_zero.set()


# resetting the amount to zero
@dp.callback_query_handler(
    lambda c: c.data == "answer_yes", state=GoStates.bank_zero
)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    db_bank.update_amount_zero()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id, 
        messages.TEXT_FOR_BANK_THE_AMOUNT_ZERO_SUCCESSFULLY, 
        reply_markup=inline_answer_to_main
    )
    await state.finish()
    await GoStates.bank_zero.set()


# Error bank name add
@dp.message_handler(content_types=CONTENT_TYPES, state=GoStates.bank_name)
async def process_address_invalid(message: types.Message):
    await message.reply(messages.ERROR_MESSAGE_FOR_BANK_NAME)


# Error requisiters add
@dp.message_handler(content_types=CONTENT_TYPES, state=GoStates.requisiters)
async def process_address_invalid(message: types.Message):
    await message.reply(messages.REQUISITERS_ERROR_MESSAGE)




# # Successful requisiters upload
# @dp.message_handler(content_types=["text"], state=GoStates.requisiters)
# async def process_message(message: types.Message, state: FSMContext):

#     async with state.proxy() as data:
#         data["text"] = message.text
#         message_requisiters = data["text"]

#     with open(
#         "bot_app/admin/settings/requisiters.txt", "w", encoding="utf-8"
#     ) as file_users:
#         file_users.write(message_requisiters)
#     with open(
#         "bot_app/admin/settings/requisiters.txt", "r", encoding="utf-8"
#     ) as file_users:
#         now_requisiters = file_users.read()

#     with open("bot_app/admin/settings/byn_balance.txt", "w+") as file_byn:    
#         file_byn.write(f"0")

#     await bot.send_message(message.from_user.id, f"{now_requisiters}")
#     await bot.send_message(
#         message.from_user.id,
#         messages.REQUISITERS_SUCCESSFULLY,
#         parse_mode="HTML",
#         reply_markup=inline_answer_to_main,
#     )

#     await state.finish()
#     await GoStates.setting.set()


# Successful a bank name upload
# @dp.message_handler(content_types=["text"], state=GoStates.bank_name)
# async def process_message(message: types.Message, state: FSMContext):

#     async with state.proxy() as data:
#         data["text"] = message.text
#         message_bank_name = data["text"]

#     with open(
#         "bot_app/admin/settings/name_bank.txt", "w", encoding="utf-8"
#     ) as file_bank_name:
#         file_bank_name.write(message_bank_name)
#     with open(
#         "bot_app/admin/settings/name_bank.txt", "r", encoding="utf-8"
#     ) as file_bank_name:
#         bank_name = file_bank_name.read()

#     await bot.send_message(
#         message.from_user.id,
#         messages.BANK_NAME_SUCCESSFULLY.format(bank_name),
#         parse_mode="HTML",
#         reply_markup=inline_answer_to_main,
#     )

#     await state.finish()
#     await GoStates.setting.set()