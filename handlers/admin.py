from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from os import environ

from pathlib import Path
import requests
import json
from decimal import InvalidOperation

# own imports

from create_bot import dp, bot, SERVER
from create_bot import GOOGLE_SHEET_LINK

from handlers.client import start, restart_by_command, restart_by_button
from handlers.client import delete_inline_keyboard, delete_stupid_message

from keyboards.client_kb import confirm_keyboard_eng, confirm_keyboard_rus, confirm_keyboard_tur
from keyboards.client_kb import SAVE_BTN_ENG, SAVE_BTN_RUS, SAVE_BTN_TUR
from keyboards.client_kb import CANCEL_BTN_ENG, CANCEL_BTN_RUS, CANCEL_BTN_TUR
from keyboards.admin_kb import *
from messages import *

from data_base.db_action import *
from g_sheet import *


if SERVER == "HEROKU":
    from create_bot import HEROKU_APP_NAME, HEROKU_APP_TOKEN


LOGO_IMG = Path(__file__).resolve().parent.parent / 'images' / 'smartpay_logo.jpg'


class FSMAdmin(StatesGroup):

    # admin_start = State()

    admin_main_menu = State()

    admin_set_password_select = State()
    admin_set_password_enter = State()
    admin_set_password_confirm = State()

    admin_set_rate_select = State()
    admin_set_rate_enter = State()
    admin_set_rate_confirm = State()


