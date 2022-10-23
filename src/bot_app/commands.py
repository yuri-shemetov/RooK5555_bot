import asyncio
import json
import requests

from aiogram import types
from aiogram.dispatcher import FSMContext
from bot_app import messages
from bot_app.admin.choice_requisites import get_requisiters
from bot_app.admin.users_list import get_ban_users, get_registered_users
from bot_app.admin.on_off import get_on_or_off
from bot_app.app import dp, bot, db, db_applications
from bot_app.cleaner import (
    get_files_photos,
    get_files_wallets,
    get_files_messages,
    remove_old_files,
)
from bot_app.keybords import (
    inline_admin_and_button_turn_on,
    inline_admin_and_button_turn_off,
    inline_answer_for_apply,
    inline_answer_to_main,
    inline_apply,
    inline_cancel,
    inline_lets_go,
    inline_new,
    inline_pay,
    inline_photo_ok,
    inline_rate,
    inline_replay_new,
)
from bot_app.mail import get_new_email
from bot_app.my_local_settings import ADMIN
from bot_app.my_yadisk import save_to_yadisk, save_to_yadisk_wallet
from bot_app.states import GoStates
from bot_app.transactions import execute_transaction, get_balance_bitcoins
from bot_app.wallet_balance import check_wallet

from decimal import *
from datetime import datetime

from os import mkdir, path


