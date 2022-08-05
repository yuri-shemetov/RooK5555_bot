import re

from aiogram import types

from bot_app import messages
from bot_app.admin.users_list import get_registered_users
from bot_app.app import dp, bot, db_applications
from bot_app.keybords import inline_continue


# Application accepted
@dp.callback_query_handler(lambda c: c.data == "answer_yes", state="*")
async def button_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    user_id = int(re.findall("[0-9]+", callback_query.message["text"])[0])

    string_id = " " + str(user_id)
    registered_users_list = [int(x) for x in get_registered_users().split()]

    submitted = db_applications.get_or_create_application_submitted(
        user_id=user_id
    )[0][0]

    # Add user in list
    if user_id not in registered_users_list and submitted:
        with open("bot_app/admin/settings/registered_users.txt", "a") as file_users:
            file_users.write(string_id)

        await bot.send_message(
            callback_query.from_user.id,
            f"Пользователь ID № {user_id} добавлен в группу.",
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
            f"Одобрение отклонено, т.к пользователь ID № {user_id} уже в Вашей группе.",
        )

    # User not exists in list
    elif user_id not in registered_users_list:
        await bot.send_message(
            callback_query.from_user.id,
            f"Пользователь ID № {user_id} был уже ранее Вами отклонен!",
        )


# Application declined
@dp.callback_query_handler(lambda c: c.data == "answer_no", state="*")
async def button_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    user_id = int(re.findall("[0-9]+", callback_query.message["text"])[0])

    registered_users_list = [int(x) for x in get_registered_users().split()]

    submitted = db_applications.get_or_create_application_submitted(
        user_id=user_id
    )[0][0]

    if user_id not in registered_users_list and submitted:

        await bot.send_message(
            callback_query.from_user.id,
            f"Заявка пользователя ID № {user_id} отклонена.",
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
            f"Отклонение невозможно, т.к Вы добавили пользователя ID № {user_id} в группу.",
        )
    
    # User not exists in list
    elif user_id not in registered_users_list:
        await bot.send_message(
            callback_query.from_user.id,
            f"Пользователь ID № {user_id} был уже ранее Вами отклонен!",
        )
