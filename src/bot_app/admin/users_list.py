import datetime, time

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_app import messages
from bot_app.app import dp, bot, db
from bot_app.keybords import inline_users, inline_answer_to_main
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


def get_registered_users():
    with open("bot_app/admin/settings/registered_users.txt", "r") as registered_users:
        return registered_users.read()


def get_ban_users():
    with open("bot_app/admin/settings/ban_users.txt", "r") as registered_users:
        return registered_users.read()


# Check all registered users on the date of using the application
@dp.callback_query_handler(lambda c: c.data == "check_users", state=GoStates.setting)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    users_list = [int(x) for x in get_registered_users().split()]

    with open(
        "bot_app/admin/settings/registered_users.txt", "r", encoding="utf-8"
    ) as file_users:
        users_string = file_users.read()

    users = users_string.split()
    users_dict = {}

    for user in users:
        try:
            date = db.get_subscriptions_created(user)[0][0]
            date = date[:6] + "20" + date[6:]
            dt = datetime.datetime.strptime(date, "%d/%m/%Y-%H:%M:%S")
            date_timestamp = dt.timestamp()
            users_dict[user] = date_timestamp
        except:
            pass

    now = round(time.time(), 0)
    period = 7776000 # 3 month
    report_list = []

    for id, timestamp in users_dict.items():
        if (now - int(timestamp)) > period:
            report_list.append(id)
    
    if report_list:
        await bot.send_message(
        callback_query.from_user.id,
        messages.USERS_MORE_3_MONTH.format(len(users_list), report_list),
        parse_mode="HTML",
        reply_markup=inline_users,
    )
    else:
        await bot.send_message(
        callback_query.from_user.id,
        messages.NO_USERS_3_MONTH.format(len(users_list)),
        parse_mode="HTML",
        reply_markup=inline_users,
    )


# Delete the user
@dp.callback_query_handler(lambda c: c.data == "delete_user", state=GoStates.setting)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, messages.ENTER_ID_USER)
    await state.finish()
    await GoStates.delete_user.set()


# Error delete the user
@dp.message_handler(content_types=CONTENT_TYPES, state=GoStates.delete_user)
async def process_address_invalid(message: types.Message):
    await message.reply(messages.ENTER_CORRECT_ID_USER)


# Successful delete the user
@dp.message_handler(content_types=["text"], state=GoStates.delete_user)
async def process_message(message: types.Message, state: FSMContext):
    user_id = message.text
    users_list = [int(x) for x in get_registered_users().split()]
    users_string = ""

    if user_id.isdigit():
        user_id = int(user_id)
        if user_id in users_list:
            users_list.remove(user_id)
            for user in users_list:
                users_string += " " + str(user)
            with open("bot_app/admin/settings/registered_users.txt", "w") as file_users:
                file_users.write(users_string)

            await bot.send_message(
                message.from_user.id,
                messages.SUCCESSFULLY_DELETED_USER.format(user_id),
                reply_markup=inline_answer_to_main,
            )
        elif user_id not in users_list:
            await bot.send_message(
                message.from_user.id,
                messages.USER_DONT_EXISTS.format(user_id),
                reply_markup=inline_answer_to_main,
            )
        await state.finish()
        await GoStates.setting.set()
    else:
        await message.reply(messages.ENTER_CORRECT_ID_USER)
