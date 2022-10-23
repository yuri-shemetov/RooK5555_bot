import datetime, time

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_app import messages
from bot_app.app import dp, bot, db
from bot_app.keybords import inline_answer_to_main
from bot_app.states import GoStates


# Check all registered users on the date of using the application
@dp.callback_query_handler(lambda c: c.data == "check_users", state=GoStates.setting)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)

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
        f"{messages.USERS_MORE_3_MONTH}{report_list}",
        parse_mode="HTML",
        reply_markup=inline_answer_to_main,
    )
    else:
        await bot.send_message(
        callback_query.from_user.id,
        messages.NO_USERS_3_MONTH,
        parse_mode="HTML",
        reply_markup=inline_answer_to_main,
    )
