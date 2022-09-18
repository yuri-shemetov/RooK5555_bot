from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_app import messages
from bot_app.app import dp, bot
from bot_app.keybords import inline_answer_for_notification, inline_answer_to_main
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


# Show message for notification
@dp.callback_query_handler(lambda c: c.data == "notification", state=GoStates.setting)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)

    await bot.send_message(
        callback_query.from_user.id,
        messages.TEXT_FOR_NOTIFICATION_START,
        reply_markup=inline_answer_for_notification,)

    await state.finish()
    await GoStates.notification.set()


# Write the message
@dp.callback_query_handler(
    lambda c: c.data == "notification_yes", state=GoStates.notification
)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, messages.TEXT_FOR_NOTIFICATION)
    


# Error requisiters upload
@dp.message_handler(content_types=CONTENT_TYPES, state=GoStates.notification)
async def process_address_invalid(message: types.Message):
    await message.reply(messages.NOTIFICATION_ERROR_MESSAGE)


# Successful requisiters upload
@dp.message_handler(content_types=["text"], state=GoStates.notification)
async def process_message(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data["text"] = message.text
        notification = data["text"]

    with open(
        "bot_app/admin/settings/registered_users.txt", "r", encoding="utf-8"
    ) as file_users:
        users_string = file_users.read()

    users = users_string.split()
    for user in users:
        try:
            await bot.send_message(
                int(user),
                notification,
                parse_mode="HTML",
            )
        except:
            pass

    await bot.send_message(
        message.from_user.id,
        messages.NOTIFICATION_SUCCESSFULLY,
        parse_mode="HTML",
        reply_markup=inline_answer_to_main,
    )

    await state.finish()
    await GoStates.setting.set()