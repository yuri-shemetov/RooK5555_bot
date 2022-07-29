from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


inline_button_answer_for_apply_yes = InlineKeyboardButton("Да", callback_data="answer_yes")
inline_button_answer_for_apply_no = InlineKeyboardButton("Нет", callback_data="answer_no")
inline_button_answer_for_requisiters_yes = InlineKeyboardButton("Изменить", callback_data="requisiters_yes")
inline_button_answer_to_main = InlineKeyboardButton("На главную", callback_data="replay_new")
inline_button_applications = InlineKeyboardButton("Списки", callback_data="applications")
inline_button_apply = InlineKeyboardButton("Согласен / запросить доступ", callback_data="apply")
inline_button_approve_transaction = InlineKeyboardButton("Одобрить", callback_data="approve_transaction")
inline_button_balance_btc = InlineKeyboardButton("Баланс BTC", callback_data="balance")
inline_button_btc = InlineKeyboardButton("BTC", callback_data="btc")
inline_button_byn = InlineKeyboardButton("BYN", callback_data="byn")
inline_button_cancel = InlineKeyboardButton("Отменить", callback_data="cancel")
inline_button_continue = InlineKeyboardButton("Продолжить", callback_data="replay_new")
inline_button_currency_rate = InlineKeyboardButton("Мин. курс", callback_data="rate")
inline_button_fees = InlineKeyboardButton("Комиссия", callback_data="fees")
inline_button_new = InlineKeyboardButton("Согласен / создать новую заявку", callback_data="new")
inline_button_paid = InlineKeyboardButton("Оплачено", callback_data="paid")
inline_button_percent = InlineKeyboardButton("Процент", callback_data="percent")
inline_button_photo_ok = InlineKeyboardButton("OK", callback_data="photo_ok")
inline_button_reject_transaction = InlineKeyboardButton("Отклонить", callback_data="reject_transaction")
inline_button_replay_new = InlineKeyboardButton("Начать сначала", callback_data="replay_new")
inline_button_requisites = InlineKeyboardButton("Реквизиты", callback_data="applications")
inline_button_setting = InlineKeyboardButton("Настройки", callback_data="setting")
inline_button_start = InlineKeyboardButton("Поехали!", callback_data="replay_new")
inline_button_stop = InlineKeyboardButton("⛔️ STOP ⛔️", callback_data="stop")
inline_button_stop_bot_server = InlineKeyboardButton("⛔️ STOP BOT SERVER", callback_data="stop_bot_server")
inline_button_trade_conditions = InlineKeyboardButton("‼️ УСЛОВИЯ ТРЕЙДА ‼️", url="https://t.me/StoProBTC_usloviya")
inline_button_turn_on = InlineKeyboardButton("Включить бот", callback_data="turn_on")
inline_button_turn_off = InlineKeyboardButton("Выключить бот", callback_data="turn_off")
inline_button_usd_byn = InlineKeyboardButton("1USD", callback_data="usd_byn")
inline_button_yes = InlineKeyboardButton("OK", callback_data="OK")


# Keyboard

inline_admin_and_button_turn_on = InlineKeyboardMarkup(row_width=2)
inline_admin_and_button_turn_off = InlineKeyboardMarkup(row_width=2)
inline_answer = InlineKeyboardMarkup()
inline_answer_for_apply = InlineKeyboardMarkup()
inline_answer_for_requisiters = InlineKeyboardMarkup()
inline_answer_to_main = InlineKeyboardMarkup()
inline_apply = InlineKeyboardMarkup(row_width=1)
inline_approved_payment = InlineKeyboardMarkup()
inline_cancel = InlineKeyboardMarkup()
inline_continue = InlineKeyboardMarkup()
inline_fees = InlineKeyboardMarkup()
inline_new = InlineKeyboardMarkup(row_width=1)
inline_pay = InlineKeyboardMarkup(row_width=2)
inline_percent = InlineKeyboardMarkup()
inline_persona = InlineKeyboardMarkup()
inline_photo_ok = InlineKeyboardMarkup()
inline_setting = InlineKeyboardMarkup(row_width=2)
inline_start = InlineKeyboardMarkup()
inline_stop = InlineKeyboardMarkup()
inline_rate = InlineKeyboardMarkup()
inline_replay_new = InlineKeyboardMarkup()
inline_usd_byn = InlineKeyboardMarkup()


# Out

inline_admin_and_button_turn_on.add(inline_button_setting, inline_button_requisites, inline_button_turn_on, inline_button_stop_bot_server, inline_button_balance_btc)
inline_admin_and_button_turn_off.add(inline_button_setting, inline_button_requisites, inline_button_turn_off, inline_button_stop_bot_server, inline_button_balance_btc)
inline_answer.row(inline_button_cancel, inline_button_yes,)
inline_answer_for_apply.row(inline_button_answer_for_apply_yes, inline_button_answer_for_apply_no,)
inline_answer_for_requisiters.row(inline_button_answer_for_requisiters_yes, inline_button_answer_to_main,)
inline_answer_to_main.row(inline_button_answer_to_main,)
inline_apply.add(inline_button_apply, inline_button_cancel,)
inline_approved_payment.row(inline_button_approve_transaction, inline_button_reject_transaction,)
inline_cancel.row(inline_button_cancel,)
inline_continue.row(inline_button_continue,)
inline_new.add(inline_button_new, inline_button_cancel,)
inline_pay.add(inline_button_cancel, inline_button_paid, inline_button_trade_conditions,)
inline_photo_ok.add(inline_button_photo_ok,)
inline_rate.row(inline_button_byn, inline_button_btc,)
inline_replay_new.row(inline_button_replay_new,)
inline_setting.add(inline_button_currency_rate, inline_button_fees, inline_button_percent, inline_button_usd_byn, inline_button_answer_to_main,)
inline_start.row(inline_button_start,)
inline_stop.row(inline_button_answer_to_main, inline_button_stop,)