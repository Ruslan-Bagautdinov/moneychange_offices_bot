from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from agent_list import agents

from icecream import ic

# # # BUTTONS # # #

# COMMON BUTTONS

USD_RATE_CALLBACK = "USD_RATE"
EUR_RATE_CALLBACK = "EUR_RATE"
RUB_RATE_CALLBACK = "RUB_RATE"
MIR_TL_CALLBACK = "MIR_TL"
MIR_USD_CALLBACK = "MIR_USD"
MIR_EUR_CALLBACK = "MIR_EUR"
USDT_TL_CALLBACK = "USDT_TL"

USD_RATE_BTN = "$ " + USD_RATE_CALLBACK
EUR_RATE_BTN = "€ " + EUR_RATE_CALLBACK
RUB_RATE_BTN = chr(0x20BD) + " " + RUB_RATE_CALLBACK
MIR_TL_BTN = chr(0x20BA) + " " + MIR_TL_CALLBACK
MIR_USD_BTN = "$ " + MIR_USD_CALLBACK
MIR_EUR_BTN = "€ " + MIR_EUR_CALLBACK
USDT_TL_BTN = chr(0x1F310) + " " + USDT_TL_CALLBACK



# ADMIN ENTER BUTTONS
ADMIN_ENTER_BTN_ENG = " LОG IN АS ADМIN "
ADMIN_ENTER_BTN_RUS = " BOЙTИ КAK AДМИH "
ADMIN_ENTER_BTN_TUR = " ADМIN ОLАRАК GİRİŞ YAРIN "

# ADMIN LINK BUTTONS
ADMIN_LINK_BTN_ENG = "Link to Google Sheets"
ADMIN_LINK_BTN_RUS = "Ссылка на Гугл Таблицы"
ADMIN_LINK_BTN_TUR = "Google E-Tablolar'a bağlantı"

# ADMIN SET PASSWORD BUTTONS
ADMIN_SET_PASSWORD_BTN_ENG = "Change password"
ADMIN_SET_PASSWORD_BTN_RUS = "Изменить пароль"
ADMIN_SET_PASSWORD_BTN_TUR = "Şifre değiştir"

# ADMIN SET RATE BUTTONS
ADMIN_SET_RATE_BTN_ENG = "Set exchange rate "
ADMIN_SET_RATE_BTN_RUS = "Установить курс обмена "
ADMIN_SET_RATE_BTN_TUR = "Döviz kurunu ayarla"


# # # KEYBOARDS # # #

# ADMIN ENTER KEYBOARD ENG
admin_enter_button_eng = InlineKeyboardButton(ADMIN_ENTER_BTN_ENG, callback_data=ADMIN_ENTER_BTN_ENG)

admin_enter_keyboard_eng = InlineKeyboardMarkup(resize_keyboard=True,
                                                one_time_keyboard=True,
                                                row_width=1
                                                )
admin_enter_keyboard_eng.\
    add(admin_enter_button_eng)

# ADMIN ENTER KEYBOARD RUS
admin_enter_button_rus = InlineKeyboardButton(ADMIN_ENTER_BTN_RUS, callback_data=ADMIN_ENTER_BTN_RUS)

admin_enter_keyboard_rus = InlineKeyboardMarkup(resize_keyboard=True,
                                                one_time_keyboard=True,
                                                row_width=1
                                                )
admin_enter_keyboard_rus\
    .add(admin_enter_button_rus)

# ADMIN ENTER KEYBOARD TUR
admin_enter_button_tur = InlineKeyboardButton(ADMIN_ENTER_BTN_TUR, callback_data=ADMIN_ENTER_BTN_TUR)

admin_enter_keyboard_tur = InlineKeyboardMarkup(resize_keyboard=True,
                                                one_time_keyboard=True,
                                                row_width=1
                                                )
admin_enter_keyboard_tur\
    .add(admin_enter_button_tur)


# ADMIN MAIN_MENU KEYBOARD ENG
admin_link_button_eng = InlineKeyboardButton(ADMIN_LINK_BTN_ENG,
                                             callback_data=ADMIN_LINK_BTN_ENG)

admin_set_password_button_eng = InlineKeyboardButton(ADMIN_SET_PASSWORD_BTN_ENG,
                                                     callback_data=ADMIN_SET_PASSWORD_BTN_ENG)

admin_set_rate_eng = InlineKeyboardButton(ADMIN_SET_RATE_BTN_ENG,
                                          callback_data=ADMIN_SET_RATE_BTN_ENG)

