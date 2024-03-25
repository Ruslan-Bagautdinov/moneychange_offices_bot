from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# # # BUTTONS # # #

LANG_BTN_ENG = chr(0x1F1EC) + chr(0x1F1E7) + " English"
LANG_BTN_RUS = chr(0x1F1F7) + chr(0x1F1FA) + " Русский"
LANG_BTN_TUR = chr(0x1F1F9) + chr(0x1F1F7) + "  Türkçe"


# COMMON BUTTONS

EUR_TO_USD_BTN = "EUR > USD"
USD_TO_EUR_BTN = "USD > EUR"


# ENGLISH_BUTTONS_TEXT

DAY_START_BTN_ENG = "Day start"
MONEY_INCOME_BTN_ENG = "Money come in"
SELL_RUBCARD_BTN_ENG = "SELL TL, USD, EURO > RUB CARD"
BUY_RUBCARD_BTN_ENG = "BUY TL, USD, EURO < RUB CARD"
BUY_CASH_BTN_ENG = "BUY CASH"
USDT_USD_BTN_ENG = "BUY USDT with USD"
USDT_TL_BTN_ENG = "BUY USDT with TL"
WU_RECEIVE_BTN_ENG = "WESTERN UNION receive"
WU_SENDING_BTN_ENG = "WESTERN UNION sending"
EXPENSES_BTN_ENG = "EXPENSES"

OTHER_BTN_ENG = "? OTHER"

SAVE_BTN_ENG = "⬆️SAVE"
CANCEL_BTN_ENG = "❌️CANCEL"

# RUSSIAN_BUTTONS_TEXT

DAY_START_BTN_RUS = "НАЧАЛО ДНЯ"
MONEY_INCOME_BTN_RUS = "ВНЕСЕНИЕ НАЛИЧНЫХ"
SELL_RUBCARD_BTN_RUS = "ПРОДАЖА TL, USD, EURO > RUB CARD"
BUY_RUBCARD_BTN_RUS = "ПОКУПКА TL, USD, EURO < RUB CARD"
BUY_CASH_BTN_RUS = "КУПИТЬ НАЛИЧНЫЕ"
USDT_USD_BTN_RUS = "КУПИТЬ USDT за USD"
USDT_TL_BTN_RUS = "КУПИТЬ USDT за TL"
WU_RECEIVE_BTN_RUS = "WESTERN UNION получение"
WU_SENDING_BTN_RUS = "WESTERN UNION отправка"
EXPENSES_BTN_RUS = "РАСХОДЫ"

OTHER_BTN_RUS = "? ДРУГАЯ"

SAVE_BTN_RUS = "⬆️СОХРАНИТЬ"
CANCEL_BTN_RUS = "❌️ОТМЕНА"

# TURKISH_BUTTONS_TEXT

DAY_START_BTN_TUR = "GÜNÜN BAŞLANGIÇ"
MONEY_INCOME_BTN_TUR = "PARA EKLEME"
SELL_RUBCARD_BTN_TUR = "SATMAK TL, USD, EURO > RUB CARD"
BUY_RUBCARD_BTN_TUR = "SATIN TL, USD, EURO < RUB CARD"
BUY_CASH_BTN_TUR = "NAKİT SATIN AL"
USDT_USD_BTN_TUR = "USD ile USDT SATIN AL"
USDT_TL_BTN_TUR = "TL ile USDT SATIN AL"
WU_RECEIVE_BTN_TUR = "WESTERN UNION ALMAK"
WU_SENDING_BTN_TUR = "WESTERN UNION GÖNDERİN"
EXPENSES_BTN_TUR = "GİDERLER"

OTHER_BTN_TUR = "? DİĞER"

SAVE_BTN_TUR = "⬆️KAYDETMEK"
CANCEL_BTN_TUR = "❌️İPTAL"

# CURRENCY_BUTTONS

TL_BTN = chr(0x20BA) + " TL"
USD_BTN = "$ USD"
EUR_BTN = "€ EUR"
RUB_BTN = chr(0x20BD) + " RUB"

