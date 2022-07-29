from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_app.app import dp, bot
from bot_app.admin.users_list import get_ban_users
from bot_app.keybords import inline_answer_to_main
from bot_app.states import GoStates


# Upload Set_max_amount
@dp.callback_query_handler(lambda c: c.data == "black_list", state=GoStates.setting)
async def button_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id, "Введите ID пользователя для добавления его в черный список:"
    )
    

# Successful Set_max_amount
@dp.message_handler(content_types=["text"], state=GoStates.setting)
async def process_message(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["text"] = message.text
            id_ban_user = int(data["text"])

        string_id = " " + str(id_ban_user)
        ban_users_list = [int(x) for x in get_ban_users().split()]

        # Add user in ban_list
        if id_ban_user not in ban_users_list:
            with open("bot_app/admin/settings/ban_users.txt", "a") as file_ban_users:
                file_ban_users.write(string_id)

        await message.reply(
            f"Пользователь ID № {id_ban_user} добавлен в черный список!",
            reply_markup=inline_answer_to_main,
        )
    except:
        await message.reply("Введите только цифры:")
