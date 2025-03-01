from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


inline_button_answer_for_apply_yes = InlineKeyboardButton("Да", callback_data="answer_yes")
inline_button_answer_for_apply_no = InlineKeyboardButton("Нет", callback_data="answer_no")
inline_button_answer_for_bank_yes = InlineKeyboardButton("Изменить БАНК", callback_data="bank_yes")
inline_button_answer_for_bank_amount_zero = InlineKeyboardButton("Обнулить суммы", callback_data="bank_zero_question")
inline_button_answer_for_notification_yes = InlineKeyboardButton("Написать", callback_data="notification_yes")
inline_button_answer_for_requisiters_add = InlineKeyboardButton("Добавить", callback_data="requisiters_add")
inline_button_answer_for_remove_bank_name = InlineKeyboardButton("Удалить", callback_data="remove_bank_name")
inline_button_answer_for_requisiters_yes = InlineKeyboardButton("Далее", callback_data="requisiters_yes")
inline_button_answer_for_is_only_day_yes = InlineKeyboardButton("Да", callback_data="is_only_day_yes")
inline_button_answer_for_is_only_day_no = InlineKeyboardButton("Нет", callback_data="is_only_day_no")
inline_button_answer_to_main = InlineKeyboardButton("На главную", callback_data="replay_new")
inline_button_applications = InlineKeyboardButton("Списки", callback_data="applications")
inline_button_apply = InlineKeyboardButton("Запросить доступ", callback_data="apply")
inline_button_balance_btc = InlineKeyboardButton("💰 Баланс BTC", callback_data="balance")
inline_button_black_list = InlineKeyboardButton("Черный список", callback_data="black_list")

inline_button_btc_coin = InlineKeyboardButton("BTC", callback_data="btc_coin")
inline_button_btc_coin_for_byn = InlineKeyboardButton("BTC за BYN", callback_data="btc_coin_for_byn")
inline_button_btc_coin_for_usdt = InlineKeyboardButton("BTC за USDT(trc20)", callback_data="btc_coin_for_usdt")
inline_button_btc = InlineKeyboardButton("BTC", callback_data="btc")
inline_button_byn = InlineKeyboardButton("BYN", callback_data="byn")


inline_button_usdt_coin = InlineKeyboardButton("USDT (trc20)", callback_data="usdt_coin")
inline_button_usdt_coin_for_byn = InlineKeyboardButton("USDT за BYN", callback_data="usdt_coin_for_byn")
inline_button_usdt_coin_for_usdt = InlineKeyboardButton("USDT за BTC", callback_data="usdt_coin_for_btc")
inline_button_usdt = InlineKeyboardButton("USDT (trc20)", callback_data="usdt")
inline_button_byn_usdt = InlineKeyboardButton("BYN", callback_data="byn_usdt")

inline_button_cancel = InlineKeyboardButton("Отменить", callback_data="cancel")
inline_button_сheck_users = InlineKeyboardButton("Проверка Users", callback_data="check_users")
inline_button_continue = InlineKeyboardButton("Продолжить", callback_data="OK")
inline_button_currency_rate = InlineKeyboardButton("Мин. курс", callback_data="rate")
inline_button_currency_rate_for_crypto = InlineKeyboardButton("Мин. курс", callback_data="rate_for_crypto")
inline_button_delete_user = InlineKeyboardButton("Удалить User", callback_data="delete_user")
inline_button_fees = InlineKeyboardButton("Комиссия", callback_data="fees")
inline_button_fees_for_crypto = InlineKeyboardButton("Комиссия", callback_data="fees_for_crypto")
inline_button_lets_go = InlineKeyboardButton("Вперед!", callback_data="replay_new")
inline_button_min_amount = InlineKeyboardButton("Мин. сумма сделки", callback_data="min_amount")
inline_button_max_amount = InlineKeyboardButton("Макс. сумма сделки", callback_data="max_amount")
inline_button_min_amount_for_crypto = InlineKeyboardButton("Мин. сумма сделки", callback_data="min_amount_for_crypto")
inline_button_max_amount_for_crypto = InlineKeyboardButton("Макс. сумма сделки", callback_data="max_amount_for_crypto")
inline_button_new = InlineKeyboardButton("Согласен / создать новую заявку", callback_data="new")
inline_button_notification = InlineKeyboardButton("Рассылка сообщений", callback_data="notification")
inline_button_paid = InlineKeyboardButton("Оплачено", callback_data="paid")
inline_button_percent = InlineKeyboardButton("Процент", callback_data="percent")
inline_button_percent_for_crypto = InlineKeyboardButton("Процент", callback_data="percent_for_crypto")
inline_button_photo_ok = InlineKeyboardButton("OK", callback_data="photo_ok")
inline_button_replay_new = InlineKeyboardButton("Начать сначала", callback_data="replay_new")
inline_button_requisites = InlineKeyboardButton("Реквизиты/Банк", callback_data="applications")