# # # KEYBOARDS # # #

# LANGUAGE KEYBOARD

language_button_eng = InlineKeyboardButton(LANG_BTN_ENG, callback_data=LANG_BTN_ENG)
language_button_rus = InlineKeyboardButton(LANG_BTN_RUS, callback_data=LANG_BTN_RUS)
language_button_tur = InlineKeyboardButton(LANG_BTN_TUR, callback_data=LANG_BTN_TUR)

language_keyboard = InlineKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=True,
                                         row_width=1
                                         )
language_keyboard\
    .add(language_button_eng)\
    .add(language_button_rus)\
    .add(language_button_tur)

# # # CONFIRM_KEYBOARD

# CONFIRM_KEYBOARD_ENG
save_button_eng = InlineKeyboardButton(SAVE_BTN_ENG, callback_data=SAVE_BTN_ENG)
cancel_button_eng = InlineKeyboardButton(CANCEL_BTN_ENG, callback_data=CANCEL_BTN_ENG)

confirm_keyboard_eng = InlineKeyboardMarkup(resize_keyboard=True,
                                            one_time_keyboard=True,
                                            row_width=1
                                            )
confirm_keyboard_eng\
    .add(save_button_eng)\
    .insert(cancel_button_eng)

# CONFIRM_KEYBOARD_RUS
save_button_rus = InlineKeyboardButton(SAVE_BTN_RUS, callback_data=SAVE_BTN_RUS)
cancel_button_rus = InlineKeyboardButton(CANCEL_BTN_RUS, callback_data=CANCEL_BTN_RUS)

confirm_keyboard_rus = InlineKeyboardMarkup(resize_keyboard=True,
                                            one_time_keyboard=True,
                                            row_width=1
                                            )
confirm_keyboard_rus\
    .add(save_button_rus)\
    .insert(cancel_button_rus)

# CONFIRM_KEYBOARD_TUR
save_button_tur = InlineKeyboardButton(SAVE_BTN_TUR, callback_data=SAVE_BTN_TUR)
cancel_button_tur = InlineKeyboardButton(CANCEL_BTN_TUR, callback_data=CANCEL_BTN_TUR)

confirm_keyboard_tur = InlineKeyboardMarkup(resize_keyboard=True,
                                            one_time_keyboard=True,
                                            row_width=1
                                            )
confirm_keyboard_tur\
    .add(save_button_tur)\
    .insert(cancel_button_tur)

# # # CURRENCY_KEYBOARDS

# TL - USD - EUR - RUB KEYBOARD

currency_button_tl = InlineKeyboardButton(TL_BTN, callback_data=TL_BTN)
currency_button_usd = InlineKeyboardButton(USD_BTN, callback_data=USD_BTN)
currency_button_eur = InlineKeyboardButton(EUR_BTN, callback_data=EUR_BTN)
currency_button_rub = InlineKeyboardButton(RUB_BTN, callback_data=RUB_BTN)

t_u_e_r_currency_keyboard = InlineKeyboardMarkup(resize_keyboard=True,
                                                 one_time_keyboard=True,
                                                 row_width=1
                                                 )
t_u_e_r_currency_keyboard\
    .add(currency_button_tl)\
    .insert(currency_button_usd)\
    .insert(currency_button_eur)\
    .insert(currency_button_rub)

# TL - USD - EUR  KEYBOARD

t_u_e_currency_keyboard = InlineKeyboardMarkup(resize_keyboard=True,
                                               one_time_keyboard=True,
                                               row_width=1
                                               )
t_u_e_currency_keyboard\
    .add(currency_button_tl)\
    .insert(currency_button_usd)\
    .insert(currency_button_eur)

# TL - USD - EUR - RUB - OTHER KEYBOARD ENG

currency_button_tl = InlineKeyboardButton(TL_BTN, callback_data=TL_BTN)
currency_button_usd = InlineKeyboardButton(USD_BTN, callback_data=USD_BTN)
currency_button_eur = InlineKeyboardButton(EUR_BTN, callback_data=EUR_BTN)
currency_button_rub = InlineKeyboardButton(RUB_BTN, callback_data=RUB_BTN)
currency_button_other_eng = InlineKeyboardButton(OTHER_BTN_ENG, callback_data=OTHER_BTN_ENG)