# ADMIN STATE FUNCTIONS
async def handle_admin_start(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    # await FSMAdmin.admin_start.set()

    async with state.proxy() as admin_operation:

        if c_back.data == ADMIN_ENTER_BTN_ENG:
            admin_operation["language"] = "ENG"
            admin_welcome_msg = ADMIN_WELCOME_MSG_ENG
            admin_main_menu_keyboard = admin_main_menu_keyboard_eng
        
        elif c_back.data == ADMIN_ENTER_BTN_RUS:
            admin_operation["language"] = "RUS"
            admin_welcome_msg = ADMIN_WELCOME_MSG_RUS
            admin_main_menu_keyboard = admin_main_menu_keyboard_rus
        
        elif c_back.data == ADMIN_ENTER_BTN_TUR:
            admin_operation["language"] = "TUR"
            admin_welcome_msg = ADMIN_WELCOME_MSG_TUR
            admin_main_menu_keyboard = admin_main_menu_keyboard_tur

        await bot.send_message(c_back.from_user.id,
                               admin_welcome_msg,
                               reply_markup=admin_main_menu_keyboard)

    await FSMAdmin.admin_main_menu.set()


async def continue_as_admin(language: str, c_back: types.CallbackQuery, state: FSMContext):

    """
    Allows to admin stay in loggined state after perfoming operation.

    :param language: "ENG" or "RUS" or "TUR"
    :param c_back: for sending to admin the message
    :param state: for finishing current state and setting "admin_main_menu" state
    :return: message with admin_main_menu_keyboard
    """

    await state.finish()

    await FSMAdmin.admin_main_menu.set()

    async with state.proxy() as admin_operation:
        admin_operation["language"] = language

        if admin_operation["language"] == "ENG":
            admin_main_menu_keyboard = admin_main_menu_keyboard_eng
            continue_admin_msg = CONTINUE_ADMIN_MSG_ENG

        elif admin_operation["language"] == "RUS":
            admin_main_menu_keyboard = admin_main_menu_keyboard_rus
            continue_admin_msg = CONTINUE_ADMIN_MSG_RUS

        elif admin_operation["language"] == "TUR":
            admin_main_menu_keyboard = admin_main_menu_keyboard_tur
            continue_admin_msg = CONTINUE_ADMIN_MSG_TUR

    await bot.send_message(c_back.from_user.id,
                           continue_admin_msg,
                           reply_markup=admin_main_menu_keyboard
                           )


# # # MAIN MENU FUNCTIONS

# # LINK TO GOOGLE SHEETS

async def handle_admin_link(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as admin_operation:
        language = admin_operation["language"]

    # if SERVER:
    #     google_sheet_link = getenv('GOOGLE_SHEET_LINK')
    #
    # else:
    #     google_sheet_link = GOOGLE_SHEET_LINK

    await bot.send_message(c_back.from_user.id,
                           GOOGLE_SHEET_LINK)

    await continue_as_admin(language, c_back, state)


# # SET PASSWORD

async def handle_admin_set_password_start(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as admin_operation:
        if admin_operation["language"] == "ENG":
            admin_set_password_msg = ADMIN_SET_PASSWORD_ENG
        elif admin_operation["language"] == "RUS":
            admin_set_password_msg = ADMIN_SET_PASSWORD_RUS
        elif admin_operation["language"] == "TUR":
            admin_set_password_msg = ADMIN_SET_PASSWORD_TUR

    await bot.send_message(c_back.from_user.id,
                           admin_set_password_msg,
                           reply_markup=admin_set_password_users_keyboard)

    await FSMAdmin.admin_set_password_select.set()


async def handle_admin_set_password_select(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    if SERVER == "HEROKU":
        func = environ.get
    else:
        func = read_password

    async with state.proxy() as admin_operation:
        if admin_operation["language"] == "ENG":
            admin_old_password_msg = ADMIN_OLD_PASSWORD_ENG
            admin_new_password_msg = ADMIN_NEW_PASSWORD_ENG
        elif admin_operation["language"] == "RUS":
            admin_old_password_msg = ADMIN_OLD_PASSWORD_RUS
            admin_new_password_msg = ADMIN_NEW_PASSWORD_RUS
        elif admin_operation["language"] == "TUR":
            admin_old_password_msg = ADMIN_OLD_PASSWORD_TUR
            admin_new_password_msg = ADMIN_NEW_PASSWORD_TUR

        for agent in agents:
            if c_back.data == agent[0]:

                old_password = func(agent[0])
                admin_operation["user_to_set_password"] = agent[0]

        admin_old_password_msg_complete = (f'{admin_operation["user_to_set_password"]}\n'
                                           f'{admin_old_password_msg}\t{old_password}')

    await bot.send_message(c_back.from_user.id,
                           admin_old_password_msg_complete)
    await bot.send_message(c_back.from_user.id,
                           admin_new_password_msg)

    await FSMAdmin.admin_set_password_enter.set()


async def handle_admin_set_password_enter(msg: types.Message, state: FSMContext):

    new_password = msg.text

    async with state.proxy() as admin_operation:
        admin_operation["new_password"] = new_password
        name = admin_operation["user_to_set_password"]

        if admin_operation["language"] == "ENG":
            password_confirm_msg = f'{ADMIN_NEW_PASSWORD_CONFIRM_ENG} {name} - {new_password} ?'
            confirm_keyboard = confirm_keyboard_eng
        
        elif admin_operation["language"] == "RUS":
            password_confirm_msg = f'{ADMIN_NEW_PASSWORD_CONFIRM_RUS} {name} - {new_password} ?'
            confirm_keyboard = confirm_keyboard_rus
        
        elif admin_operation["language"] == "TUR":
            password_confirm_msg = f'{name} {ADMIN_NEW_PASSWORD_CONFIRM_TUR} - {new_password} ?'
            confirm_keyboard = confirm_keyboard_tur

        await bot.send_message(msg.from_user.id,
                               password_confirm_msg,
                               reply_markup=confirm_keyboard)

        await FSMAdmin.admin_set_password_confirm.set()


async def handle_admin_set_password_confirm(c_back: types.CallbackQuery, state: FSMContext):

    async with state.proxy() as admin_operation:
        language = admin_operation["language"]
        user = admin_operation["user_to_set_password"]
        new_password = admin_operation["new_password"]

        if admin_operation["language"] == "ENG":
            new_password_ok_msg = ADMIN_NEW_PASSWORD_OK_ENG
            new_password_error_msg = ADMIN_NEW_PASSWORD_ERROR_ENG

        elif admin_operation["language"] == "RUS":
            new_password_ok_msg = ADMIN_NEW_PASSWORD_OK_RUS
            new_password_error_msg = ADMIN_NEW_PASSWORD_ERROR_RUS

        elif admin_operation["language"] == "TUR":
            new_password_ok_msg = ADMIN_NEW_PASSWORD_OK_TUR
            new_password_error_msg = ADMIN_NEW_PASSWORD_ERROR_TUR

    if SERVER == 'HEROKU':
        if change_the_value(user, new_password):
            new_password_report = new_password_ok_msg
        else:
            new_password_report = new_password_error_msg
    else:
        change_password(user, new_password)
        new_password_report = new_password_ok_msg

    await bot.send_message(c_back.from_user.id,
                           new_password_report)

    await delete_inline_keyboard(c_back)

    await continue_as_admin(language, c_back, state)


def change_the_value(name, new_value):

    config_var_name = name

    url = f'https://api.heroku.com/apps/{HEROKU_APP_NAME}/config-vars'

    headers = {
        'Accept': 'application/vnd.heroku+json; version=3',
        'Authorization': f'Bearer {HEROKU_APP_TOKEN}',
        'Content-Type': 'application/json'
    }

    new_value = str(new_value)

    data = {
        f'{config_var_name}': new_value
    }

    response = requests.patch(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return True
    else:
        return False


# # SET RATE

async def handle_admin_set_rate_start(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as admin_operation:
        if admin_operation["language"] == "ENG":
            admin_set_rate_msg = ADMIN_SET_RATE_ENG
        elif admin_operation["language"] == "RUS":
            admin_set_rate_msg = ADMIN_SET_RATE_RUS
        elif admin_operation["language"] == "TUR":
            admin_set_rate_msg = ADMIN_SET_RATE_TUR

    await bot.send_message(c_back.from_user.id,
                           admin_set_rate_msg,
                           reply_markup=admin_set_rate_currency_keyboard)

    await FSMAdmin.admin_set_rate_select.set()


async def handle_admin_set_rate_select(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    if SERVER == "HEROKU":
        func = environ.get
    else:
        func = read_rate

    async with state.proxy() as admin_operation:
        if admin_operation["language"] == "ENG":
            admin_old_rate_msg = ADMIN_OLD_RATE_ENG
            admin_new_rate_msg = ADMIN_NEW_RATE_ENG
        elif admin_operation["language"] == "RUS":
            admin_old_rate_msg = ADMIN_OLD_RATE_RUS
            admin_new_rate_msg = ADMIN_NEW_RATE_RUS
        elif admin_operation["language"] == "TUR":
            admin_old_rate_msg = ADMIN_OLD_RATE_TUR
            admin_new_rate_msg = ADMIN_NEW_RATE_TUR

        old_rate = func(c_back.data)
        admin_operation["name_to_set_rate"] = c_back.data

        admin_old_rate_msg_complete = f'{admin_operation["name_to_set_rate"]}\n{admin_old_rate_msg} {old_rate}'

    await bot.send_message(c_back.from_user.id,
                           admin_old_rate_msg_complete)
    await bot.send_message(c_back.from_user.id,
                           admin_new_rate_msg)

    await FSMAdmin.admin_set_rate_enter.set()


async def handle_admin_set_rate_enter(msg: types.Message, state: FSMContext):
    
    new_rate = msg.text

    try:
        new_rate = number_processing(new_rate)
    except InvalidOperation:
        await delete_stupid_message(msg)

    async with state.proxy() as admin_operation:
        
        admin_operation["new_rate"] = new_rate
        name = admin_operation["name_to_set_rate"]

        if admin_operation["language"] == "ENG":
            rate_confirm_msg = f'{ADMIN_NEW_RATE_CONFIRM_ENG} {name} - {new_rate} ?'
            confirm_keyboard = confirm_keyboard_eng

        elif admin_operation["language"] == "RUS":
            rate_confirm_msg = f'{ADMIN_NEW_RATE_CONFIRM_RUS} {name} - {new_rate} ?'
            confirm_keyboard = confirm_keyboard_rus

        elif admin_operation["language"] == "TUR":
            rate_confirm_msg = f'{name} {ADMIN_NEW_RATE_CONFIRM_TUR} - {new_rate} ?'
            confirm_keyboard = confirm_keyboard_tur

        await bot.send_message(msg.from_user.id,
                               rate_confirm_msg,
                               reply_markup=confirm_keyboard)

        await FSMAdmin.admin_set_rate_confirm.set()


async def handle_admin_set_rate_confirm(c_back: types.CallbackQuery, state: FSMContext):

    async with state.proxy() as admin_operation:
        language = admin_operation["language"]
        name = admin_operation["name_to_set_rate"]
        new_rate = admin_operation["new_rate"]

        new_rate = string_number_to_python(new_rate, bank_round=False)
        new_rate = decimal_number_to_string(new_rate, bank_round=False)

        if admin_operation["language"] == "ENG":
            new_rate_ok_msg = ADMIN_NEW_RATE_OK_ENG
            new_rate_error_msg = ADMIN_NEW_RATE_ERROR_ENG

        elif admin_operation["language"] == "RUS":
            new_rate_ok_msg = ADMIN_NEW_RATE_OK_RUS
            new_rate_error_msg = ADMIN_NEW_RATE_ERROR_RUS

        elif admin_operation["language"] == "TUR":
            new_rate_ok_msg = ADMIN_NEW_RATE_OK_TUR
            new_rate_error_msg = ADMIN_NEW_RATE_ERROR_TUR

    if SERVER == "HEROKU":
        if change_the_value(name, new_rate):
            new_rate_report = new_rate_ok_msg
        else:
            new_rate_report = new_rate_error_msg
    else:
        change_rate(name, new_rate)
        new_rate_report = new_rate_ok_msg

    await bot.send_message(c_back.from_user.id,
                           new_rate_report)

    await delete_inline_keyboard(c_back)

    await continue_as_admin(language, c_back, state)


def register_handlers_admin(dp: Dispatcher):

    # # # COMMON HANDLERS

    dp.register_message_handler(start,
                                commands=["start"],
                                state=None
                                )

    dp.register_message_handler(restart_by_command,
                                commands=["start"],
                                state="*"
                                )

    dp.register_callback_query_handler(restart_by_button,
                                       lambda c: c.data == CANCEL_BTN_ENG,
                                       state="*"
                                       )

    dp.register_callback_query_handler(restart_by_button,
                                       lambda c: c.data == CANCEL_BTN_RUS,
                                       state="*"
                                       )

    dp.register_callback_query_handler(restart_by_button,
                                       lambda c: c.data == CANCEL_BTN_TUR,
                                       state="*"
                                       )
    # # # ADMIN STATE START HANDLERS

    dp.register_callback_query_handler(handle_admin_start,
                                       lambda c: c.data == ADMIN_ENTER_BTN_ENG,
                                       state=None
                                       )

    dp.register_callback_query_handler(handle_admin_start,
                                       lambda c: c.data == ADMIN_ENTER_BTN_RUS,
                                       state=None
                                       )

    dp.register_callback_query_handler(handle_admin_start,
                                       lambda c: c.data == ADMIN_ENTER_BTN_TUR,
                                       state=None
                                       )
    # # # MAIN MENU HANDLERS

    # # # # LINK TO GOOGLE SHEETS

    dp.register_callback_query_handler(handle_admin_link,
                                       lambda c: c.data == ADMIN_LINK_BTN_ENG,
                                       state=FSMAdmin.admin_main_menu
                                       )

    dp.register_callback_query_handler(handle_admin_link,
                                       lambda c: c.data == ADMIN_LINK_BTN_RUS,
                                       state=FSMAdmin.admin_main_menu
                                       )

    dp.register_callback_query_handler(handle_admin_link,
                                       lambda c: c.data == ADMIN_LINK_BTN_TUR,
                                       state=FSMAdmin.admin_main_menu
                                       )

    # # # # SET PASSWORD

    dp.register_callback_query_handler(handle_admin_set_password_start,
                                       lambda c: c.data == ADMIN_SET_PASSWORD_BTN_ENG,
                                       state=FSMAdmin.admin_main_menu
                                       )

    dp.register_callback_query_handler(handle_admin_set_password_start,
                                       lambda c: c.data == ADMIN_SET_PASSWORD_BTN_RUS,
                                       state=FSMAdmin.admin_main_menu
                                       )

    dp.register_callback_query_handler(handle_admin_set_password_start,
                                       lambda c: c.data == ADMIN_SET_PASSWORD_BTN_TUR,
                                       state=FSMAdmin.admin_main_menu
                                       )

    dp.register_callback_query_handler(handle_admin_set_password_select,
                                       lambda c: c.data == agents[0][0],
                                       state=FSMAdmin.admin_set_password_select
                                       )

    dp.register_callback_query_handler(handle_admin_set_password_select,
                                       lambda c: c.data == agents[1][0],
                                       state=FSMAdmin.admin_set_password_select
                                       )
    dp.register_callback_query_handler(handle_admin_set_password_select,
                                       lambda c: c.data == agents[2][0],
                                       state=FSMAdmin.admin_set_password_select
                                       )
    dp.register_callback_query_handler(handle_admin_set_password_select,
                                       lambda c: c.data == agents[3][0],
                                       state=FSMAdmin.admin_set_password_select
                                       )


    dp.register_message_handler(handle_admin_set_password_enter,
                                content_types=["text"],
                                state=FSMAdmin.admin_set_password_enter
                                )

    dp.register_callback_query_handler(handle_admin_set_password_confirm,
                                       lambda c: c.data == SAVE_BTN_ENG,
                                       state=FSMAdmin.admin_set_password_confirm
                                       )

    dp.register_callback_query_handler(handle_admin_set_password_confirm,
                                       lambda c: c.data == SAVE_BTN_RUS,
                                       state=FSMAdmin.admin_set_password_confirm
                                       )

    dp.register_callback_query_handler(handle_admin_set_password_confirm,
                                       lambda c: c.data == SAVE_BTN_TUR,
                                       state=FSMAdmin.admin_set_password_confirm
                                       )
    
    # # # # SET RATE

    dp.register_callback_query_handler(handle_admin_set_rate_start,
                                       lambda c: c.data == ADMIN_SET_RATE_BTN_ENG,
                                       state=FSMAdmin.admin_main_menu
                                       )

    dp.register_callback_query_handler(handle_admin_set_rate_start,
                                       lambda c: c.data == ADMIN_SET_RATE_BTN_RUS,
                                       state=FSMAdmin.admin_main_menu
                                       )

    dp.register_callback_query_handler(handle_admin_set_rate_start,
                                       lambda c: c.data == ADMIN_SET_RATE_BTN_TUR,
                                       state=FSMAdmin.admin_main_menu
                                       )

    dp.register_callback_query_handler(handle_admin_set_rate_select,
                                       lambda c: c.data == USD_RATE_CALLBACK,
                                       state=FSMAdmin.admin_set_rate_select
                                       )

    dp.register_callback_query_handler(handle_admin_set_rate_select,
                                       lambda c: c.data == EUR_RATE_CALLBACK,
                                       state=FSMAdmin.admin_set_rate_select
                                       )

    dp.register_callback_query_handler(handle_admin_set_rate_select,
                                       lambda c: c.data == RUB_RATE_CALLBACK,
                                       state=FSMAdmin.admin_set_rate_select
                                       )

    dp.register_callback_query_handler(handle_admin_set_rate_select,
                                       lambda c: c.data == MIR_USD_CALLBACK,
                                       state=FSMAdmin.admin_set_rate_select
                                       )

    dp.register_callback_query_handler(handle_admin_set_rate_select,
                                       lambda c: c.data == MIR_EUR_CALLBACK,
                                       state=FSMAdmin.admin_set_rate_select
                                       )

    dp.register_callback_query_handler(handle_admin_set_rate_select,
                                       lambda c: c.data == MIR_TL_CALLBACK,
                                       state=FSMAdmin.admin_set_rate_select
                                       )

    dp.register_callback_query_handler(handle_admin_set_rate_select,
                                       lambda c: c.data == USDT_TL_CALLBACK,
                                       state=FSMAdmin.admin_set_rate_select
                                       )

    dp.register_message_handler(handle_admin_set_rate_enter,
                                content_types=["text"],
                                state=FSMAdmin.admin_set_rate_enter
                                )

    dp.register_callback_query_handler(handle_admin_set_rate_confirm,
                                       lambda c: c.data == SAVE_BTN_ENG,
                                       state=FSMAdmin.admin_set_rate_confirm
                                       )

    dp.register_callback_query_handler(handle_admin_set_rate_confirm,
                                       lambda c: c.data == SAVE_BTN_RUS,
                                       state=FSMAdmin.admin_set_rate_confirm
                                       )

    dp.register_callback_query_handler(handle_admin_set_rate_confirm,
                                       lambda c: c.data == SAVE_BTN_TUR,
                                       state=FSMAdmin.admin_set_rate_confirm
                                       )

    #   #   #   RANDOM TEXT ERASERS #   #   #
    # !!! Must be above all others registered handlers !!! #

    dp.register_message_handler(delete_stupid_message,
                                content_types=["text"],
                                state=None
                                )

    dp.register_message_handler(delete_stupid_message,
                                content_types=["text"],
                                state="*"
                                )
