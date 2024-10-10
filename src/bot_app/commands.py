import asyncio
import json
import logging
import requests

from aiogram import types
from aiogram.dispatcher import FSMContext
from bot_app import messages
from bot_app.admin.choice_requisites import get_requisiters
from bot_app.admin.users_list import get_ban_users, get_registered_users
from bot_app.admin.on_off import get_on_or_off
from bot_app.admin.settings_crypto import get_btc_state
from bot_app.app import dp, bot, db, db_applications, db_bank
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
    inline_rate_btc,
    inline_rate_coins,
    inline_rate_coins_btc_hidden,
    inline_rate_usdt,
    inline_replay_new,
)
from bot_app.mail import get_new_email
from bot_app.my_local_settings import ADMIN
from bot_app.my_yadisk import (
    save_to_yadisk,
    save_to_yadisk_wallet,
    save_to_yadisk_general_report
)
from bot_app.states import GoStates
from bot_app.transactions import execute_transaction, get_balance_bitcoins
from bot_app import transactions_usdt
from bot_app.wallet_balance import check_wallet, check_wallet_usdt

from decimal import *
from datetime import datetime
from time import time

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
        total_balance = db_bank.get_total()[0]
        date_time = str(datetime.now().strftime("%H:%M:%S %d.%m.%y"))
        btc_msg = messages.WELCOME_ADMIN_TURN_ON_BTC if get_btc_state() else messages.WELCOME_ADMIN_TURN_OFF_BTC
        await bot.send_message(
            callback_query.from_user.id,
            f"{messages.WELCOME_ADMIN_TURN_ON}{btc_msg}\
                \n{date_time}\nОбщая сумма по всем реквизитам составляет: <b>{total_balance} BYN</b>",
            reply_markup=inline_admin_and_button_turn_off,
            parse_mode="html",
        )
        await GoStates.setting.set()

    # Admin user and button "turn_on"
    elif callback_query.from_user.id == ADMIN and on_or_off == "off":
        with open("bot_app/admin/settings/byn_balance.txt", "r") as file_byn:
            total_balance = file_byn.read()
        date_time = str(datetime.now().strftime("%H:%M:%S %d.%m.%y"))
        btc_msg = messages.WELCOME_ADMIN_TURN_ON_BTC if get_btc_state() else messages.WELCOME_ADMIN_TURN_OFF_BTC
        await bot.send_message(
            callback_query.from_user.id,
            f"{messages.WELCOME_ADMIN_TURN_OFF}{btc_msg}\
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


# New application - Choise coins
@dp.callback_query_handler(lambda c: c.data == "new", state=GoStates.everybody_users)
async def button_click_call_back(callback_query: types.CallbackQuery):

    await callback_query.answer()
    await GoStates.everybody_users_coin.set()
    btc_visible = get_btc_state()
    # inline_buttons = inline_rate_coins if btc_visible else inline_rate_coins_btc_hidden
    msg_btc = messages.CHOISE_RATE_MESSAGE if btc_visible else messages.CHOISE_RATE_MESSAGE_BTC_HIDDEN
    await bot.send_message(
        callback_query.from_user.id,
        msg_btc,
        reply_markup=inline_rate_coins,
        parse_mode="HTML",
    )

# New application - BTC
@dp.callback_query_handler(lambda c: c.data == "btc_coin", state=GoStates.everybody_users_coin)
async def button_click_call_back(callback_query: types.CallbackQuery):

    await callback_query.answer()
    await GoStates.go.set()
    await bot.send_message(
        callback_query.from_user.id,
        messages.CHOISE_RATE_MESSAG_COIN,
        reply_markup=inline_rate_btc,
    )

# New application - USDT
@dp.callback_query_handler(lambda c: c.data == "usdt_coin", state=GoStates.everybody_users_coin)
async def button_click_call_back(callback_query: types.CallbackQuery):

    await callback_query.answer()
    await GoStates.go.set()
    await bot.send_message(
        callback_query.from_user.id,
        messages.CHOISE_RATE_MESSAG_COIN,
        reply_markup=inline_rate_usdt,
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
        total_amount = db.get_subscriptions_total_amount(callback_query.from_user.id)[0]

        if total_amount:
            if total_amount < 3000:
                text = messages.TEXT_FOR_PRICE.format(str(byn))
                loyalty = messages.TEXT_FOR_LOYALTY.format(total_amount, '20', int(3000 - total_amount))
            elif total_amount < 7000:
                byn_loyalty = round(Decimal(byn * 0.995))
                db.update_subscription_loyalty_price(callback_query.from_user.id, byn_loyalty) # update loyalty price
                byn_loyalty = db.get_subscriptions_all_loyalty_price(callback_query.from_user.id)[0][0] # get loyalty price
                text = messages.TEXT_FOR_PRICE_LOYALTY.format(str(byn), str(byn_loyalty))
                loyalty = messages.TEXT_FOR_LOYALTY.format(total_amount, '40', int(7000 - total_amount))
            elif total_amount < 15000:
                byn_loyalty = round(Decimal(byn * 0.99))
                db.update_subscription_loyalty_price(callback_query.from_user.id, byn_loyalty) # update loyalty price
                byn_loyalty = db.get_subscriptions_all_loyalty_price(callback_query.from_user.id)[0][0] # get loyalty price
                text = messages.TEXT_FOR_PRICE_LOYALTY.format(str(byn), str(byn_loyalty))
                loyalty = messages.TEXT_FOR_LOYALTY.format(total_amount, '60', int(15000 - total_amount))
            elif total_amount < 30000:
                byn_loyalty = round(Decimal(byn * 0.985))
                db.update_subscription_loyalty_price(callback_query.from_user.id, byn_loyalty) # update loyalty price
                byn_loyalty = db.get_subscriptions_all_loyalty_price(callback_query.from_user.id)[0][0] # get loyalty price
                text = messages.TEXT_FOR_PRICE_LOYALTY.format(str(byn), str(byn_loyalty))
                loyalty = messages.TEXT_FOR_LOYALTY.format(total_amount, '80', int(30000 - total_amount))
            elif total_amount < 60000:
                byn_loyalty = round(Decimal(byn * 0.98))
                db.update_subscription_loyalty_price(callback_query.from_user.id, byn_loyalty) # update loyalty price
                byn_loyalty = db.get_subscriptions_all_loyalty_price(callback_query.from_user.id)[0][0] # get loyalty price
                text = messages.TEXT_FOR_PRICE_LOYALTY.format(str(byn), str(byn_loyalty))
                loyalty = messages.TEXT_FOR_LOYALTY.format(total_amount, '100', int(60000 - total_amount))
            elif total_amount >= 60000:
                byn_loyalty = round(Decimal(byn * 0.975))
                db.update_subscription_loyalty_price(callback_query.from_user.id, byn_loyalty) # update loyalty price
                byn_loyalty = db.get_subscriptions_all_loyalty_price(callback_query.from_user.id)[0][0] # get loyalty price
                text = messages.TEXT_FOR_PRICE_LOYALTY.format(str(byn), str(byn_loyalty))
                loyalty = messages.TEXT_FOR_LOYALTY_THANKS.format(total_amount)

                """
                    3000 рублей - скидка 0.5%
                    7000 рублей - скидка 1%
                    15000 рублей - скидка 1.5%
                    30000 рублей - скидка 2%
                    60000 рублей - скидка 2.5% 
                """
        else:
            text = messages.TEXT_FOR_PRICE.format(str(byn))
            loyalty = messages.TEXT_FOR_LOYALTY_ZERO
        coins, rate = db.get_subscriptions_translation(callback_query.from_user.id)[0]
        rate = "USDT"  if "USDT" in rate else "BTC"
        count_coins = messages.TEXT_FOR_COUNT_COINS.format(str(coins), rate)
        now_requisiters, name_bank = get_requisiters()
        db.update_name_bank(callback_query.from_user.id, name_bank)

        await bot.send_message(
            callback_query.from_user.id,
            f"{text}\n{count_coins}\n\n{loyalty}\n\n{now_requisiters}",
            parse_mode="HTML",
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
        # Check timestamp
        start_timestamp = db.get_subscriptions_start_timestamp(message.from_user.id)[0][0]
        end_timestamp = int(time())
        cryptocurrency = "USDT" if "T" == user_message[0] else "BTC"
        if (end_timestamp - start_timestamp) < 900:
            await bot.send_message(
                message.from_user.id,
                messages.STATUS_WAIT_MESSAGE.format(cryptocurrency, cryptocurrency),
                parse_mode="HTML"
            )
        else:
            await bot.send_message(
                message.from_user.id,
                messages.STATUS_MORE_15_MINUTES_MESSAGE,
                parse_mode="HTML",
                reply_markup=inline_replay_new
            )
            await state.finish()
            return

    except:
        await message.reply(messages.ERROR_YANDEX)
        await state.finish()
        return

    # Waiting for a transaction

    try:
        try:
            byn_loyalty = db.get_subscriptions_all_loyalty_price(message.from_user.id)[0][0]
            if byn_loyalty:
                price = byn_loyalty
            else:
                price = db.get_subscriptions_all_price(message.from_user.id)[0][0]
        except Exception as exc:
            price = db.get_subscriptions_all_price(message.from_user.id)[0][0]
        time_wait = 0

        while time_wait != 60:  # 10 minutes

            # refund money from email for saved receipts if payment was successful
            money = get_new_email(price=price)

            if Decimal(money) == Decimal(price):
                # transaction
                coins, rate = db.get_subscriptions_translation(message.from_user.id)[0]
                is_usdt = "USDT" in rate
                if is_usdt:
                    tx = transactions_usdt.create_transaction(
                        dest_address=user_message, translation=round(Decimal(coins), 0)
                    )
                    wallet = check_wallet_usdt(tx.txid)
                    balance = Decimal(transactions_usdt.get_balance()) - round(Decimal(coins), 0)
                    transactions_usdt.execute_transaction(tx)
                else:
                    try:
                        tx = execute_transaction(
                            dest_address=user_message, translation=round(Decimal(coins), 8)
                        )
                    except Exception as exc:
                        logging.warning(f"Error. Execute Transaction BTC! {exc}")
                        await bot.send_message(
                            ADMIN,
                            f"❌ Внимание! Бот не смог автоматически перевести  \
                                \{round(Decimal(coins), int_for_rounnd)} {rate} пользователю \
                                \nID № {message.from_user.id}, \nНик: {username} \nИмя: {first_name}. \
                                \nНеобходима ручная отправка на адрес {user_message}! \
                                \nПользователю придет сообщение об успешной отправке!",
                            parse_mode="HTML",
                        )
                        url_for_view = f"https://www.blockchain.com/ru/btc/address/{wallet}"
                        await message.reply(
                            messages.ERROR_EXECUTE_TRANSACTION.format(url_for_view), reply_markup=inline_replay_new, parse_mode="HTML"
                        )
                        await state.finish()
                        return
                    
                    await asyncio.sleep(20)
                    wallet = check_wallet(tx)
                    balance = Decimal(get_balance_bitcoins()) - round(Decimal(coins), 8)

                try:
                    # save a general report
                    id_user = message.from_user.id
                    try:
                        transactions_url = f"https://mempool.space/api/address/" + user_message + "/txs"
                        response = requests.get(transactions_url)
                        hash_address = json.loads(response.text)[0]['txid']
                    except:
                        hash_address = user_message
                    name_bank = db.get_name_bank(id_user)[0]
                    username = ""
                    if message.from_user.username:
                        username = f"@{message.from_user.username}"
                    save_to_yadisk_general_report(hash_address, id_user, username, name_bank)
                except:
                    await bot.send_message(
                        ADMIN,
                        f"⚠️ Сохранить новый отчет не удалось",
                        parse_mode="HTML",
                    )

                # show a message about successful transaction and a wallet
                with open("animation/successful.jpeg", "rb") as photo:
                    await bot.send_photo(
                        message.from_user.id,
                        photo=photo,
                        caption=messages.GET_APLICATION + wallet,
                        reply_markup=inline_replay_new,
                    )
                
                try:
                    # Total amount for loyalty program
                    total_amount = db.get_subscriptions_total_amount(message.from_user.id)[0]
                    if total_amount:
                        total = round(Decimal(price) + Decimal(total_amount))
                        db.update_subscription_total_amount(message.from_user.id, total)
                    else:
                        db.update_subscription_total_amount(message.from_user.id, price)

                except Exception as exc:
                    await message.reply(messages.ERROR_TOTAL_AMOUNT_LOYATY.format(exc), parse_mode="HTML")
                    logging.info(f"Error. Total amount for loyalty program. {exc}")
                
                try:
                    # Calculate the balance
                    user_balance = db.get_subscriptions_all_price(message.from_user.id)[0][0]
                    balance_from_bank = db_bank.get_amount_from_bank(name_bank)[0]
                    total_balance = Decimal(balance_from_bank) + Decimal(user_balance)
                    db_bank.update_amount_from_bank(int(total_balance), name_bank)

                except:
                    await message.reply(messages.ERROR_COUNT_BALANCE, parse_mode="HTML")
                    await state.finish()
                    return

                try:
                    # send a message about successful payment
                    if message.from_user.first_name:
                        first_name = message.from_user.first_name
                    else:
                        first_name = ""
                    if message.from_user.username:
                        username = f"@{message.from_user.username}"
                    else:
                        username = ""

                    int_for_rounnd = 2 if is_usdt else 8
                    if Decimal(total_balance) > 10000:
                        await bot.send_message(
                            ADMIN,
                            f"❗️❗️❗️ Для банка {name_bank} достигнут максимальный баланс счетчика - 10K.\
                                \n✅️ Бот перевел {round(Decimal(coins), int_for_rounnd)} {rate} пользователю \
                                \nID № {message.from_user.id}, \nНик: {username} \nИмя: {first_name}. \
                                \nПримерно осталось: {round(Decimal(balance), int_for_rounnd)} {rate}",
                            parse_mode="HTML",
                        )

                    else:
                        await bot.send_message(
                            ADMIN,
                            f"✅️ Бот перевел {round(Decimal(coins), int_for_rounnd)} {rate} пользователю \
                                \nID № {message.from_user.id}, \nНик: {username} \nИмя: {first_name}. \
                                \nПримерно осталось: {round(Decimal(balance), int_for_rounnd)} {rate}",
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
                
                # Approved from mempool
                if is_usdt:
                    return
                else:
                    try:
                        await asyncio.sleep(30)
                        time_approved = 0
                        while time_approved < 3600:
                            transactions_status = "https://mempool.space/api/tx/{}/status".format(tx)
                            response = requests.get(transactions_status)
                            res = json.loads(response.text)
                            if res.get("confirmed") == True:
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

    except Exception as exc:
        await message.reply(
            messages.ERROR_LOOP, reply_markup=inline_replay_new, parse_mode="HTML"
        )
        await state.finish()
        logging.info(f"Error. Transaction loop. {exc}")
        return