t_u_e_r_o_currency_keyboard_eng = InlineKeyboardMarkup(resize_keyboard=True,
                                                       one_time_keyboard=True,
                                                       row_width=1
                                                       )
t_u_e_r_o_currency_keyboard_eng\
    .add(currency_button_tl)\
    .insert(currency_button_usd)\
    .insert(currency_button_eur)\
    .insert(currency_button_rub)\
    .insert(currency_button_other_eng)

# TL - USD - EUR - RUB - OTHER KEYBOARD RUS

currency_button_tl = InlineKeyboardButton(TL_BTN, callback_data=TL_BTN)
currency_button_usd = InlineKeyboardButton(USD_BTN, callback_data=USD_BTN)
currency_button_eur = InlineKeyboardButton(EUR_BTN, callback_data=EUR_BTN)
currency_button_rub = InlineKeyboardButton(RUB_BTN, callback_data=RUB_BTN)
currency_button_other_rus = InlineKeyboardButton(OTHER_BTN_RUS, callback_data=OTHER_BTN_RUS)

t_u_e_r_o_currency_keyboard_rus = InlineKeyboardMarkup(resize_keyboard=True,
                                                       one_time_keyboard=True,
                                                       row_width=1
                                                       )
t_u_e_r_o_currency_keyboard_rus\
    .add(currency_button_tl)\
    .insert(currency_button_usd)\
    .insert(currency_button_eur)\
    .insert(currency_button_rub)\
    .insert(currency_button_other_rus)

# TL - USD - EUR - RUB - OTHER KEYBOARD TUR

currency_button_tl = InlineKeyboardButton(TL_BTN, callback_data=TL_BTN)
currency_button_usd = InlineKeyboardButton(USD_BTN, callback_data=USD_BTN)
currency_button_eur = InlineKeyboardButton(EUR_BTN, callback_data=EUR_BTN)
currency_button_rub = InlineKeyboardButton(RUB_BTN, callback_data=RUB_BTN)
currency_button_other_tur = InlineKeyboardButton(OTHER_BTN_TUR, callback_data=OTHER_BTN_TUR)

t_u_e_r_o_currency_keyboard_tur = InlineKeyboardMarkup(resize_keyboard=True,
                                                       one_time_keyboard=True,
                                                       row_width=1
                                                       )
t_u_e_r_o_currency_keyboard_tur\
    .add(currency_button_tl)\
    .insert(currency_button_usd)\
    .insert(currency_button_eur)\
    .insert(currency_button_rub)\
    .insert(currency_button_other_tur)

# CASH KEYBOARD

currency_button_other_eng = InlineKeyboardButton(OTHER_BTN_ENG, callback_data=OTHER_BTN_ENG)
currency_button_other_rus = InlineKeyboardButton(OTHER_BTN_ENG, callback_data=OTHER_BTN_RUS)
currency_button_other_tur = InlineKeyboardButton(OTHER_BTN_ENG, callback_data=OTHER_BTN_TUR)

# # # CASH KEYBOARD ENG
cash_currency_keyboard_eng = InlineKeyboardMarkup(resize_keyboard=True,
                                                  one_time_keyboard=True,
                                                  row_width=1
                                                  )
cash_currency_keyboard_eng\
    .add(currency_button_usd)\
    .insert(currency_button_eur)\
    .insert(currency_button_rub).insert(currency_button_other_eng)

# # # CASH KEYBOARD RUS
cash_currency_keyboard_rus = InlineKeyboardMarkup(resize_keyboard=True,
                                                  one_time_keyboard=True,
                                                  row_width=1
                                                  )
cash_currency_keyboard_rus\
    .add(currency_button_usd)\
    .insert(currency_button_eur)\
    .insert(currency_button_rub).insert(currency_button_other_rus)