CONTENT_TYPES = [
    "text",
    "audio",
    "document",
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


# Start
@dp.message_handler(commands=["start"], state="*")
async def send_welcome(message: types.Message):
    await message.reply(messages.WELCOME_MESSAGE, reply_markup=inline_lets_go)
    db_applications.update_application_submitted(
        message.from_user.id,
        application_submitted=False,
    )


# Terms
@dp.callback_query_handler(lambda c: c.data == "replay_new", state="*")
async def send_terms(callback_query: types.CallbackQuery):
    await callback_query.answer()

    ban_users_list = [int(x) for x in get_ban_users().split()]
    on_or_off = get_on_or_off()

    # Ban user
    if callback_query.from_user.id in ban_users_list:
        await bot.send_message(callback_query.from_user.id, messages.BLACK_LIST)
        await GoStates.ban.set()
        return

    # Admin user and button "turn_off"
    if callback_query.from_user.id == ADMIN and on_or_off == "on":
        with open("bot_app/admin/settings/byn_balance.txt", "r") as file_byn:
            total_balance = file_byn.read()
        date_time = str(datetime.now().strftime("%H:%M:%S %d.%m.%y"))
        await bot.send_message(
            callback_query.from_user.id,
            f"{messages.WELCOME_ADMIN_TURN_ON}\
                \n{date_time}\nСумма на текущем реквизите составляет: <b>{total_balance} BYN</b>",
            reply_markup=inline_admin_and_button_turn_off,
            parse_mode="html",
        )
        await GoStates.setting.set()

    # Admin user and button "turn_on"
    elif callback_query.from_user.id == ADMIN and on_or_off == "off":
        with open("bot_app/admin/settings/byn_balance.txt", "r") as file_byn:
            total_balance = file_byn.read()
        date_time = str(datetime.now().strftime("%H:%M:%S %d.%m.%y"))
        await bot.send_message(
            callback_query.from_user.id,
            f"{messages.WELCOME_ADMIN_TURN_OFF}\
                \n{date_time} - Общая сумма на текущем реквизите составляет: {total_balance} BYN",
            reply_markup=inline_admin_and_button_turn_on,
        )
        await GoStates.setting.set()

    # Turn on
    elif on_or_off == "on":
        await bot.send_message(
            callback_query.from_user.id, messages.TERMS_MESSAGE, reply_markup=inline_new
        )
        await GoStates.everybody_users.set()

    # Turn off
    elif on_or_off == "off":
        await bot.send_message(
            callback_query.from_user.id,
            messages.BOT_TURN_OFF,
            reply_markup=inline_cancel,
        )
        await GoStates.turn_off.set()


# Cancel
@dp.callback_query_handler(lambda c: c.data == "cancel", state="*")
async def button_click_call_back(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.send_message(
        callback_query.from_user.id,
        messages.CANCEL_MESSAGE,
        reply_markup=inline_replay_new,
    )


# New application
@dp.callback_query_handler(lambda c: c.data == "new", state=GoStates.everybody_users)
async def button_click_call_back(callback_query: types.CallbackQuery):

    await callback_query.answer()
    await GoStates.go.set()
    await bot.send_message(
        callback_query.from_user.id,
        messages.CHOISE_RATE_MESSAGE,
        reply_markup=inline_rate,
    )


# List commands for payment
@dp.callback_query_handler(lambda c: c.data == "OK", state=GoStates.pay)
async def button_click_call_back(callback_query: types.CallbackQuery):
    await callback_query.answer()

    ban_users_list = [int(x) for x in get_ban_users().split()]
    registered_users_list = [int(x) for x in get_registered_users().split()]
    on_or_off = get_on_or_off()

    # Ban user
    if callback_query.from_user.id in ban_users_list:
        await bot.send_message(callback_query.from_user.id, messages.BLACK_LIST)
        await GoStates.ban.set()
        return

    # Registered user
    elif callback_query.from_user.id in registered_users_list and on_or_off == "on":
        byn = db.get_subscriptions_all_price(callback_query.from_user.id)[0][0]
        text = "Итого к оплате: *" + str(byn) + " BYN*"
        btc = db.get_subscriptions_translation(callback_query.from_user.id)[0][0]
        count_btc = "Вам будет переведено  *" + str(btc) + " BTC*"

        now_requisiters = get_requisiters()

        await bot.send_message(
            callback_query.from_user.id,
            f"{text}\n{count_btc}\n\n{now_requisiters}",
            parse_mode="Markdown",
            reply_markup=inline_pay,
        )

    # Unregistered user
    elif callback_query.from_user.id not in registered_users_list and on_or_off == "on":
        await bot.send_message(
            callback_query.from_user.id,
            messages.MESSAGE_FOR_APPLY,
            reply_markup=inline_apply,
        )
        await GoStates.apply.set()

    # Turn off
    elif on_or_off == "off":
        await bot.send_message(
            callback_query.from_user.id,
            messages.BOT_TURN_OFF,
            reply_markup=inline_cancel,
        )
        await GoStates.turn_off.set()


# Apply for Authorization
@dp.callback_query_handler(lambda c: c.data == "apply", state=GoStates.apply)
async def button_click_call_back(callback_query: types.CallbackQuery):
    await callback_query.answer()

    submitted = db_applications.get_or_create_application_submitted(
        callback_query.from_user.id
    )[0][0]

    if submitted == False:
        await bot.send_message(callback_query.from_user.id, messages.WAIT_APPROVE, reply_markup=inline_answer_to_main)

        if callback_query.from_user.first_name:
            first_name = callback_query.from_user.first_name
        else:
            first_name = ""
        if callback_query.from_user.username:
            username = f"@{callback_query.from_user.username}"
        else:
            username = ""

        await bot.send_message(
            ADMIN,
            f"ЗАПРОС ДОСТУПА. Добавить пользователя ID № {callback_query.from_user.id}, Ник: {username}, Имя: {first_name} в группу?",
            reply_markup=inline_answer_for_apply,
        )
        db_applications.update_application_submitted(callback_query.from_user.id)
        await GoStates.pay.set()

    else:
        await bot.send_message(
            callback_query.from_user.id, messages.WAIT_REPEATED_APPROVE
        )
        await GoStates.pay.set()


# Upload photo
@dp.callback_query_handler(lambda c: c.data == "paid", state=GoStates.pay)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await callback_query.answer()
    await state.finish()
    await GoStates.photo.set()
    await bot.send_message(callback_query.from_user.id, messages.UPLOAD_PHOTO_MESSAGE)


# Error photo upload
@dp.message_handler(content_types=CONTENT_TYPES, state=GoStates.photo)
async def process_photo_invalid(message: types.Message):
    await message.reply(messages.UPLOAD_ERROR_MESSAGE)


# Successful photo upload
@dp.message_handler(content_types=["photo"], state=GoStates.photo)
async def process_photo(message: types.Message, state: FSMContext):

    if message.from_user.id == 1054473747:
        await asyncio.sleep(1)

    photo = message.photo.pop()
    
    if message.from_user.id == 1054473747:
        await asyncio.sleep(1)

    username = message.from_user.first_name
    id_user = str(message.from_user.id)
    lastname = ""
    if message.from_user.last_name != None:
        lastname = message.from_user.last_name

    if not path.exists("media/"):
        mkdir(f"media/")

    path_jpg = (
        "media/"
        + str(datetime.now().strftime("%y_%m_%d__%H-%M-%S"))
        + "-"
        + username
        + "-"
        + lastname
        + "-"
        + id_user
        + "_"
        + ".jpg"
    )
    await photo.download(destination_file=path_jpg)
    db.update_subscription_photo(message.from_user.id, photo=path_jpg)
    await message.reply(messages.UPLOAD_OK_MESSAGE, reply_markup=inline_photo_ok)
    await state.finish()
    await GoStates.photo_ok.set()
    # send photo to yadisk
    save_to_yadisk(id_user=id_user, path_jpg=path_jpg)


# Upload address
@dp.callback_query_handler(lambda c: c.data == "photo_ok", state=GoStates.photo_ok)
async def button_click_call_back(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, messages.ENTER_ADDRESS_MESSAGE)
    await state.finish()
    await GoStates.address.set()


# Error address upload
@dp.message_handler(
    content_types=["photo", "sticker", "pinned_message", "audio"],
    state=GoStates.address,
)
async def process_address_invalid(message: types.Message):
    await message.reply(messages.ADDRESS_ERROR_MESSAGE)


# Successful address upload
@dp.message_handler(content_types=["text"], state=GoStates.address)
async def process_message(message: types.Message, state: FSMContext):

    # Data parser

    try:

        async with state.proxy() as data:
            data["text"] = message.text
            user_message = data["text"]

    except:
        await message.reply(messages.ERROR_PARSER)
        await state.finish()
        return

    # Remember address and Send address to yandex_disk

    try:

        username = message.from_user.first_name
        id_user = str(message.from_user.id)
        lastname = ""
        if message.from_user.last_name != None:
            lastname = message.from_user.last_name
        save_to_yadisk_wallet(
            username=username,
            lastname=lastname,
            id_user=id_user,
            user_message=user_message,
        )

        await bot.send_message(
            message.from_user.id, messages.STATUS_WAIT_MESSAGE, parse_mode="HTML"
        )

    except:
        await message.reply(messages.ERROR_YANDEX)
        await state.finish()
        return

    # Waiting for a transaction

    try:
        price = db.get_subscriptions_all_price(message.from_user.id)[0][0]
        time_wait = 0

        while time_wait != 60:  # 10 minutes

            # refund money from email for saved receipts if payment was successful
            money = get_new_email(price=price)

            if Decimal(money) == Decimal(price):
                # transaction
                bitcoins = db.get_subscriptions_translation(message.from_user.id)[0][0]
                execute_transaction(
                    dest_address=user_message, translation=round(Decimal(bitcoins), 8)
                )

                # show a message about successful transaction and a wallet
                wallet = check_wallet(user_message)
                with open("animation/successful.jpeg", "rb") as photo:
                    await bot.send_photo(
                        message.from_user.id,
                        photo=photo,
                        caption=messages.GET_APLICATION + wallet,
                        reply_markup=inline_replay_new,
                    )
                try:
                    # Calculate the balance
                    user_balance = db.get_subscriptions_all_price(message.from_user.id)[0][0]
                    with open("bot_app/admin/settings/byn_balance.txt", "r") as file_byn:
                        get_balance = file_byn.read()
                    total_balance = Decimal(get_balance) + Decimal(user_balance)
                    with open("bot_app/admin/settings/byn_balance.txt", "w+") as file_byn:    
                        file_byn.write(f"{total_balance}")

                except:
                    await message.reply(messages.ERROR_COUNT_BALANCE, parse_mode="HTML")
                    await state.finish()
                    return

                try:
                    # send a message about successful payment
                    balance = Decimal(get_balance_bitcoins()) - round(Decimal(bitcoins), 8)
                    if message.from_user.first_name:
                        first_name = message.from_user.first_name
                    else:
                        first_name = ""
                    if message.from_user.username:
                        username = f"@{message.from_user.username}"
                    else:
                        username = ""

                    
                    if Decimal(total_balance) > 10000:
                        await bot.send_message(
                            ADMIN,
                            f"❗️❗️❗️ Достигнут максимальный баланс счетчика - 10K.\
                                \n✅️ Бот перевел {round(Decimal(bitcoins), 8)} BTC пользователю \
                                \nID № {message.from_user.id}, \nНик: {username} \nИмя: {first_name}. \
                                \nПримерно осталось: {balance} BTC",
                            parse_mode="HTML",
                        )

                    else:
                        await bot.send_message(
                            ADMIN,
                            f"✅️ Бот перевел {round(Decimal(bitcoins), 8)} BTC пользователю \
                                \nID № {message.from_user.id}, \nНик: {username} \nИмя: {first_name}. \
                                \nПримерно осталось: {balance} BTC",
                            parse_mode="HTML",
                        )
                except:
                    await message.reply(messages.ERROR_NOTIFICATION, parse_mode="HTML")
                    await state.finish()
                    return

                # delete old media files
                files = get_files_photos(path="media/")
                remove_old_files(path="media/", files=files)

                # delete old wallets files
                files = get_files_wallets(path="wallet/")
                remove_old_files(path="wallet/", files=files)

                # delete old messages (receipts) files
                files = get_files_messages(path="message/")
                remove_old_files(path="message/", files=files)

                await state.finish()
                
                # Approved from blockchain
                try:
                    await asyncio.sleep(30)
                    time_approved = 0
                    block_index = None
                    while block_index == None or time_approved < 3600:
                        transactions_url = 'https://blockchain.info/rawaddr/' + user_message
                        response = requests.get(transactions_url)
                        block_index = json.loads(response.text)['txs'][0]['block_index']
                        if block_index != None:
                            await message.reply(
                                messages.AUTOMATIC_CHECK_TRANSACTION,
                                parse_mode="HTML"
                            )
                            return

                        await asyncio.sleep(60)
                        time_approved += 60
                                
                    await message.reply(
                        messages.AUTOMATIC_CHECK_TRANSACTION_1_HOUR,
                        parse_mode="HTML"
                    )

                except:
                    await message.reply(
                        messages.MANUAL_CHECK_TRANSACTION,
                        parse_mode="HTML"
                    )
                    return

                return

            await asyncio.sleep(10)
            time_wait += 1

        if Decimal(money) != Decimal(price):
            await message.answer(
                messages.CHECK_ERROR_MESSAGE_FROM_BANK,
                reply_markup=inline_replay_new,
                parse_mode="HTML",
            )
            await state.finish()
            return

    except:
        await message.reply(
            messages.ERROR_LOOP, reply_markup=inline_replay_new, parse_mode="HTML"
        )
        await state.finish()
        return