admin_main_menu_keyboard_eng = InlineKeyboardMarkup(resize_keyboard=True,
                                                    one_time_keyboard=True,
                                                    row_width=1
                                                    )
admin_main_menu_keyboard_eng\
    .add(admin_link_button_eng)\
    .add(admin_set_password_button_eng)\
    .add(admin_set_rate_eng)

# ADMIN MAIN_MENU KEYBOARD RUS
admin_link_button_rus = InlineKeyboardButton(ADMIN_LINK_BTN_RUS,
                                             callback_data=ADMIN_LINK_BTN_RUS)
admin_set_password_button_rus = InlineKeyboardButton(ADMIN_SET_PASSWORD_BTN_RUS,
                                                     callback_data=ADMIN_SET_PASSWORD_BTN_RUS)
admin_set_rate_rus = InlineKeyboardButton(ADMIN_SET_RATE_BTN_RUS,
                                          callback_data=ADMIN_SET_RATE_BTN_RUS)

admin_main_menu_keyboard_rus = InlineKeyboardMarkup(resize_keyboard=True,
                                                    one_time_keyboard=True,
                                                    row_width=1
                                                    )
admin_main_menu_keyboard_rus\
    .add(admin_link_button_rus)\
    .add(admin_set_password_button_rus)\
    .add(admin_set_rate_rus)

# ADMIN MAIN_MENU KEYBOARD TUR
admin_link_button_tur = InlineKeyboardButton(ADMIN_LINK_BTN_TUR,
                                             callback_data=ADMIN_LINK_BTN_TUR)
admin_set_password_button_tur = InlineKeyboardButton(ADMIN_SET_PASSWORD_BTN_TUR,
                                                     callback_data=ADMIN_SET_PASSWORD_BTN_TUR)
admin_set_rate_tur = InlineKeyboardButton(ADMIN_SET_RATE_BTN_TUR,
                                          callback_data=ADMIN_SET_RATE_BTN_TUR)

admin_main_menu_keyboard_tur = InlineKeyboardMarkup(resize_keyboard=True,
                                                    one_time_keyboard=True,
                                                    row_width=1
                                                    )
admin_main_menu_keyboard_tur\
    .add(admin_link_button_tur)\
    .add(admin_set_password_button_tur)\
    .add(admin_set_rate_tur)

# ADMIN SET PASSWORD USERS KEYBOARD

admin_set_password_users_keyboard = InlineKeyboardMarkup(resize_keyboard=True,
                                                         one_time_keyboard=True,
                                                         row_width=1
                                                         )
# AGENT BUTTONS

for agent in agents:
    agent_button = InlineKeyboardButton(agent[0],
                                        callback_data=agent[0])
    admin_set_password_users_keyboard.add(agent_button)


# ADMIN SET RATE CURRENCY KEYBOARD
admin_usd_rate_button = InlineKeyboardButton(USD_RATE_BTN,
                                             callback_data=USD_RATE_CALLBACK)
admin_eur_rate_button = InlineKeyboardButton(EUR_RATE_BTN,
                                             callback_data=EUR_RATE_CALLBACK)
admin_rub_rate_button = InlineKeyboardButton(RUB_RATE_BTN,
                                             callback_data=RUB_RATE_CALLBACK)
admin_mir_tl_button = InlineKeyboardButton(MIR_TL_BTN,
                                           callback_data=MIR_TL_CALLBACK)
admin_mir_usd_button = InlineKeyboardButton(MIR_USD_BTN,
                                            callback_data=MIR_USD_CALLBACK)
admin_mir_eur_button = InlineKeyboardButton(MIR_EUR_BTN,
                                            callback_data=MIR_EUR_CALLBACK)
admin_usdt_tl_button = InlineKeyboardButton(USDT_TL_BTN,
                                            callback_data=USDT_TL_CALLBACK)


admin_set_rate_currency_keyboard = InlineKeyboardMarkup(resize_keyboard=True,
                                                        one_time_keyboard=True,
                                                        row_width=1
                                                        )
admin_set_rate_currency_keyboard\
    .add(admin_usd_rate_button)\
    .add(admin_eur_rate_button)\
    .add(admin_rub_rate_button)\
    .add(admin_mir_usd_button)\
    .add(admin_mir_eur_button)\
    .add(admin_mir_tl_button) \
    .add(admin_usdt_tl_button)
