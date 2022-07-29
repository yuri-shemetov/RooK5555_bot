import re

from aiogram import types

from bot_app import messages
from bot_app.admin.users_list import get_registered_users
from bot_app.app import dp, bot, db, db_applications
from bot_app.keybords import inline_continue
from bot_app.my_local_settings import ADMIN

from datetime import datetime, timedelta


# Application accepted
@dp.callback_query_handler(lambda c: c.data == "answer_yes", state="*")
async def button_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    user_id = int(re.findall("[0-9]+", callback_query.message["text"])[0])
    username = re.findall("[@]\w*", callback_query.message["text"])[0]

    string_id = " " + str(user_id)
    registered_users_list = [int(x) for x in get_registered_users().split()]

    # Add user in list
    if user_id not in registered_users_list:
        with open("bot_app/admin/settings/registered_users.txt", "a") as file_users:
            file_users.write(string_id)

        await bot.send_message(
            callback_query.from_user.id,
            f"Пользователь ID № {user_id} {username} добавлен в группу.",
        )

        await bot.send_message(
            user_id,
            messages.APROVED,
            reply_markup=inline_continue,
        )

        db_applications.update_application_submitted(
            user_id,
            application_submitted=False,
        )

    # User exists in list
    elif user_id in registered_users_list:
        await bot.send_message(
            callback_query.from_user.id,
            f"Одобрение отклонено, т.к пользователь ID № {user_id} {username} уже в Вашей группе.",
        )


# Application declined
@dp.callback_query_handler(lambda c: c.data == "answer_no", state="*")
async def button_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    user_id = int(re.findall("[0-9]+", callback_query.message["text"])[0])
    username = re.findall("[@]\w*", callback_query.message["text"])[0]

    registered_users_list = [int(x) for x in get_registered_users().split()]

    if user_id not in registered_users_list:

        await bot.send_message(
            callback_query.from_user.id,
            f"Заявка пользователя ID № {user_id} {username} отклонена.",
        )

        await bot.send_message(
            user_id,
            messages.DECLINED,
        )

        db_applications.update_application_submitted(
            user_id,
            application_submitted=False,
        )

    # User exists in list
    elif user_id in registered_users_list:
        await bot.send_message(
            callback_query.from_user.id,
            f"Отклонение невозможно, т.к Вы добавили пользователя ID № {user_id} {username} группу.",
        )


# Transaction approve
@dp.callback_query_handler(lambda c: c.data == "approve_transaction", state="*")
async def button_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    limit_time = callback_query.message.date + timedelta(hours=24)
    user_id = int(re.findall("[0-9]+", callback_query.message["text"])[0])
    username = re.findall("[@]\w*", callback_query.message["text"])[0]
    reviewed = db.get_subscriptions_reviewed(user_id)[0][0]

    if (
        callback_query.from_user.id == ADMIN
        and reviewed == False
        and datetime.now() < limit_time
    ):

        db.update_subscription_reviewed_and_approve(user_id=user_id, approve=True)

        await bot.send_message(
            callback_query.from_user.id,
            f"💰✅ Пользователю ID № {user_id} {username} одобрена транзакция!",
        )

    elif (
        callback_query.from_user.id == ADMIN
        and reviewed
        and datetime.now() < limit_time
    ):
        await bot.send_message(
            callback_query.from_user.id,
            f"Для пользователя ID № {user_id} {username} одобрение\отклонение транзакции было уже Вами рассмотрено.",
        )

    elif callback_query.from_user.id == ADMIN and datetime.now() >= limit_time:
        await bot.send_message(
            callback_query.from_user.id,
            f"Время ожидания (24 ч.) Вашего подтверждения прошло.",
        )


# Transaction reject
@dp.callback_query_handler(lambda c: c.data == "reject_transaction", state="*")
async def button_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    limit_time = callback_query.message.date + timedelta(hours=24)
    user_id = int(re.findall("[0-9]+", callback_query.message["text"])[0])
    username = re.findall("[@]\w*", callback_query.message["text"])[0]
    reviewed = db.get_subscriptions_reviewed(user_id)[0][0]

    if (
        callback_query.from_user.id == ADMIN
        and reviewed == False
        and datetime.now() < limit_time
    ):

        db.update_subscription_reviewed_and_approve(user_id=user_id, approve=False)

        await bot.send_message(
            callback_query.from_user.id,
            f"❌ Пользователю ID № {user_id} {username} транзакция отклонена !",
        )

    elif (
        callback_query.from_user.id == ADMIN
        and reviewed
        and datetime.now() < limit_time
    ):
        await bot.send_message(
            callback_query.from_user.id,
            f"Для пользователя ID № {user_id} {username} одобрение/отклонение транзакции было уже Вами рассмотрено.",
        )

    elif callback_query.from_user.id == ADMIN and datetime.now() >= limit_time:
        await bot.send_message(
            callback_query.from_user.id,
            f"Время ожидания (24 ч.) Вашего подтверждения прошло.",
        )