# # # CASH KEYBOARD TUR
cash_currency_keyboard_tur = InlineKeyboardMarkup(resize_keyboard=True,
                                                  one_time_keyboard=True,
                                                  row_width=1
                                                  )
cash_currency_keyboard_tur\
    .add(currency_button_usd)\
    .insert(currency_button_eur)\
    .insert(currency_button_rub).insert(currency_button_other_tur)


# # # MAIN_MENU KEYBOARD

# MAIN_MENU_ENG
day_start_button_eng = InlineKeyboardButton(DAY_START_BTN_ENG, callback_data=DAY_START_BTN_ENG)
money_income_button_eng = InlineKeyboardButton(MONEY_INCOME_BTN_ENG, callback_data=MONEY_INCOME_BTN_ENG)
sell_rubcard_button_eng = InlineKeyboardButton(SELL_RUBCARD_BTN_ENG, callback_data=SELL_RUBCARD_BTN_ENG)
buy_rubcard_button_eng = InlineKeyboardButton(BUY_RUBCARD_BTN_ENG, callback_data=BUY_RUBCARD_BTN_ENG)
buy_cash_button_eng = InlineKeyboardButton(BUY_CASH_BTN_ENG, callback_data=BUY_CASH_BTN_ENG)
eur_usd_button_eng = InlineKeyboardButton(EUR_TO_USD_BTN, callback_data=EUR_TO_USD_BTN)
usd_eur_button_eng = InlineKeyboardButton(USD_TO_EUR_BTN, callback_data=USD_TO_EUR_BTN)
usdt_usd_button_eng = InlineKeyboardButton(USDT_USD_BTN_ENG, callback_data=USDT_USD_BTN_ENG)
usdt_tl_button_eng = InlineKeyboardButton(USDT_TL_BTN_ENG, callback_data=USDT_TL_BTN_ENG)
wu_receive_button_eng = InlineKeyboardButton(WU_RECEIVE_BTN_ENG, callback_data=WU_RECEIVE_BTN_ENG)
wu_sending_button_eng = InlineKeyboardButton(WU_SENDING_BTN_ENG, callback_data=WU_SENDING_BTN_ENG)
expenses_button_eng = InlineKeyboardButton(EXPENSES_BTN_ENG, callback_data=EXPENSES_BTN_ENG)

main_menu_keyboard_eng = InlineKeyboardMarkup(resize_keyboard=True,
                                              one_time_keyboard=True,
                                              row_width=1
                                              )

main_menu_keyboard_eng\
    .add(day_start_button_eng)\
    .add(money_income_button_eng)\
    .add(sell_rubcard_button_eng)\
    .add(buy_rubcard_button_eng)\
    .add(buy_cash_button_eng)\
    .add(eur_usd_button_eng)\
    .insert(usd_eur_button_eng)\
    .add(usdt_usd_button_eng)\
    .add(usdt_tl_button_eng)\
    .add(wu_receive_button_eng)\
    .add(wu_sending_button_eng)\
    .add(expenses_button_eng)

# MAIN_MENU_RUS
day_start_button_rus = InlineKeyboardButton(DAY_START_BTN_RUS, callback_data=DAY_START_BTN_RUS)
money_income_button_rus = InlineKeyboardButton(MONEY_INCOME_BTN_RUS, callback_data=MONEY_INCOME_BTN_RUS)
sell_rubcard_button_rus = InlineKeyboardButton(SELL_RUBCARD_BTN_RUS, callback_data=SELL_RUBCARD_BTN_RUS)
buy_rubcard_button_rus = InlineKeyboardButton(BUY_RUBCARD_BTN_RUS, callback_data=BUY_RUBCARD_BTN_RUS)
buy_cash_button_rus = InlineKeyboardButton(BUY_CASH_BTN_RUS, callback_data=BUY_CASH_BTN_RUS)
eur_usd_button_rus = InlineKeyboardButton(EUR_TO_USD_BTN, callback_data=EUR_TO_USD_BTN)
usd_eur_button_rus = InlineKeyboardButton(USD_TO_EUR_BTN, callback_data=USD_TO_EUR_BTN)
usdt_usd_button_rus = InlineKeyboardButton(USDT_USD_BTN_RUS, callback_data=USDT_USD_BTN_RUS)
usdt_tl_button_rus = InlineKeyboardButton(USDT_TL_BTN_RUS, callback_data=USDT_TL_BTN_RUS)
wu_receive_button_rus = InlineKeyboardButton(WU_RECEIVE_BTN_RUS, callback_data=WU_RECEIVE_BTN_RUS)
wu_sending_button_rus = InlineKeyboardButton(WU_SENDING_BTN_RUS, callback_data=WU_SENDING_BTN_RUS)
expenses_button_rus = InlineKeyboardButton(EXPENSES_BTN_RUS, callback_data=EXPENSES_BTN_RUS)