inline_button_setting = InlineKeyboardButton("🛠 Настройки", callback_data="setting")
inline_button_settings_for_crypto = InlineKeyboardButton("🛠 Настройки CRYPTO", callback_data="settings_for_crypto")

inline_button_settings_crypto = InlineKeyboardButton("⚖️ Обмен Монет", callback_data="settings_crypto")
inline_button_stop = InlineKeyboardButton("⛔️ STOP ⛔️", callback_data="stop")
inline_button_stop_bot_server = InlineKeyboardButton("⛔️ STOP BOT SERVER", callback_data="stop_bot_server")
inline_button_turn_on = InlineKeyboardButton("Включить бот", callback_data="turn_on")
inline_button_turn_off = InlineKeyboardButton("Выключить бот", callback_data="turn_off")
inline_button_turn_on_btc = InlineKeyboardButton("Включить BTC", callback_data="turn_on_btc")
inline_button_turn_off_btc = InlineKeyboardButton("Выключить BTC", callback_data="turn_off_btc")
inline_button_usd_byn = InlineKeyboardButton("1USD", callback_data="usd_byn")
inline_button_yes = InlineKeyboardButton("OK", callback_data="OK")


# Keyboard

inline_admin_and_button_turn_on = InlineKeyboardMarkup(row_width=2)
inline_admin_and_button_turn_off = InlineKeyboardMarkup(row_width=2)
inline_answer = InlineKeyboardMarkup()
inline_answer_for_apply = InlineKeyboardMarkup()
inline_answer_for_notification = InlineKeyboardMarkup()
inline_answer_to_settings_crypto = InlineKeyboardMarkup(row_width=2)
inline_answer_for_requisiters = InlineKeyboardMarkup(row_width=2)
inline_answer_for_requisiters_add = InlineKeyboardMarkup()
inline_answer_for_is_only_day = InlineKeyboardMarkup()
inline_answer_for_question_admin = InlineKeyboardMarkup(row_width=2)
inline_answer_to_main = InlineKeyboardMarkup()
inline_apply = InlineKeyboardMarkup(row_width=1)
inline_cancel = InlineKeyboardMarkup()
inline_continue = InlineKeyboardMarkup()
inline_choice_btc_between = InlineKeyboardMarkup()
inline_choice_usdt_between = InlineKeyboardMarkup()
inline_fees = InlineKeyboardMarkup()
inline_lets_go = InlineKeyboardMarkup()
inline_new = InlineKeyboardMarkup(row_width=1)
inline_pay = InlineKeyboardMarkup(row_width=2)
inline_percent = InlineKeyboardMarkup()
inline_persona = InlineKeyboardMarkup()
inline_photo_ok = InlineKeyboardMarkup()
inline_setting = InlineKeyboardMarkup(row_width=2)
inline_settings_for_crypto = InlineKeyboardMarkup(row_width=2)
inline_stop = InlineKeyboardMarkup()
inline_rate_coins = InlineKeyboardMarkup(row_width=2)
inline_rate_coins_btc_hidden = InlineKeyboardMarkup(row_width=2)
inline_rate_btc = InlineKeyboardMarkup(row_width=2)
inline_rate_usdt = InlineKeyboardMarkup(row_width=2)
inline_replay_new = InlineKeyboardMarkup()
inline_usd_byn = InlineKeyboardMarkup()
inline_users = InlineKeyboardMarkup(row_width=2)


