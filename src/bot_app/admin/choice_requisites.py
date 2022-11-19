from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_app import messages
from bot_app.app import dp, bot
from bot_app.keybords import inline_answer_for_requisiters, inline_answer_to_main
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
    with open(
        "bot_app/admin/settings/requisiters.txt", "r", encoding="utf-8"
    ) as requisiters:
        return requisiters.read()

def get_name_bank():
    with open(
        "bot_app/admin/settings/name_bank.txt", "r", encoding="utf-8"
    ) as name_bank:
        return name_bank.read()


# Show setting requisites
@dp.callback_query_handler(lambda c: c.data == "applications", state=GoStates.setting)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)

    with open(
        "bot_app/admin/settings/requisiters.txt", "r", encoding="utf-8"
    ) as file_req:
        now_requisiters = file_req.read()
    with open(
        "bot_app/admin/settings/name_bank.txt", "r", encoding="utf-8"
    ) as file_bank:
        name_bank = file_bank.read()
    await bot.send_message(
        callback_query.from_user.id,
        messages.TEXT_FOR_REQUISITERS.format(now_requisiters, name_bank),
        reply_markup=inline_answer_for_requisiters,
        parse_mode="HTML",
    )
    await state.finish()
    await GoStates.requisiters.set()


# Upload requisiters
@dp.callback_query_handler(
    lambda c: c.data == "requisiters_yes", state=GoStates.requisiters
)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, messages.TEXT_FOR_REMINDER)


# Upload a bank
@dp.callback_query_handler(
    lambda c: c.data == "bank_yes", state=GoStates.requisiters
)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, messages.TEXT_FOR_BANK_NAME)
    await state.finish()
    await GoStates.bank_name.set()


# Error requisiters upload
@dp.message_handler(content_types=CONTENT_TYPES, state=GoStates.requisiters)
async def process_address_invalid(message: types.Message):
    await message.reply(messages.REQUISITERS_ERROR_MESSAGE)


# Error requisiters upload
@dp.message_handler(content_types=CONTENT_TYPES, state=GoStates.bank_name)
async def process_address_invalid(message: types.Message):
    await message.reply(messages.ERROR_MESSAGE_FOR_BANK_NAME)


# Successful requisiters upload
@dp.message_handler(content_types=["text"], state=GoStates.requisiters)
async def process_message(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data["text"] = message.text
        message_requisiters = data["text"]

    with open(
        "bot_app/admin/settings/requisiters.txt", "w", encoding="utf-8"
    ) as file_users:
        file_users.write(message_requisiters)
    with open(
        "bot_app/admin/settings/requisiters.txt", "r", encoding="utf-8"
    ) as file_users:
        now_requisiters = file_users.read()

    with open("bot_app/admin/settings/byn_balance.txt", "w+") as file_byn:    
        file_byn.write(f"0")

    await bot.send_message(message.from_user.id, f"{now_requisiters}")
    await bot.send_message(
        message.from_user.id,
        messages.REQUISITERS_SUCCESSFULLY,
        parse_mode="HTML",
        reply_markup=inline_answer_to_main,
    )

    await state.finish()
    await GoStates.setting.set()


# Successful a bank name upload
@dp.message_handler(content_types=["text"], state=GoStates.bank_name)
async def process_message(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data["text"] = message.text
        message_bank_name = data["text"]

    with open(
        "bot_app/admin/settings/name_bank.txt", "w", encoding="utf-8"
    ) as file_bank_name:
        file_bank_name.write(message_bank_name)
    with open(
        "bot_app/admin/settings/name_bank.txt", "r", encoding="utf-8"
    ) as file_bank_name:
        bank_name = file_bank_name.read()

    await bot.send_message(
        message.from_user.id,
        messages.BANK_NAME_SUCCESSFULLY.format(bank_name),
        parse_mode="HTML",
        reply_markup=inline_answer_to_main,
    )

    await state.finish()
    await GoStates.setting.set()