main_menu_keyboard_rus = InlineKeyboardMarkup(resize_keyboard=True,
                                              one_time_keyboard=True,
                                              row_width=1
                                              )

main_menu_keyboard_rus\
    .add(day_start_button_rus)\
    .add(money_income_button_rus)\
    .add(sell_rubcard_button_rus)\
    .add(buy_rubcard_button_rus)\
    .add(buy_cash_button_rus)\
    .add(eur_usd_button_rus)\
    .insert(usd_eur_button_rus)\
    .add(usdt_usd_button_rus)\
    .add(usdt_tl_button_rus)\
    .add(wu_receive_button_rus)\
    .add(wu_sending_button_rus)\
    .add(expenses_button_rus)

# MAIN_MENU_TUR
day_start_button_tur = InlineKeyboardButton(DAY_START_BTN_TUR, callback_data=DAY_START_BTN_TUR)
money_income_button_tur = InlineKeyboardButton(MONEY_INCOME_BTN_TUR, callback_data=MONEY_INCOME_BTN_TUR)
sell_rubcard_button_tur = InlineKeyboardButton(SELL_RUBCARD_BTN_TUR, callback_data=SELL_RUBCARD_BTN_TUR)
buy_rubcard_button_tur = InlineKeyboardButton(BUY_RUBCARD_BTN_TUR, callback_data=BUY_RUBCARD_BTN_TUR)
buy_cash_button_tur = InlineKeyboardButton(BUY_CASH_BTN_TUR, callback_data=BUY_CASH_BTN_TUR)
eur_usd_button_tur = InlineKeyboardButton(EUR_TO_USD_BTN, callback_data=EUR_TO_USD_BTN)
usd_eur_button_tur = InlineKeyboardButton(USD_TO_EUR_BTN, callback_data=USD_TO_EUR_BTN)
usdt_usd_button_tur = InlineKeyboardButton(USDT_USD_BTN_TUR, callback_data=USDT_USD_BTN_TUR)
usdt_tl_button_tur = InlineKeyboardButton(USDT_TL_BTN_TUR, callback_data=USDT_TL_BTN_TUR)
wu_receive_button_tur = InlineKeyboardButton(WU_RECEIVE_BTN_TUR, callback_data=WU_RECEIVE_BTN_TUR)
wu_sending_button_tur = InlineKeyboardButton(WU_SENDING_BTN_TUR, callback_data=WU_SENDING_BTN_TUR)
expenses_button_tur = InlineKeyboardButton(EXPENSES_BTN_TUR, callback_data=EXPENSES_BTN_TUR)

main_menu_keyboard_tur = InlineKeyboardMarkup(resize_keyboard=True,
                                              one_time_keyboard=True,
                                              row_width=1
                                              )

main_menu_keyboard_tur\
    .add(day_start_button_tur)\
    .add(money_income_button_tur)\
    .add(sell_rubcard_button_tur)\
    .add(buy_rubcard_button_tur)\
    .add(buy_cash_button_tur)\
    .add(eur_usd_button_tur)\
    .insert(usd_eur_button_tur)\
    .add(usdt_usd_button_tur)\
    .add(usdt_tl_button_tur)\
    .add(wu_receive_button_tur)\
    .add(wu_sending_button_tur)\
    .add(expenses_button_tur)