# Out

inline_admin_and_button_turn_on.add(
    inline_button_setting,
    inline_button_settings_for_crypto,
    inline_button_requisites,
    inline_button_balance_btc,
    inline_button_black_list,
    inline_button_settings_crypto,
    inline_button_turn_on,
    inline_button_stop_bot_server,
    inline_button_notification,
    
)
inline_admin_and_button_turn_off.add(
    inline_button_setting,
    inline_button_settings_for_crypto,
    inline_button_requisites,
    inline_button_balance_btc,
    inline_button_сheck_users,
    inline_button_settings_crypto,
    inline_button_turn_off,
    inline_button_stop_bot_server,
    inline_button_notification,
)
inline_answer.row(inline_button_yes, inline_button_cancel,)
inline_answer_for_apply.row(inline_button_answer_for_apply_yes, inline_button_answer_for_apply_no,)
inline_answer_for_notification.row(inline_button_answer_for_notification_yes, inline_button_answer_to_main,)
inline_answer_for_requisiters.add(
    inline_button_answer_for_requisiters_add,
    inline_button_answer_for_remove_bank_name,
    inline_button_answer_for_bank_amount_zero,
    inline_button_answer_to_main,
)
inline_answer_for_requisiters_add.add(inline_button_answer_for_requisiters_yes)
inline_answer_for_is_only_day.add(
    inline_button_answer_for_is_only_day_yes, inline_button_answer_for_is_only_day_no)
inline_answer_to_settings_crypto.row(inline_button_turn_on_btc, inline_button_turn_off_btc)
inline_answer_to_main.row(inline_button_answer_to_main,)
inline_answer_for_question_admin.row(inline_button_answer_for_apply_yes, inline_button_answer_to_main)
inline_apply.add(inline_button_apply, inline_button_cancel,)
inline_cancel.row(inline_button_cancel,)
inline_continue.row(inline_button_continue, inline_button_replay_new,)
inline_lets_go.row(inline_button_lets_go,)
inline_new.add(inline_button_new, inline_button_cancel,)
inline_pay.add(inline_button_paid, inline_button_cancel,)
inline_photo_ok.add(inline_button_photo_ok,)
inline_rate_coins.add(
    inline_button_btc_coin,
    inline_button_usdt_coin,
)
inline_rate_coins_btc_hidden.add(
    inline_button_usdt_coin,
)
inline_choice_btc_between.add(
    inline_button_btc_coin_for_byn,
    # inline_button_btc_coin_for_usdt,
)
inline_rate_btc.add(
    inline_button_btc,
    inline_button_byn,
)
inline_choice_usdt_between.add(
    inline_button_usdt_coin_for_byn,
    # inline_button_usdt_coin_for_usdt,
)
inline_rate_usdt.add(
    inline_button_usdt,
    inline_button_byn_usdt
)
inline_replay_new.row(inline_button_replay_new,)
inline_setting.add(
    inline_button_currency_rate, 
    inline_button_fees,
    inline_button_percent,
    inline_button_usd_byn,
    inline_button_min_amount,
    inline_button_max_amount,
    inline_button_answer_to_main,
)
inline_settings_for_crypto.add(
    inline_button_currency_rate_for_crypto, 
    inline_button_fees_for_crypto,
    inline_button_percent_for_crypto,
    inline_button_min_amount_for_crypto,
    inline_button_max_amount_for_crypto,
    inline_button_answer_to_main,
)
inline_stop.row(inline_button_answer_to_main, inline_button_stop,)
inline_users.add(
    inline_button_delete_user,
    inline_button_answer_to_main,
)
