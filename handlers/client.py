from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove

from datetime import datetime, timedelta, timezone
from pathlib import Path
from os import environ

# own imports

from g_sheet import *
from keyboards import *
from messages import *
from data_base.db_action import read_password, read_rate
from number_funcs import string_number_to_python,decimal_number_to_string, number_processing, b_r, InvalidOperation

from create_bot import dp, bot
from create_bot import SERVER

from agent_list import agents

if SERVER == "HEROKU":
    func_rate = environ.get
else:
    func_rate = read_rate

LOGO_IMG = Path(__file__).resolve().parent.parent / 'images' / 'smartpay_logo.jpg'


class FSMClient(StatesGroup):

    language = State()

    password = State()

    main_menu = State()

    day_start_tl = State()
    day_start_usd = State()
    day_start_eur = State()
    day_start_rub = State()
    day_start_confirm = State()

    money_income_currency = State()
    money_income_amount = State()
    money_income_confirm = State()

    sell_rubcard_currency = State()
    sell_rubcard_amount = State()
    sell_rubcard_confirm = State()

    buy_rubcard_currency = State()
    buy_rubcard_amount = State()
    buy_rubcard_confirm = State()

    buy_cash_currency = State()
    buy_cash_amount = State()
    buy_cash_other_amount = State()
    buy_cash_other_currency_input = State()
    buy_cash_other_rate = State()
    buy_cash_confirm = State()

    eur_to_usd_amount = State()
    eur_to_usd_confirm = State()

    usd_to_eur_amount = State()
    usd_to_eur_confirm = State()

    usdt_for_usd_amount = State()
    usdt_for_usd_confirm = State()

    usdt_for_tl_amount = State()
    usdt_for_tl_confirm = State()

    wu_receive_currency = State()
    wu_receive_amount = State()
    wu_receive_confirm = State()

    wu_sending_currency = State()
    wu_sending_amount = State()
    wu_sending_confirm = State()

    expenses_currency = State()
    expenses_other_currency = State()
    expenses_other_currency_input = State()
    expenses_amount = State()
    expenses_explanation = State()
    expenses_confirm = State()


# COMMON FUNCTIONS

async def delete_stupid_message(msg):
    try:
        await bot.delete_message(msg.chat.id, msg.message_id)
    except:
        pass


async def delete_inline_keyboard(c_back):
    try:
        await c_back.message.edit_reply_markup(reply_markup=None)
    except:
        pass


async def delete_reply_button(msg):
    try:
        sent = await bot.send_message(msg.from_user.id,
                                      'dummie_message',
                                      reply_markup=ReplyKeyboardRemove()
                                      )
        await delete_stupid_message(sent)
    except:
        pass


async def start(msg):

    with open(LOGO_IMG, 'rb') as image:
        await bot.send_photo(msg.from_user.id,
                             image,
                             reply_markup=language_keyboard
                             )


async def restart_by_command(msg, state: FSMContext):

    current_state = await state.get_state()

    if current_state is not None:
        await state.finish()

    await delete_inline_keyboard(msg)

    await start(msg)


async def restart_by_button(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:
        agent = operation["agent"]
        language = operation["language"]

    await continue_operation(agent, language, c_back, state)


async def continue_operation(agent: str, language: str, c_back: types.CallbackQuery, state: FSMContext):

    """
    Allows to agent stay in loggined state after perfoming operation.

    :param agent: name of agent
    :param language: "ENG" or "RUS" or "TUR"
    :param c_back:  for sending to agent the message
    :param state: for finishing current state and setting "main_menu" state
    :return: message with main_menu_keyboard
    """

    await state.finish()

    await FSMClient.main_menu.set()

    async with state.proxy() as operation:
        operation["agent"] = agent
        operation["language"] = language

        if operation["language"] == "ENG":
            main_menu_keyboard = main_menu_keyboard_eng
            continue_msg = CONTINUE_MSG_ENG

        elif operation["language"] == "RUS":
            main_menu_keyboard = main_menu_keyboard_rus
            continue_msg = CONTINUE_MSG_RUS

        elif operation["language"] == "TUR":
            main_menu_keyboard = main_menu_keyboard_tur
            continue_msg = CONTINUE_MSG_TUR

    await bot.send_message(c_back.from_user.id,
                           continue_msg,
                           reply_markup=main_menu_keyboard
                           )


# CLIENT STATE FUNCTIONS

async def handle_language_eng(c_back: types.CallbackQuery, state: FSMContext):

    await FSMClient.language.set()

    async with state.proxy() as operation:
        operation["language"] = "ENG"

    await delete_inline_keyboard(c_back)

    await bot.send_message(c_back.from_user.id,
                           PASSWORD_MSG_ENG
                           )


async def handle_language_rus(c_back: types.CallbackQuery, state: FSMContext):

    await FSMClient.language.set()

    async with state.proxy() as operation:
        operation["language"] = "RUS"

    await delete_inline_keyboard(c_back)

    await bot.send_message(c_back.from_user.id,
                           PASSWORD_MSG_RUS
                           )


async def handle_language_tur(c_back: types.CallbackQuery, state: FSMContext):

    await FSMClient.language.set()

    async with state.proxy() as operation:
        operation["language"] = "TUR"

    await delete_inline_keyboard(c_back)

    await bot.send_message(c_back.from_user.id,
                           PASSWORD_MSG_TUR
                           )


async def handle_password(msg: types.Message, state: FSMContext):

    password = 'No'

    # Reading all existing passwords

    async with state.proxy() as operation:

        if SERVER == "HEROKU":
            func_pass = environ.get
        else:
            func_pass = read_password

        for agent in agents:
            if msg.text.lower() == func_pass(agent[0]):
                operation["agent"] = agent[1]
                operation["agent_welcome"] = agent[0]
                if agent[0] == "Admin":
                    password = "ADMIN"
                else:
                    password = "AGENT"

        # Recognizing inputted password
        
        if password == "AGENT":

            if operation["language"] == "ENG":
                main_menu_welcome = f'Welcome, {operation["agent_welcome"]}!'
                main_menu_keyboard = main_menu_keyboard_eng

            elif operation["language"] == "RUS":
                main_menu_welcome = f'Добро пожаловать, {operation["agent_welcome"]}!'
                main_menu_keyboard = main_menu_keyboard_rus

            elif operation["language"] == "TUR":
                main_menu_welcome = f'Hoş geldin, {operation["agent_welcome"]}!'
                main_menu_keyboard = main_menu_keyboard_tur

            await bot.send_message(msg.from_user.id,
                                   main_menu_welcome,
                                   reply_markup=main_menu_keyboard
                                   )

            await FSMClient.main_menu.set()

        elif password == "ADMIN":

            if operation["language"] == "ENG":
                admin_enter_keyboard = admin_enter_keyboard_eng
                admin_enter_msg = ADMIN_ENTER_MSG_ENG

            elif operation["language"] == "RUS":
                admin_enter_keyboard = admin_enter_keyboard_rus
                admin_enter_msg = ADMIN_ENTER_MSG_RUS

            elif operation["language"] == "TUR":
                admin_enter_keyboard = admin_enter_keyboard_tur
                admin_enter_msg = ADMIN_ENTER_MSG_TUR

            await bot.send_message(msg.from_user.id,
                                   admin_enter_msg,
                                   reply_markup=admin_enter_keyboard
                                   )
            await state.finish()

        else:
            await delete_stupid_message(msg)


# # # MAIN MENU FUNCTIONS

# # DAY START

async def handle_day_start(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:
        if operation["language"] == "ENG":
            day_start_tl_msg = DAY_START_TL_MSG_ENG
        elif operation["language"] == "RUS":
            day_start_tl_msg = DAY_START_TL_MSG_RUS
        elif operation["language"] == "TUR":
            day_start_tl_msg = DAY_START_TL_MSG_TUR

    await bot.send_message(c_back.from_user.id,
                           day_start_tl_msg)

    await FSMClient.day_start_tl.set()


async def handle_day_start_tl(msg: types.Message, state: FSMContext):

    try:
        start_tl = number_processing(msg.text, zero=True)
        async with state.proxy() as operation:
            operation["START_TL"] = start_tl

            if operation["language"] == "ENG":
                day_start_usd_msg = DAY_START_USD_MSG_ENG

            elif operation["language"] == "RUS":
                day_start_usd_msg = DAY_START_USD_MSG_RUS

            elif operation["language"] == "TUR":
                day_start_usd_msg = DAY_START_USD_MSG_TUR

        await bot.send_message(msg.from_user.id,
                               day_start_usd_msg)

        await FSMClient.day_start_usd.set()

    except InvalidOperation:
        await delete_stupid_message(msg)


async def handle_day_start_usd(msg: types.Message, state: FSMContext):

    try:
        start_usd = number_processing(msg.text, zero=True)
        async with state.proxy() as operation:
            operation["START_USD"] = start_usd

            if operation["language"] == "ENG":
                day_start_eur_msg = DAY_START_EUR_MSG_ENG

            elif operation["language"] == "RUS":
                day_start_eur_msg = DAY_START_EUR_MSG_RUS

            elif operation["language"] == "TUR":
                day_start_eur_msg = DAY_START_EUR_MSG_TUR

        await bot.send_message(msg.from_user.id,
                               day_start_eur_msg)

        await FSMClient.day_start_eur.set()

    except InvalidOperation:
        await delete_stupid_message(msg)


async def handle_day_start_eur(msg: types.Message, state: FSMContext):

    try:
        start_eur = number_processing(msg.text, zero=True)
        async with state.proxy() as operation:
            operation["START_EUR"] = start_eur

            if operation["language"] == "ENG":
                day_start_eur_msg = DAY_START_RUB_MSG_ENG

            elif operation["language"] == "RUS":
                day_start_eur_msg = DAY_START_RUB_MSG_RUS

            elif operation["language"] == "TUR":
                day_start_eur_msg = DAY_START_RUB_MSG_TUR

        await bot.send_message(msg.from_user.id,
                               day_start_eur_msg)

        await FSMClient.day_start_rub.set()

    except InvalidOperation:
        await delete_stupid_message(msg)


async def handle_day_start_rub(msg: types.Message, state: FSMContext):

    try:
        start_rub = number_processing(msg.text, zero=True)
        async with state.proxy() as operation:
            operation["START_RUB"] = start_rub

            if operation["language"] == "ENG":
                day_start_total_msg = (f'{DAY_START_TL_MSG_ENG} = {b_r(operation["START_TL"])} TL\n'
                                       f'{DAY_START_USD_MSG_ENG} = {b_r(operation["START_USD"])} USD\n'
                                       f'{DAY_START_EUR_MSG_ENG} = {b_r(operation["START_EUR"])} EUR\n'
                                       f'{DAY_START_RUB_MSG_ENG} = {b_r(operation["START_RUB"])} RUB')
                confirm_keyboard = confirm_keyboard_eng

            elif operation["language"] == "RUS":
                day_start_total_msg = (f'{DAY_START_TL_MSG_RUS} = {b_r(operation["START_TL"])} TL\n'
                                       f'{DAY_START_USD_MSG_RUS} = {b_r(operation["START_USD"])} USD\n'
                                       f'{DAY_START_EUR_MSG_RUS} = {b_r(operation["START_EUR"])} EUR\n'
                                       f'{DAY_START_RUB_MSG_RUS} = {b_r(operation["START_RUB"])} RUB')
                confirm_keyboard = confirm_keyboard_rus

            elif operation["language"] == "TUR":
                day_start_total_msg = (f'{DAY_START_TL_MSG_TUR} = {b_r(operation["START_TL"])} TL\n'
                                       f'{DAY_START_USD_MSG_TUR} = {b_r(operation["START_USD"])} USD\n'
                                       f'{DAY_START_EUR_MSG_TUR} = {b_r(operation["START_EUR"])} EUR\n'
                                       f'{DAY_START_RUB_MSG_TUR} = {b_r(operation["START_RUB"])} RUB')
                confirm_keyboard = confirm_keyboard_tur

        await bot.send_message(msg.from_user.id,
                               day_start_total_msg,
                               reply_markup=confirm_keyboard)

        await FSMClient.day_start_confirm.set()

    except InvalidOperation:
        await delete_stupid_message(msg)


async def handle_day_start_confirm(c_back: types.CallbackQuery, state: FSMContext):

    today = datetime.now(timezone.utc) + timedelta(hours=3)
    day = today.strftime("%d.%m.%Y")

    async with state.proxy() as operation:
        agent = operation["agent"]
        language = operation["language"]
        start_tl = operation["START_TL"]
        start_usd = operation["START_USD"]
        start_eur = operation["START_EUR"]
        start_rub = operation["START_RUB"]

        if g_sheet_func.create_agent_day_sheet(agent,
                                               day,
                                               start_tl,
                                               start_usd,
                                               start_eur,
                                               start_rub):

            if operation["language"] == "ENG":
                data_enter_ok_msg = DATA_ENTER_OK_ENG

            elif operation["language"] == "RUS":
                data_enter_ok_msg = DATA_ENTER_OK_RUS

            elif operation["language"] == "TUR":
                data_enter_ok_msg = DATA_ENTER_OK_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_ok_msg)

        else:

            if operation["language"] == "ENG":
                data_start_fail_msg = DAY_START_FAIL_ENG

            elif operation["language"] == "RUS":
                data_start_fail_msg = DAY_START_FAIL_RUS

            elif operation["language"] == "TUR":
                data_start_fail_msg = DAY_START_FAIL_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_start_fail_msg)

    await delete_inline_keyboard(c_back)

    await continue_operation(agent, language, c_back, state)


# # MONEY INCOME

async def handle_money_income_start(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:
        if operation["language"] == "ENG":
            money_income_currency_msg = CURRENCY_MSG_ENG
        elif operation["language"] == "RUS":
            money_income_currency_msg = CURRENCY_MSG_RUS
        elif operation["language"] == "TUR":
            money_income_currency_msg = CURRENCY_MSG_TUR

    await bot.send_message(c_back.from_user.id,
                           money_income_currency_msg,
                           reply_markup=t_u_e_r_currency_keyboard)

    await FSMClient.money_income_currency.set()


async def handle_money_income_currency(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:
        if c_back.data == TL_BTN:
            operation["money_income_currency"] = "TL"
        elif c_back.data == USD_BTN:
            operation["money_income_currency"] = "USD"
        elif c_back.data == EUR_BTN:
            operation["money_income_currency"] = "EUR"
        elif c_back.data == RUB_BTN:
            operation["money_income_currency"] = "RUB"

        if operation["language"] == "ENG":
            amount_msg = AMOUNT_MSG_ENG
        elif operation["language"] == "RUS":
            amount_msg = AMOUNT_MSG_RUS
        elif operation["language"] == "TUR":
            amount_msg = AMOUNT_MSG_TUR

    await c_back.message.edit_text(f'{c_back.data}')

    await bot.send_message(c_back.from_user.id,
                           amount_msg)

    await FSMClient.money_income_amount.set()


async def handle_money_income_amount(msg: types.Message, state: FSMContext):

    try:
        money_income = number_processing(msg.text)
        async with state.proxy() as operation:
            operation["money_income_amount"] = money_income

            if operation["language"] == "ENG":
                money_income_confirm_msg = (f'{MONEY_INCOME_ENG} = {b_r(money_income)} '
                                            f'{operation["money_income_currency"]}')
                confirm_keyboard = confirm_keyboard_eng
            elif operation["language"] == "RUS":
                money_income_confirm_msg = (f'{MONEY_INCOME_RUS} = {b_r(money_income)} '
                                            f'{operation["money_income_currency"]}')
                confirm_keyboard = confirm_keyboard_rus
            elif operation["language"] == "TUR":
                money_income_confirm_msg = (f'{MONEY_INCOME_TUR} = {b_r(money_income)} '
                                            f'{operation["money_income_currency"]}')
                confirm_keyboard = confirm_keyboard_tur

        await bot.send_message(msg.from_user.id,
                               money_income_confirm_msg,
                               reply_markup=confirm_keyboard)

        await FSMClient.money_income_confirm.set()

    except InvalidOperation:
        await delete_stupid_message(msg)


async def handle_money_income_confirm(c_back: types.CallbackQuery, state: FSMContext):

    today = datetime.now(timezone.utc) + timedelta(hours=3)
    day = today.strftime("%d.%m.%Y")

    async with state.proxy() as operation:
        agent = operation["agent"]
        language = operation["language"]
        amount = operation["money_income_amount"]
        currency = operation["money_income_currency"]

        if g_sheet_func.money_income_save_sheet(agent,
                                                day,
                                                amount,
                                                currency):
            if operation["language"] == "ENG":
                data_enter_ok_msg = DATA_ENTER_OK_ENG

            elif operation["language"] == "RUS":
                data_enter_ok_msg = DATA_ENTER_OK_RUS

            elif operation["language"] == "TUR":
                data_enter_ok_msg = DATA_ENTER_OK_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_ok_msg)

        else:

            if operation["language"] == "ENG":
                data_enter_fail_msg = DATA_ENTER_FAIL_ENG

            elif operation["language"] == "RUS":
                data_enter_fail_msg = DATA_ENTER_FAIL_RUS

            elif operation["language"] == "TUR":
                data_enter_fail_msg = DATA_ENTER_FAIL_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_fail_msg)

    await delete_inline_keyboard(c_back)
    await continue_operation(agent, language, c_back, state)


# # SELL RUBCARD

async def handle_sell_rubcard_start(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:
        if operation["language"] == "ENG":
            sell_rubcard_currency_msg = SOLD_TO_CLIENT_MSG_ENG
        elif operation["language"] == "RUS":
            sell_rubcard_currency_msg = SOLD_TO_CLIENT_MSG_RUS
        elif operation["language"] == "TUR":
            sell_rubcard_currency_msg = SOLD_TO_CLIENT_MSG_TUR

    await bot.send_message(c_back.from_user.id,
                           sell_rubcard_currency_msg,
                           reply_markup=t_u_e_currency_keyboard)

    await FSMClient.sell_rubcard_currency.set()


async def handle_sell_rubcard_currency(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:

        if c_back.data == TL_BTN:
            operation["sell_rubcard_currency"] = "TL"
            operation["sell_rubcard_rate"] = func_rate('MIR_TL')

        elif c_back.data == USD_BTN:
            operation["sell_rubcard_currency"] = "USD"
            operation["sell_rubcard_rate"] = func_rate('MIR_USD')

        elif c_back.data == EUR_BTN:
            operation["sell_rubcard_currency"] = "EUR"
            operation["sell_rubcard_rate"] = func_rate('MIR_EUR')

        if operation["language"] == "ENG":
            amount_msg = AMOUNT_MSG_ENG
        elif operation["language"] == "RUS":
            amount_msg = AMOUNT_MSG_RUS
        elif operation["language"] == "TUR":
            amount_msg = AMOUNT_MSG_TUR

    await c_back.message.edit_text(f'{c_back.data}')

    await bot.send_message(c_back.from_user.id,
                           amount_msg)

    await FSMClient.sell_rubcard_amount.set()


async def handle_sell_rubcard_amount(msg: types.Message, state: FSMContext):

    try:

        sell_rubcard_amount = number_processing(msg.text)
        async with state.proxy() as operation:
            operation["sell_rubcard_amount"] = sell_rubcard_amount

            sell_rubcard_amount = string_number_to_python(sell_rubcard_amount)
            sell_rubcard_rate = string_number_to_python(operation["sell_rubcard_rate"])
            sell_rubcard_result = sell_rubcard_amount * sell_rubcard_rate

            if operation["language"] == "ENG":
                sell_rubcard_confirm_msg = (f'{SOLD_TO_CLIENT_MSG_ENG} '
                                            f'{b_r(sell_rubcard_amount)} '
                                            f'{operation["sell_rubcard_currency"]}\n'
                                            f'{RECEIVED_FROM_CLIENT_MSG_ENG} '
                                            f'{b_r(sell_rubcard_result)} '
                                            f' RUB CARD')
                confirm_keyboard = confirm_keyboard_eng
            
            elif operation["language"] == "RUS":
                sell_rubcard_confirm_msg = (f'{SOLD_TO_CLIENT_MSG_RUS} '
                                            f'{b_r(sell_rubcard_amount)} '
                                            f'{operation["sell_rubcard_currency"]}\n'
                                            f'{RECEIVED_FROM_CLIENT_MSG_RUS} '
                                            f'{b_r(sell_rubcard_result)} '
                                            f' RUB CARD')
                confirm_keyboard = confirm_keyboard_rus
            
            elif operation["language"] == "TUR":
                sell_rubcard_confirm_msg = (f'{SOLD_TO_CLIENT_MSG_TUR} '
                                            f'{b_r(sell_rubcard_amount)} '
                                            f'{operation["sell_rubcard_currency"]}\n '
                                            f'{RECEIVED_FROM_CLIENT_MSG_TUR} '
                                            f'{b_r(sell_rubcard_result)} '
                                            f' RUB CARD')
                confirm_keyboard = confirm_keyboard_tur

        await bot.send_message(msg.from_user.id,
                               sell_rubcard_confirm_msg,
                               reply_markup=confirm_keyboard)

        await FSMClient.sell_rubcard_confirm.set()

    except InvalidOperation:
        await delete_stupid_message(msg)


async def handle_sell_rubcard_confirm(c_back: types.CallbackQuery, state: FSMContext):

    today = datetime.now(timezone.utc) + timedelta(hours=3)
    day = today.strftime("%d.%m.%Y")

    async with state.proxy() as operation:
        agent = operation["agent"]
        language = operation["language"]
        amount = operation["sell_rubcard_amount"]
        currency = operation["sell_rubcard_currency"]

        if g_sheet_func.sell_rubcard_save_sheet(agent,
                                                day,
                                                amount,
                                                currency):
            if operation["language"] == "ENG":
                data_enter_ok_msg = DATA_ENTER_OK_ENG

            elif operation["language"] == "RUS":
                data_enter_ok_msg = DATA_ENTER_OK_RUS

            elif operation["language"] == "TUR":
                data_enter_ok_msg = DATA_ENTER_OK_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_ok_msg)

        else:

            if operation["language"] == "ENG":
                data_enter_fail_msg = DATA_ENTER_FAIL_ENG

            elif operation["language"] == "RUS":
                data_enter_fail_msg = DATA_ENTER_FAIL_RUS

            elif operation["language"] == "TUR":
                data_enter_fail_msg = DATA_ENTER_FAIL_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_fail_msg)

    await delete_inline_keyboard(c_back)
    await continue_operation(agent, language, c_back, state)


# # BUY RUBCARD

async def handle_buy_rubcard_start(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:
        if operation["language"] == "ENG":
            buy_rubcard_currency_msg = PURCHASE_FROM_CLIENT_MSG_ENG
        elif operation["language"] == "RUS":
            buy_rubcard_currency_msg = PURCHASE_FROM_CLIENT_MSG_RUS
        elif operation["language"] == "TUR":
            buy_rubcard_currency_msg = PURCHASE_FROM_CLIENT_MSG_TUR

    await bot.send_message(c_back.from_user.id,
                           buy_rubcard_currency_msg,
                           reply_markup=t_u_e_currency_keyboard)

    await FSMClient.buy_rubcard_currency.set()


async def handle_buy_rubcard_currency(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:

        if c_back.data == TL_BTN:
            operation["buy_rubcard_currency"] = "TL"
            operation["buy_rubcard_rate"] = func_rate('MIR_TL')

        elif c_back.data == USD_BTN:
            operation["buy_rubcard_currency"] = "USD"
            operation["buy_rubcard_rate"] = func_rate('MIR_USD')

        elif c_back.data == EUR_BTN:
            operation["buy_rubcard_currency"] = "EUR"
            operation["buy_rubcard_rate"] = func_rate('MIR_EUR')

        if operation["language"] == "ENG":
            amount_msg = AMOUNT_MSG_ENG
        elif operation["language"] == "RUS":
            amount_msg = AMOUNT_MSG_RUS
        elif operation["language"] == "TUR":
            amount_msg = AMOUNT_MSG_TUR

    await c_back.message.edit_text(f'{c_back.data}')

    await bot.send_message(c_back.from_user.id,
                           amount_msg)

    await FSMClient.buy_rubcard_amount.set()


async def handle_buy_rubcard_amount(msg: types.Message, state: FSMContext):

    try:

        buy_rubcard_amount = number_processing(msg.text)
        async with state.proxy() as operation:
            operation["buy_rubcard_amount"] = buy_rubcard_amount

            buy_rubcard_amount = string_number_to_python(buy_rubcard_amount)
            buy_rubcard_rate = string_number_to_python(operation["buy_rubcard_rate"])
            buy_rubcard_result = buy_rubcard_amount * buy_rubcard_rate

            if operation["language"] == "ENG":
                buy_rubcard_confirm_msg = (f'{PURCHASE_FROM_CLIENT_MSG_ENG} '
                                           f'{b_r(buy_rubcard_amount)} '
                                           f'{operation["buy_rubcard_currency"]}\n'
                                           f'{TRANSFERRED_TO_CLIENT_MSG_ENG} '
                                           f'{b_r(buy_rubcard_result)} '
                                           f'RUB CARD')
                confirm_keyboard = confirm_keyboard_eng
            elif operation["language"] == "RUS":
                buy_rubcard_confirm_msg = (f'{PURCHASE_FROM_CLIENT_MSG_RUS} '
                                           f'{b_r(buy_rubcard_amount)} '
                                           f'{operation["buy_rubcard_currency"]}\n'
                                           f'{TRANSFERRED_TO_CLIENT_MSG_RUS} '
                                           f'{b_r(buy_rubcard_result)} '
                                           f'RUB CARD')
                confirm_keyboard = confirm_keyboard_rus
            elif operation["language"] == "TUR":
                buy_rubcard_confirm_msg = (f'{PURCHASE_FROM_CLIENT_MSG_TUR} '
                                           f'{b_r(buy_rubcard_amount)} '
                                           f'{operation["buy_rubcard_currency"]}\n'
                                           f'{TRANSFERRED_TO_CLIENT_MSG_TUR} '
                                           f'{b_r(buy_rubcard_result)} '
                                           f'RUB CARD')
                confirm_keyboard = confirm_keyboard_tur

        await bot.send_message(msg.from_user.id,
                               buy_rubcard_confirm_msg,
                               reply_markup=confirm_keyboard)

        await FSMClient.buy_rubcard_confirm.set()

    except InvalidOperation:
        await delete_stupid_message(msg)


async def handle_buy_rubcard_confirm(c_back: types.CallbackQuery, state: FSMContext):

    today = datetime.now(timezone.utc) + timedelta(hours=3)
    day = today.strftime("%d.%m.%Y")

    async with state.proxy() as operation:
        agent = operation["agent"]
        language = operation["language"]
        amount = operation["buy_rubcard_amount"]
        currency = operation["buy_rubcard_currency"]

        if g_sheet_func.buy_rubcard_save_sheet(agent,
                                               day,
                                               amount,
                                               currency):
            if operation["language"] == "ENG":
                data_enter_ok_msg = DATA_ENTER_OK_ENG

            elif operation["language"] == "RUS":
                data_enter_ok_msg = DATA_ENTER_OK_RUS

            elif operation["language"] == "TUR":
                data_enter_ok_msg = DATA_ENTER_OK_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_ok_msg)

        else:

            if operation["language"] == "ENG":
                data_enter_fail_msg = DATA_ENTER_FAIL_ENG

            elif operation["language"] == "RUS":
                data_enter_fail_msg = DATA_ENTER_FAIL_RUS

            elif operation["language"] == "TUR":
                data_enter_fail_msg = DATA_ENTER_FAIL_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_fail_msg)

    await delete_inline_keyboard(c_back)
    await continue_operation(agent, language, c_back, state)

# # BUY CASH


async def handle_buy_cash_start(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:
        if operation["language"] == "ENG":
            buy_cash_currency_msg = CURRENCY_MSG_ENG
            cash_currency_keyboard = cash_currency_keyboard_eng
        elif operation["language"] == "RUS":
            buy_cash_currency_msg = CURRENCY_MSG_RUS
            cash_currency_keyboard = cash_currency_keyboard_rus
        elif operation["language"] == "TUR":
            buy_cash_currency_msg = CURRENCY_MSG_TUR
            cash_currency_keyboard = cash_currency_keyboard_tur

    await bot.send_message(c_back.from_user.id,
                           buy_cash_currency_msg,
                           reply_markup=cash_currency_keyboard)

    await FSMClient.buy_cash_currency.set()


async def handle_buy_cash_currency(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:

        if c_back.data == USD_BTN:
            operation["buy_cash_currency"] = "USD"
            operation["buy_cash_rate"] = func_rate('USD_RATE')

        elif c_back.data == EUR_BTN:
            operation["buy_cash_currency"] = "EUR"
            operation["buy_cash_rate"] = func_rate('EUR_RATE')

        elif c_back.data == RUB_BTN:
            operation["buy_cash_currency"] = "RUB"
            rub_rate = func_rate('RUB_RATE')
            operation["buy_cash_rate"] = decimal_number_to_string(
                1 / string_number_to_python(rub_rate, bank_round=False),
                bank_round=False)

        if operation["language"] == "ENG":
            amount_msg = AMOUNT_MSG_ENG
        elif operation["language"] == "RUS":
            amount_msg = AMOUNT_MSG_RUS
        elif operation["language"] == "TUR":
            amount_msg = AMOUNT_MSG_TUR

    await c_back.message.edit_text(f'{c_back.data}')

    await bot.send_message(c_back.from_user.id,
                           amount_msg)

    await FSMClient.buy_cash_amount.set()


async def handle_buy_cash_amount(msg: types.Message, state: FSMContext):

    try:
        buy_cash_amount = number_processing(msg.text)
        async with state.proxy() as operation:
            operation["buy_cash_amount"] = buy_cash_amount

            buy_cash_amount = string_number_to_python(buy_cash_amount)
            buy_cash_rate = string_number_to_python(operation["buy_cash_rate"], bank_round=False)
            buy_cash_result = buy_cash_amount * buy_cash_rate

            if operation["language"] == "ENG":
                buy_cash_confirm_msg = (f'{PURCHASE_FROM_CLIENT_MSG_ENG} '
                                        f'{b_r(buy_cash_amount)} {operation["buy_cash_currency"]}\n'
                                        f'{ISSUED_TO_CLIENT_MSG_ENG} '
                                        f'{b_r(buy_cash_result)} '
                                        f'TL')
                confirm_keyboard = confirm_keyboard_eng
            elif operation["language"] == "RUS":
                buy_cash_confirm_msg = (f'{PURCHASE_FROM_CLIENT_MSG_RUS} '
                                        f'{b_r(buy_cash_amount)} {operation["buy_cash_currency"]}\n'
                                        f'{ISSUED_TO_CLIENT_MSG_RUS} '
                                        f'{b_r(buy_cash_result)} '
                                        f'TL')
                confirm_keyboard = confirm_keyboard_rus
            elif operation["language"] == "TUR":
                buy_cash_confirm_msg = (f'{PURCHASE_FROM_CLIENT_MSG_TUR} '
                                        f'{b_r(buy_cash_amount)} {operation["buy_cash_currency"]}\n'
                                        f'{ISSUED_TO_CLIENT_MSG_TUR} '
                                        f'{b_r(buy_cash_result)} '
                                        f'TL')
                confirm_keyboard = confirm_keyboard_tur

        await bot.send_message(msg.from_user.id,
                               buy_cash_confirm_msg,
                               reply_markup=confirm_keyboard)

        await FSMClient.buy_cash_confirm.set()

    except InvalidOperation:
        await delete_stupid_message(msg)


async def handle_buy_cash_other_currency(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:

        if operation["language"] == "ENG":
            amount_msg = AMOUNT_MSG_ENG
        elif operation["language"] == "RUS":
            amount_msg = AMOUNT_MSG_RUS
        elif operation["language"] == "TUR":
            amount_msg = AMOUNT_MSG_TUR

    await bot.send_message(c_back.from_user.id,
                           amount_msg)

    await FSMClient.buy_cash_other_amount.set()


async def handle_buy_cash_other_amount(msg: types.Message, state: FSMContext):

    try:
        buy_cash_amount = number_processing(msg.text)
        async with state.proxy() as operation:
            operation["buy_cash_amount"] = buy_cash_amount

            if operation["language"] == "ENG":
                buy_cash_other_currency_msg = CURRENCY_MSG_ENG
            elif operation["language"] == "RUS":
                buy_cash_other_currency_msg = CURRENCY_MSG_RUS
            elif operation["language"] == "TUR":
                buy_cash_other_currency_msg = CURRENCY_MSG_TUR

        await bot.send_message(msg.from_user.id,
                               buy_cash_other_currency_msg)

        await FSMClient.buy_cash_other_currency_input.set()

    except InvalidOperation:
        await delete_stupid_message(msg)


async def handle_buy_cash_other_currency_input(msg: types.Message, state: FSMContext):

    async with state.proxy() as operation:
        operation["buy_cash_currency"] = msg.text

        if operation["language"] == "ENG":
            buy_cash_other_currency_msg = OTHER_CURRENCY_RATE_MSG_ENG
        elif operation["language"] == "RUS":
            buy_cash_other_currency_msg = OTHER_CURRENCY_RATE_MSG_RUS
        elif operation["language"] == "TUR":
            buy_cash_other_currency_msg = OTHER_CURRENCY_RATE_MSG_TUR

    await bot.send_message(msg.from_user.id,
                           buy_cash_other_currency_msg)

    await FSMClient.buy_cash_other_rate.set()


async def handle_buy_cash_other_rate(msg: types.Message, state: FSMContext):

    try:
        buy_cash_rate = number_processing(msg.text)
        async with state.proxy() as operation:
            operation["buy_cash_rate"] = buy_cash_rate

            buy_cash_rate = string_number_to_python(buy_cash_rate)
            buy_cash_amount = string_number_to_python(operation["buy_cash_amount"])
            buy_cash_result = buy_cash_amount * buy_cash_rate

            if operation["language"] == "ENG":
                buy_cash_confirm_msg = (f'{PURCHASE_FROM_CLIENT_MSG_ENG} '
                                        f'{b_r(buy_cash_amount)} '
                                        f'{operation["buy_cash_currency"]}\n'
                                        f'{ISSUED_TO_CLIENT_MSG_ENG} '
                                        f'{b_r(buy_cash_result)}'
                                        f'TL')
                confirm_keyboard = confirm_keyboard_eng
            elif operation["language"] == "RUS":
                buy_cash_confirm_msg = (f'{PURCHASE_FROM_CLIENT_MSG_RUS} '
                                        f'{b_r(buy_cash_amount)} '
                                        f'{operation["buy_cash_currency"]}\n'
                                        f'{ISSUED_TO_CLIENT_MSG_RUS} '
                                        f'{b_r(buy_cash_result)}'
                                        f'TL')
                confirm_keyboard = confirm_keyboard_rus
            elif operation["language"] == "TUR":
                buy_cash_confirm_msg = (f'{PURCHASE_FROM_CLIENT_MSG_TUR} '
                                        f'{b_r(buy_cash_amount)} '
                                        f'{operation["buy_cash_currency"]}\n'
                                        f'{ISSUED_TO_CLIENT_MSG_TUR} '
                                        f'{b_r(buy_cash_result)}'
                                        f'TL')
                confirm_keyboard = confirm_keyboard_tur

        await bot.send_message(msg.from_user.id,
                               buy_cash_confirm_msg,
                               reply_markup=confirm_keyboard)

        await FSMClient.buy_cash_confirm.set()

    except InvalidOperation:
        await delete_stupid_message(msg)


async def handle_buy_cash_confirm(c_back: types.CallbackQuery, state: FSMContext):

    today = datetime.now(timezone.utc) + timedelta(hours=3)
    day = today.strftime("%d.%m.%Y")

    async with state.proxy() as operation:
        agent = operation["agent"]
        language = operation["language"]
        amount = operation["buy_cash_amount"]
        currency = operation["buy_cash_currency"]
        if operation["buy_cash_rate"]:
            rate = operation["buy_cash_rate"]
        else:
            rate = None

        if g_sheet_func.buy_cash_save_sheet(agent,
                                            day,
                                            amount,
                                            currency,
                                            rate=rate):
            if operation["language"] == "ENG":
                data_enter_ok_msg = DATA_ENTER_OK_ENG

            elif operation["language"] == "RUS":
                data_enter_ok_msg = DATA_ENTER_OK_RUS

            elif operation["language"] == "TUR":
                data_enter_ok_msg = DATA_ENTER_OK_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_ok_msg)

        else:

            if operation["language"] == "ENG":
                data_enter_fail_msg = DATA_ENTER_FAIL_ENG

            elif operation["language"] == "RUS":
                data_enter_fail_msg = DATA_ENTER_FAIL_RUS

            elif operation["language"] == "TUR":
                data_enter_fail_msg = DATA_ENTER_FAIL_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_fail_msg)

    await delete_inline_keyboard(c_back)
    await continue_operation(agent, language, c_back, state)


# # # EUR to USD

async def handle_eur_to_usd_start(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:
        if operation["language"] == "ENG":
            eur_to_usd_msg = EUR_TO_USD_MSG_ENG
        elif operation["language"] == "RUS":
            eur_to_usd_msg = EUR_TO_USD_MSG_RUS
        elif operation["language"] == "TUR":
            eur_to_usd_msg = EUR_TO_USD_MSG_TUR

    await bot.send_message(c_back.from_user.id,
                           eur_to_usd_msg)
    await FSMClient.eur_to_usd_amount.set()


async def handle_eur_to_usd_amount(msg: types.Message, state: FSMContext):

    try:
        eur_to_usd_amount = number_processing(msg.text)
        async with state.proxy() as operation:
            operation["eur_to_usd_amount"] = eur_to_usd_amount

            eur_to_usd_amount = string_number_to_python(eur_to_usd_amount)

            usd_rate = func_rate('USD_RATE')
            eur_rate = func_rate('EUR_RATE')

            usd_rate = string_number_to_python(usd_rate)
            eur_rate = string_number_to_python(eur_rate)

            eur_to_usd_rate = eur_rate / usd_rate

            eur_to_usd_result = eur_to_usd_amount * eur_to_usd_rate

            if operation["language"] == "ENG":
                eur_to_usd_confirm_msg = (f'{RECEIVED_FROM_CLIENT_MSG_ENG} '
                                          f'{b_r(operation["eur_to_usd_amount"])} EUR\n'
                                          f'{ISSUED_TO_CLIENT_MSG_ENG} '
                                          f'{b_r(eur_to_usd_result)} '
                                          f'USD')
                confirm_keyboard = confirm_keyboard_eng
            elif operation["language"] == "RUS":
                eur_to_usd_confirm_msg = (f'{RECEIVED_FROM_CLIENT_MSG_RUS} '
                                          f'{b_r(operation["eur_to_usd_amount"])} EUR\n'
                                          f'{ISSUED_TO_CLIENT_MSG_RUS} '
                                          f'{b_r(eur_to_usd_result)} '
                                          f'USD')
                confirm_keyboard = confirm_keyboard_rus
            elif operation["language"] == "TUR":
                eur_to_usd_confirm_msg = (f'{RECEIVED_FROM_CLIENT_MSG_TUR} '
                                          f'{b_r(operation["eur_to_usd_amount"])} EUR\n'
                                          f'{ISSUED_TO_CLIENT_MSG_TUR} '
                                          f'{b_r(eur_to_usd_result)} '
                                          f'USD')
                confirm_keyboard = confirm_keyboard_tur

        await bot.send_message(msg.from_user.id,
                               eur_to_usd_confirm_msg,
                               reply_markup=confirm_keyboard)

        await FSMClient.eur_to_usd_confirm.set()

    except InvalidOperation:
        await delete_stupid_message(msg)


async def handle_eur_to_usd_confirm(c_back: types.CallbackQuery, state: FSMContext):

    today = datetime.now(timezone.utc) + timedelta(hours=3)
    day = today.strftime("%d.%m.%Y")

    async with state.proxy() as operation:
        agent = operation["agent"]
        language = operation["language"]
        amount = operation["eur_to_usd_amount"]

        if g_sheet_func.eur_to_usd_save_sheet(agent,
                                              day,
                                              amount):
            if operation["language"] == "ENG":
                data_enter_ok_msg = DATA_ENTER_OK_ENG

            elif operation["language"] == "RUS":
                data_enter_ok_msg = DATA_ENTER_OK_RUS

            elif operation["language"] == "TUR":
                data_enter_ok_msg = DATA_ENTER_OK_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_ok_msg)

        else:

            if operation["language"] == "ENG":
                data_enter_fail_msg = DATA_ENTER_FAIL_ENG

            elif operation["language"] == "RUS":
                data_enter_fail_msg = DATA_ENTER_FAIL_RUS

            elif operation["language"] == "TUR":
                data_enter_fail_msg = DATA_ENTER_FAIL_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_fail_msg)

    await delete_inline_keyboard(c_back)
    await continue_operation(agent, language, c_back, state)


# # # USD to EUR

async def handle_usd_to_eur_start(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:
        if operation["language"] == "ENG":
            usd_to_eur_msg = USD_TO_EUR_MSG_ENG
        elif operation["language"] == "RUS":
            usd_to_eur_msg = USD_TO_EUR_MSG_RUS
        elif operation["language"] == "TUR":
            usd_to_eur_msg = USD_TO_EUR_MSG_TUR

    await bot.send_message(c_back.from_user.id,
                           usd_to_eur_msg)
    await FSMClient.usd_to_eur_amount.set()


async def handle_usd_to_eur_amount(msg: types.Message, state: FSMContext):

    try:
        usd_to_eur_amount = number_processing(msg.text)
        async with state.proxy() as operation:
            operation["usd_to_eur_amount"] = usd_to_eur_amount

            usd_to_eur_amount = string_number_to_python(usd_to_eur_amount)

            usd_rate = func_rate('USD_RATE')
            eur_rate = func_rate('EUR_RATE')

            usd_rate = string_number_to_python(usd_rate)
            eur_rate = string_number_to_python(eur_rate)

            usd_to_eur_rate = usd_rate / eur_rate

            usd_to_eur_result = usd_to_eur_amount * usd_to_eur_rate

            if operation["language"] == "ENG":
                usd_to_eur_confirm_msg = (f'{RECEIVED_FROM_CLIENT_MSG_ENG} '
                                          f'{b_r(operation["usd_to_eur_amount"])} USD\n'
                                          f'{ISSUED_TO_CLIENT_MSG_ENG} '
                                          f'{b_r(usd_to_eur_result)} '
                                          f'EUR')
                confirm_keyboard = confirm_keyboard_eng
            elif operation["language"] == "RUS":
                usd_to_eur_confirm_msg = (f'{RECEIVED_FROM_CLIENT_MSG_RUS} '
                                          f'{b_r(operation["usd_to_eur_amount"])} USD\n'
                                          f'{ISSUED_TO_CLIENT_MSG_RUS} '
                                          f'{b_r(usd_to_eur_result)} '
                                          f'EUR')
                confirm_keyboard = confirm_keyboard_rus
            elif operation["language"] == "TUR":
                usd_to_eur_confirm_msg = (f'{RECEIVED_FROM_CLIENT_MSG_TUR} '
                                          f'{b_r(operation["usd_to_eur_amount"])} USD\n'
                                          f'{ISSUED_TO_CLIENT_MSG_TUR} '
                                          f'{b_r(usd_to_eur_result)} '
                                          f'EUR')
                confirm_keyboard = confirm_keyboard_tur

        await bot.send_message(msg.from_user.id,
                               usd_to_eur_confirm_msg,
                               reply_markup=confirm_keyboard)

        await FSMClient.usd_to_eur_confirm.set()

    except InvalidOperation:
        await delete_stupid_message(msg)


async def handle_usd_to_eur_confirm(c_back: types.CallbackQuery, state: FSMContext):

    today = datetime.now(timezone.utc) + timedelta(hours=3)
    day = today.strftime("%d.%m.%Y")

    async with state.proxy() as operation:
        agent = operation["agent"]
        language = operation["language"]
        amount = operation["usd_to_eur_amount"]

        if g_sheet_func.usd_to_eur_save_sheet(agent,
                                              day,
                                              amount):
            if operation["language"] == "ENG":
                data_enter_ok_msg = DATA_ENTER_OK_ENG

            elif operation["language"] == "RUS":
                data_enter_ok_msg = DATA_ENTER_OK_RUS

            elif operation["language"] == "TUR":
                data_enter_ok_msg = DATA_ENTER_OK_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_ok_msg)

        else:

            if operation["language"] == "ENG":
                data_enter_fail_msg = DATA_ENTER_FAIL_ENG

            elif operation["language"] == "RUS":
                data_enter_fail_msg = DATA_ENTER_FAIL_RUS

            elif operation["language"] == "TUR":
                data_enter_fail_msg = DATA_ENTER_FAIL_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_fail_msg)

    await delete_inline_keyboard(c_back)
    await continue_operation(agent, language, c_back, state)


# # BUY USDT for USD

async def handle_usdt_for_usd_start(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:
        if operation["language"] == "ENG":
            usdt_for_usd_msg = USDT_FOR_USD_MSG_ENG
        elif operation["language"] == "RUS":
            usdt_for_usd_msg = USDT_FOR_USD_MSG_RUS
        elif operation["language"] == "TUR":
            usdt_for_usd_msg = USDT_FOR_USD_MSG_TUR

    await bot.send_message(c_back.from_user.id,
                           usdt_for_usd_msg)
    await FSMClient.usdt_for_usd_amount.set()


async def handle_usdt_for_usd_amount(msg: types.Message, state: FSMContext):

    try:
        usdt_for_usd_amount = number_processing(msg.text)
        async with state.proxy() as operation:
            operation["usdt_for_usd_amount"] = usdt_for_usd_amount

            if operation["language"] == "ENG":
                usdt_for_usd_confirm_msg = (f'{TRANSFERRED_TO_CLIENT_MSG_ENG} '
                                            f'{b_r(operation["usdt_for_usd_amount"])} USDT\n'
                                            f'{RECEIVED_FROM_CLIENT_MSG_ENG} '
                                            f'{b_r(operation["usdt_for_usd_amount"])} USD')
                confirm_keyboard = confirm_keyboard_eng
            elif operation["language"] == "RUS":
                usdt_for_usd_confirm_msg = (f'{TRANSFERRED_TO_CLIENT_MSG_RUS} '
                                            f'{b_r(operation["usdt_for_usd_amount"])} USDT\n'
                                            f'{RECEIVED_FROM_CLIENT_MSG_RUS} '
                                            f'{b_r(operation["usdt_for_usd_amount"])} USD')
                confirm_keyboard = confirm_keyboard_rus
            elif operation["language"] == "TUR":
                usdt_for_usd_confirm_msg = (f'{TRANSFERRED_TO_CLIENT_MSG_TUR} '
                                            f'{b_r(operation["usdt_for_usd_amount"])} USDT\n'
                                            f'{RECEIVED_FROM_CLIENT_MSG_TUR} '
                                            f'{b_r(operation["usdt_for_usd_amount"])} USD')
                confirm_keyboard = confirm_keyboard_tur

        await bot.send_message(msg.from_user.id,
                               usdt_for_usd_confirm_msg,
                               reply_markup=confirm_keyboard)

        await FSMClient.usdt_for_usd_confirm.set()

    except InvalidOperation:
        await delete_stupid_message(msg)


async def handle_usdt_for_usd_confirm(c_back: types.CallbackQuery, state: FSMContext):

    today = datetime.now(timezone.utc) + timedelta(hours=3)
    day = today.strftime("%d.%m.%Y")

    async with state.proxy() as operation:
        agent = operation["agent"]
        language = operation["language"]
        amount = operation["usdt_for_usd_amount"]

        if g_sheet_func.usdt_for_usd_save_sheet(agent,
                                                day,
                                                amount):
            if operation["language"] == "ENG":
                data_enter_ok_msg = DATA_ENTER_OK_ENG

            elif operation["language"] == "RUS":
                data_enter_ok_msg = DATA_ENTER_OK_RUS

            elif operation["language"] == "TUR":
                data_enter_ok_msg = DATA_ENTER_OK_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_ok_msg)

        else:

            if operation["language"] == "ENG":
                data_enter_fail_msg = DATA_ENTER_FAIL_ENG

            elif operation["language"] == "RUS":
                data_enter_fail_msg = DATA_ENTER_FAIL_RUS

            elif operation["language"] == "TUR":
                data_enter_fail_msg = DATA_ENTER_FAIL_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_fail_msg)

    await delete_inline_keyboard(c_back)
    await continue_operation(agent, language, c_back, state)


# # BUY USDT for TL

async def handle_usdt_for_tl_start(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:
        if operation["language"] == "ENG":
            usdt_for_tl_msg = USDT_FOR_TL_MSG_ENG
        elif operation["language"] == "RUS":
            usdt_for_tl_msg = USDT_FOR_TL_MSG_RUS
        elif operation["language"] == "TUR":
            usdt_for_tl_msg = USDT_FOR_TL_MSG_TUR

    await bot.send_message(c_back.from_user.id,
                           usdt_for_tl_msg)
    await FSMClient.usdt_for_tl_amount.set()


async def handle_usdt_for_tl_amount(msg: types.Message, state: FSMContext):

    try:
        usdt_for_tl_amount = number_processing(msg.text)
        async with state.proxy() as operation:
            operation["usdt_for_tl_amount"] = usdt_for_tl_amount

            usdt_for_tl_amount = string_number_to_python(usdt_for_tl_amount)

            usdt_for_tl_rate = func_rate('USDT_TL')

            usdt_for_tl_rate = string_number_to_python(usdt_for_tl_rate)
            
            usdt_for_tl_result = usdt_for_tl_amount * usdt_for_tl_rate

            if operation["language"] == "ENG":
                usdt_for_tl_confirm_msg = (f'{TRANSFERRED_TO_CLIENT_MSG_ENG} '
                                           f'{b_r(operation["usdt_for_tl_amount"])} USDT\n'
                                           f'{RECEIVED_FROM_CLIENT_MSG_ENG} '
                                           f'{b_r(usdt_for_tl_result)} '
                                           f'TL')
                confirm_keyboard = confirm_keyboard_eng
            elif operation["language"] == "RUS":
                usdt_for_tl_confirm_msg = (f'{TRANSFERRED_TO_CLIENT_MSG_RUS} '
                                           f'{b_r(operation["usdt_for_tl_amount"])} USDT\n'
                                           f'{RECEIVED_FROM_CLIENT_MSG_RUS} '
                                           f'{b_r(usdt_for_tl_result)} '
                                           f'TL')
                confirm_keyboard = confirm_keyboard_rus
            elif operation["language"] == "TUR":
                usdt_for_tl_confirm_msg = (f'{TRANSFERRED_TO_CLIENT_MSG_TUR} '
                                           f'{b_r(operation["usdt_for_tl_amount"])} USDT\n'
                                           f'{RECEIVED_FROM_CLIENT_MSG_TUR} '
                                           f'{b_r(usdt_for_tl_result)} '
                                           f'TL')
                confirm_keyboard = confirm_keyboard_tur

        await bot.send_message(msg.from_user.id,
                               usdt_for_tl_confirm_msg,
                               reply_markup=confirm_keyboard)

        await FSMClient.usdt_for_tl_confirm.set()

    except InvalidOperation:
        await delete_stupid_message(msg)


async def handle_usdt_for_tl_confirm(c_back: types.CallbackQuery, state: FSMContext):

    today = datetime.now(timezone.utc) + timedelta(hours=3)
    day = today.strftime("%d.%m.%Y")

    async with state.proxy() as operation:
        agent = operation["agent"]
        language = operation["language"]
        amount = operation["usdt_for_tl_amount"]

        if g_sheet_func.usdt_for_tl_save_sheet(agent,
                                               day,
                                               amount):
            if operation["language"] == "ENG":
                data_enter_ok_msg = DATA_ENTER_OK_ENG

            elif operation["language"] == "RUS":
                data_enter_ok_msg = DATA_ENTER_OK_RUS

            elif operation["language"] == "TUR":
                data_enter_ok_msg = DATA_ENTER_OK_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_ok_msg)

        else:

            if operation["language"] == "ENG":
                data_enter_fail_msg = DATA_ENTER_FAIL_ENG

            elif operation["language"] == "RUS":
                data_enter_fail_msg = DATA_ENTER_FAIL_RUS

            elif operation["language"] == "TUR":
                data_enter_fail_msg = DATA_ENTER_FAIL_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_fail_msg)

    await delete_inline_keyboard(c_back)
    await continue_operation(agent, language, c_back, state)


# # # WE receive

async def handle_wu_receive_start(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:
        if operation["language"] == "ENG":
            wu_receive_msg = WU_RECEIVE_MSG_ENG
        elif operation["language"] == "RUS":
            wu_receive_msg = WU_RECEIVE_MSG_RUS
        elif operation["language"] == "TUR":
            wu_receive_msg = WU_RECEIVE_MSG_TUR

    await bot.send_message(c_back.from_user.id,
                           wu_receive_msg,
                           reply_markup=t_u_e_r_currency_keyboard)

    await FSMClient.wu_receive_currency.set()


async def handle_wu_receive_currency(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:

        if c_back.data == TL_BTN:
            operation["wu_receive_currency"] = "TL"
        elif c_back.data == USD_BTN:
            operation["wu_receive_currency"] = "USD"
        elif c_back.data == EUR_BTN:
            operation["wu_receive_currency"] = "EUR"
        elif c_back.data == RUB_BTN:
            operation["wu_receive_currency"] = "RUB"

        if operation["language"] == "ENG":
            amount_msg = AMOUNT_MSG_ENG
        elif operation["language"] == "RUS":
            amount_msg = AMOUNT_MSG_RUS
        elif operation["language"] == "TUR":
            amount_msg = AMOUNT_MSG_TUR

    await c_back.message.edit_text(f'{c_back.data}')

    await bot.send_message(c_back.from_user.id,
                           amount_msg)

    await FSMClient.wu_receive_amount.set()


async def handle_wu_receive_amount(msg: types.Message, state: FSMContext):

    try:
        wu_receive_amount = number_processing(msg.text)
        async with state.proxy() as operation:
            operation["wu_receive_amount"] = wu_receive_amount

            if operation["language"] == "ENG":
                wu_receive_confirm_msg = (f'{ISSUED_TO_CLIENT_MSG_ENG} '
                                          f'{b_r(operation["wu_receive_amount"])} '
                                          f'{operation["wu_receive_currency"]} '
                                          f'{FROM_WE_MSG_ENG}')
                confirm_keyboard = confirm_keyboard_eng
            elif operation["language"] == "RUS":
                wu_receive_confirm_msg = (f'{ISSUED_TO_CLIENT_MSG_RUS} '
                                          f'{b_r(operation["wu_receive_amount"])} '
                                          f'{operation["wu_receive_currency"]} '
                                          f'{FROM_WE_MSG_RUS}')
                confirm_keyboard = confirm_keyboard_rus
            elif operation["language"] == "TUR":
                wu_receive_confirm_msg = (f'{ISSUED_TO_CLIENT_MSG_TUR} '
                                          f'{b_r(operation["wu_receive_amount"])} '
                                          f'{operation["wu_receive_currency"]} '
                                          f'{FROM_WE_MSG_TUR}')
                confirm_keyboard = confirm_keyboard_tur

        await bot.send_message(msg.from_user.id,
                               wu_receive_confirm_msg,
                               reply_markup=confirm_keyboard)

        await FSMClient.wu_receive_confirm.set()

    except InvalidOperation:
        await delete_stupid_message(msg)


async def handle_wu_receive_confirm(c_back: types.CallbackQuery, state: FSMContext):

    today = datetime.now(timezone.utc) + timedelta(hours=3)
    day = today.strftime("%d.%m.%Y")

    async with state.proxy() as operation:
        agent = operation["agent"]
        language = operation["language"]
        amount = operation["wu_receive_amount"]
        currency = operation["wu_receive_currency"]

        if g_sheet_func.wu_receive_save_sheet(agent,
                                              day,
                                              amount,
                                              currency):
            if operation["language"] == "ENG":
                data_enter_ok_msg = DATA_ENTER_OK_ENG

            elif operation["language"] == "RUS":
                data_enter_ok_msg = DATA_ENTER_OK_RUS

            elif operation["language"] == "TUR":
                data_enter_ok_msg = DATA_ENTER_OK_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_ok_msg)

        else:

            if operation["language"] == "ENG":
                data_enter_fail_msg = DATA_ENTER_FAIL_ENG

            elif operation["language"] == "RUS":
                data_enter_fail_msg = DATA_ENTER_FAIL_RUS

            elif operation["language"] == "TUR":
                data_enter_fail_msg = DATA_ENTER_FAIL_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_fail_msg)

    await delete_inline_keyboard(c_back)
    await continue_operation(agent, language, c_back, state)


# # # WE sending

async def handle_wu_sending_start(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:
        if operation["language"] == "ENG":
            wu_sending_msg = WU_SENDING_MSG_ENG
        elif operation["language"] == "RUS":
            wu_sending_msg = WU_SENDING_MSG_RUS
        elif operation["language"] == "TUR":
            wu_sending_msg = WU_SENDING_MSG_TUR

    await bot.send_message(c_back.from_user.id,
                           wu_sending_msg,
                           reply_markup=t_u_e_r_currency_keyboard)

    await FSMClient.wu_sending_currency.set()


async def handle_wu_sending_currency(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:

        if c_back.data == TL_BTN:
            operation["wu_sending_currency"] = "TL"
        elif c_back.data == USD_BTN:
            operation["wu_sending_currency"] = "USD"
        elif c_back.data == EUR_BTN:
            operation["wu_sending_currency"] = "EUR"
        elif c_back.data == RUB_BTN:
            operation["wu_sending_currency"] = "RUB"

        if operation["language"] == "ENG":
            amount_msg = AMOUNT_MSG_ENG
        elif operation["language"] == "RUS":
            amount_msg = AMOUNT_MSG_RUS
        elif operation["language"] == "TUR":
            amount_msg = AMOUNT_MSG_TUR

    await c_back.message.edit_text(f'{c_back.data}')

    await bot.send_message(c_back.from_user.id,
                           amount_msg)

    await FSMClient.wu_sending_amount.set()


async def handle_wu_sending_amount(msg: types.Message, state: FSMContext):

    try:
        wu_sending_amount = number_processing(msg.text)
        async with state.proxy() as operation:
            operation["wu_sending_amount"] = wu_sending_amount

            if operation["language"] == "ENG":
                wu_sending_confirm_msg = (f'{RECEIVED_FROM_CLIENT_MSG_ENG} '
                                          f'{b_r(operation["wu_sending_amount"])} '
                                          f'{operation["wu_sending_currency"]} '
                                          f'{FOR_WE_MSG_ENG}')
                confirm_keyboard = confirm_keyboard_eng
            elif operation["language"] == "RUS":
                wu_sending_confirm_msg = (f'{RECEIVED_FROM_CLIENT_MSG_ENG} '
                                          f'{b_r(operation["wu_sending_amount"])} '
                                          f'{operation["wu_sending_currency"]} '
                                          f'{FOR_WE_MSG_RUS}')
                confirm_keyboard = confirm_keyboard_rus
            elif operation["language"] == "TUR":
                wu_sending_confirm_msg = (f'{RECEIVED_FROM_CLIENT_MSG_ENG} '
                                          f'{b_r(operation["wu_sending_amount"])} '
                                          f'{operation["wu_sending_currency"]} '
                                          f'{FOR_WE_MSG_TUR}')
                confirm_keyboard = confirm_keyboard_tur

        await bot.send_message(msg.from_user.id,
                               wu_sending_confirm_msg,
                               reply_markup=confirm_keyboard)

        await FSMClient.wu_sending_confirm.set()

    except InvalidOperation:
        await delete_stupid_message(msg)


async def handle_wu_sending_confirm(c_back: types.CallbackQuery, state: FSMContext):

    today = datetime.now(timezone.utc) + timedelta(hours=3)
    day = today.strftime("%d.%m.%Y")

    async with state.proxy() as operation:
        agent = operation["agent"]
        language = operation["language"]
        amount = operation["wu_sending_amount"]
        currency = operation["wu_sending_currency"]

        if g_sheet_func.wu_sending_save_sheet(agent,
                                              day,
                                              amount,
                                              currency):
            if operation["language"] == "ENG":
                data_enter_ok_msg = DATA_ENTER_OK_ENG

            elif operation["language"] == "RUS":
                data_enter_ok_msg = DATA_ENTER_OK_RUS

            elif operation["language"] == "TUR":
                data_enter_ok_msg = DATA_ENTER_OK_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_ok_msg)

        else:

            if operation["language"] == "ENG":
                data_enter_fail_msg = DATA_ENTER_FAIL_ENG

            elif operation["language"] == "RUS":
                data_enter_fail_msg = DATA_ENTER_FAIL_RUS

            elif operation["language"] == "TUR":
                data_enter_fail_msg = DATA_ENTER_FAIL_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_fail_msg)

    await delete_inline_keyboard(c_back)
    await continue_operation(agent, language, c_back, state)


# # # EXPENSES

async def handle_expenses_start(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:
        if operation["language"] == "ENG":
            expenses_msg = CURRENCY_MSG_ENG
            t_u_e_r_o_currency_keyboard = t_u_e_r_o_currency_keyboard_eng
        elif operation["language"] == "RUS":
            expenses_msg = CURRENCY_MSG_RUS
            t_u_e_r_o_currency_keyboard = t_u_e_r_o_currency_keyboard_rus
        elif operation["language"] == "TUR":
            expenses_msg = CURRENCY_MSG_TUR
            t_u_e_r_o_currency_keyboard = t_u_e_r_o_currency_keyboard_tur

    await bot.send_message(c_back.from_user.id,
                           expenses_msg,
                           reply_markup=t_u_e_r_o_currency_keyboard)

    await FSMClient.expenses_currency.set()


async def handle_expenses_currency(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:

        if c_back.data == TL_BTN:
            operation["expenses_currency"] = "TL"
        elif c_back.data == USD_BTN:
            operation["expenses_currency"] = "USD"
        elif c_back.data == EUR_BTN:
            operation["expenses_currency"] = "EUR"
        elif c_back.data == RUB_BTN:
            operation["expenses_currency"] = "RUB"

        if operation["language"] == "ENG":
            amount_msg = AMOUNT_MSG_ENG
        elif operation["language"] == "RUS":
            amount_msg = AMOUNT_MSG_RUS
        elif operation["language"] == "TUR":
            amount_msg = AMOUNT_MSG_TUR

    await c_back.message.edit_text(f'{c_back.data}')

    await bot.send_message(c_back.from_user.id,
                           amount_msg)

    await FSMClient.expenses_amount.set()


async def handle_expenses_other_currency(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    async with state.proxy() as operation:

        if operation["language"] == "ENG":
            other_currency_msg = CURRENCY_MSG_ENG
        elif operation["language"] == "RUS":
            other_currency_msg = CURRENCY_MSG_RUS
        elif operation["language"] == "TUR":
            other_currency_msg = CURRENCY_MSG_TUR

    await bot.send_message(c_back.from_user.id,
                           other_currency_msg)

    await FSMClient.expenses_other_currency_input.set()


async def handle_expenses_other_currency_input(msg: types.Message, state: FSMContext):

    async with state.proxy() as operation:
        operation["expenses_currency"] = msg.text

        if operation["language"] == "ENG":
            amount_msg = AMOUNT_MSG_ENG
        elif operation["language"] == "RUS":
            amount_msg = AMOUNT_MSG_RUS
        elif operation["language"] == "TUR":
            amount_msg = AMOUNT_MSG_TUR

    await bot.send_message(msg.from_user.id,
                           amount_msg)

    await FSMClient.expenses_amount.set()


async def handle_expenses_amount(msg: types.Message, state: FSMContext):

    try:
        expenses_amount = number_processing(msg.text)
        async with state.proxy() as operation:
            operation["expenses_amount"] = expenses_amount

            if operation["language"] == "ENG":
                explanation_msg = EXPLANATION_MSG_ENG
            elif operation["language"] == "RUS":
                explanation_msg = EXPLANATION_MSG_RUS
            elif operation["language"] == "TUR":
                explanation_msg = EXPLANATION_MSG_TUR

        await bot.send_message(msg.from_user.id,
                               explanation_msg)

        await FSMClient.expenses_explanation.set()

    except InvalidOperation:
        await delete_stupid_message(msg)


async def handle_expenses_explanation(msg: types.Message, state: FSMContext):

    async with state.proxy() as operation:
        operation["expenses_explanation"] = msg.text

        if operation["language"] == "ENG":
            expenses_confirm_msg = (f'Add '
                                    f'{b_r(operation["expenses_amount"])} '
                                    f'{operation["expenses_currency"]} '
                                    f'to EXPENSES with explanation: \n'
                                    f'«{operation["expenses_explanation"]}»?')
            confirm_keyboard = confirm_keyboard_eng

        elif operation["language"] == "RUS":
            expenses_confirm_msg = (f'Добавить '
                                    f'{b_r(operation["expenses_amount"])} '
                                    f'{operation["expenses_currency"]} '
                                    f'в РАСХОДЫ с объяснением: \n'
                                    f'«{operation["expenses_explanation"]}»?')
            confirm_keyboard = confirm_keyboard_rus

        elif operation["language"] == "TUR":
            expenses_confirm_msg = (f"«{operation['expenses_explanation']}» "
                                    f"açıklaması ile GİDERLER'e "
                                    f"{b_r(operation['expenses_amount'])} "
                                    f"{operation['expenses_currency']} "
                                    f"eklensin mi?")
            confirm_keyboard = confirm_keyboard_tur

    await bot.send_message(msg.from_user.id,
                           expenses_confirm_msg,
                           reply_markup=confirm_keyboard)

    await FSMClient.expenses_confirm.set()


async def handle_expenses_confirm(c_back: types.CallbackQuery, state: FSMContext):

    today = datetime.now(timezone.utc) + timedelta(hours=3)
    day = today.strftime("%d.%m.%Y")

    async with state.proxy() as operation:
        agent = operation["agent"]
        language = operation["language"]
        amount = operation["expenses_amount"]
        currency = operation["expenses_currency"]
        explanation = operation["expenses_explanation"]

        if g_sheet_func.expenses_save_sheet(agent,
                                            day,
                                            amount,
                                            currency,
                                            explanation):
            if operation["language"] == "ENG":
                data_enter_ok_msg = DATA_ENTER_OK_ENG

            elif operation["language"] == "RUS":
                data_enter_ok_msg = DATA_ENTER_OK_RUS

            elif operation["language"] == "TUR":
                data_enter_ok_msg = DATA_ENTER_OK_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_ok_msg)

        else:

            if operation["language"] == "ENG":
                data_enter_fail_msg = DATA_ENTER_FAIL_ENG

            elif operation["language"] == "RUS":
                data_enter_fail_msg = DATA_ENTER_FAIL_RUS

            elif operation["language"] == "TUR":
                data_enter_fail_msg = DATA_ENTER_FAIL_TUR

            await bot.send_message(c_back.from_user.id,
                                   data_enter_fail_msg)

    await delete_inline_keyboard(c_back)
    await continue_operation(agent, language, c_back, state)

# ###################################################################################################


def register_handlers_client(dp: Dispatcher):

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
    # # # LANGUAGE HANDLERS

    dp.register_callback_query_handler(handle_language_eng,
                                       lambda c: c.data == LANG_BTN_ENG,
                                       state=None
                                       )

    dp.register_callback_query_handler(handle_language_rus,
                                       lambda c: c.data == LANG_BTN_RUS,
                                       state=None
                                       )

    dp.register_callback_query_handler(handle_language_tur,
                                       lambda c: c.data == LANG_BTN_TUR,
                                       state=None
                                       )

    dp.register_message_handler(handle_password,
                                content_types=["text"],
                                state=FSMClient.language
                                )

    # # # MAIN MENU HANDLERS

    # # # # DAY START
    dp.register_callback_query_handler(handle_day_start,
                                       lambda c: c.data == DAY_START_BTN_ENG,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_day_start,
                                       lambda c: c.data == DAY_START_BTN_RUS,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_day_start,
                                       lambda c: c.data == DAY_START_BTN_TUR,
                                       state=FSMClient.main_menu
                                       )

    dp.register_message_handler(handle_day_start_tl,
                                content_types=["text"],
                                state=FSMClient.day_start_tl
                                )

    dp.register_message_handler(handle_day_start_usd,
                                content_types=["text"],
                                state=FSMClient.day_start_usd
                                )

    dp.register_message_handler(handle_day_start_eur,
                                content_types=["text"],
                                state=FSMClient.day_start_eur
                                )

    dp.register_message_handler(handle_day_start_rub,
                                content_types=["text"],
                                state=FSMClient.day_start_rub
                                )

    dp.register_callback_query_handler(handle_day_start_confirm,
                                       lambda c: c.data == SAVE_BTN_ENG,
                                       state=FSMClient.day_start_confirm
                                       )

    dp.register_callback_query_handler(handle_day_start_confirm,
                                       lambda c: c.data == SAVE_BTN_RUS,
                                       state=FSMClient.day_start_confirm
                                       )

    dp.register_callback_query_handler(handle_day_start_confirm,
                                       lambda c: c.data == SAVE_BTN_TUR,
                                       state=FSMClient.day_start_confirm
                                       )
    # # # # MONEY INCOME

    dp.register_callback_query_handler(handle_money_income_start,
                                       lambda c: c.data == MONEY_INCOME_BTN_ENG,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_money_income_start,
                                       lambda c: c.data == MONEY_INCOME_BTN_RUS,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_money_income_start,
                                       lambda c: c.data == MONEY_INCOME_BTN_TUR,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_money_income_currency,
                                       lambda c: c.data == TL_BTN,
                                       state=FSMClient.money_income_currency
                                       )

    dp.register_callback_query_handler(handle_money_income_currency,
                                       lambda c: c.data == USD_BTN,
                                       state=FSMClient.money_income_currency
                                       )

    dp.register_callback_query_handler(handle_money_income_currency,
                                       lambda c: c.data == EUR_BTN,
                                       state=FSMClient.money_income_currency
                                       )

    dp.register_callback_query_handler(handle_money_income_currency,
                                       lambda c: c.data == RUB_BTN,
                                       state=FSMClient.money_income_currency
                                       )

    dp.register_message_handler(handle_money_income_amount,
                                content_types=["text"],
                                state=FSMClient.money_income_amount
                                )

    dp.register_callback_query_handler(handle_money_income_confirm,
                                       lambda c: c.data == SAVE_BTN_ENG,
                                       state=FSMClient.money_income_confirm
                                       )

    dp.register_callback_query_handler(handle_money_income_confirm,
                                       lambda c: c.data == SAVE_BTN_RUS,
                                       state=FSMClient.money_income_confirm
                                       )

    dp.register_callback_query_handler(handle_money_income_confirm,
                                       lambda c: c.data == SAVE_BTN_TUR,
                                       state=FSMClient.money_income_confirm
                                       )

    # # # # SELL RUBCARD

    dp.register_callback_query_handler(handle_sell_rubcard_start,
                                       lambda c: c.data == SELL_RUBCARD_BTN_ENG,
                                       state=FSMClient.main_menu
                                       )
    dp.register_callback_query_handler(handle_sell_rubcard_start,
                                       lambda c: c.data == SELL_RUBCARD_BTN_RUS,
                                       state=FSMClient.main_menu
                                       )
    dp.register_callback_query_handler(handle_sell_rubcard_start,
                                       lambda c: c.data == SELL_RUBCARD_BTN_TUR,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_sell_rubcard_currency,
                                       lambda c: c.data == TL_BTN,
                                       state=FSMClient.sell_rubcard_currency
                                       )

    dp.register_callback_query_handler(handle_sell_rubcard_currency,
                                       lambda c: c.data == USD_BTN,
                                       state=FSMClient.sell_rubcard_currency
                                       )

    dp.register_callback_query_handler(handle_sell_rubcard_currency,
                                       lambda c: c.data == EUR_BTN,
                                       state=FSMClient.sell_rubcard_currency
                                       )

    dp.register_message_handler(handle_sell_rubcard_amount,
                                content_types=["text"],
                                state=FSMClient.sell_rubcard_amount
                                )

    dp.register_callback_query_handler(handle_sell_rubcard_confirm,
                                       lambda c: c.data == SAVE_BTN_ENG,
                                       state=FSMClient.sell_rubcard_confirm
                                       )

    dp.register_callback_query_handler(handle_sell_rubcard_confirm,
                                       lambda c: c.data == SAVE_BTN_RUS,
                                       state=FSMClient.sell_rubcard_confirm
                                       )

    dp.register_callback_query_handler(handle_sell_rubcard_confirm,
                                       lambda c: c.data == SAVE_BTN_TUR,
                                       state=FSMClient.sell_rubcard_confirm
                                       )

    # # # # BUY RUBCARD

    dp.register_callback_query_handler(handle_buy_rubcard_start,
                                       lambda c: c.data == BUY_RUBCARD_BTN_ENG,
                                       state=FSMClient.main_menu
                                       )
    dp.register_callback_query_handler(handle_buy_rubcard_start,
                                       lambda c: c.data == BUY_RUBCARD_BTN_RUS,
                                       state=FSMClient.main_menu
                                       )
    dp.register_callback_query_handler(handle_buy_rubcard_start,
                                       lambda c: c.data == BUY_RUBCARD_BTN_TUR,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_buy_rubcard_currency,
                                       lambda c: c.data == TL_BTN,
                                       state=FSMClient.buy_rubcard_currency
                                       )

    dp.register_callback_query_handler(handle_buy_rubcard_currency,
                                       lambda c: c.data == USD_BTN,
                                       state=FSMClient.buy_rubcard_currency
                                       )

    dp.register_callback_query_handler(handle_buy_rubcard_currency,
                                       lambda c: c.data == EUR_BTN,
                                       state=FSMClient.buy_rubcard_currency
                                       )

    dp.register_message_handler(handle_buy_rubcard_amount,
                                content_types=["text"],
                                state=FSMClient.buy_rubcard_amount
                                )

    dp.register_callback_query_handler(handle_buy_rubcard_confirm,
                                       lambda c: c.data == SAVE_BTN_ENG,
                                       state=FSMClient.buy_rubcard_confirm
                                       )

    dp.register_callback_query_handler(handle_buy_rubcard_confirm,
                                       lambda c: c.data == SAVE_BTN_RUS,
                                       state=FSMClient.buy_rubcard_confirm
                                       )

    dp.register_callback_query_handler(handle_buy_rubcard_confirm,
                                       lambda c: c.data == SAVE_BTN_TUR,
                                       state=FSMClient.buy_rubcard_confirm
                                       )

    # # # BUY CASH

    dp.register_callback_query_handler(handle_buy_cash_start,
                                       lambda c: c.data == BUY_CASH_BTN_ENG,
                                       state=FSMClient.main_menu
                                       )
    dp.register_callback_query_handler(handle_buy_cash_start,
                                       lambda c: c.data == BUY_CASH_BTN_RUS,
                                       state=FSMClient.main_menu
                                       )
    dp.register_callback_query_handler(handle_buy_cash_start,
                                       lambda c: c.data == BUY_CASH_BTN_TUR,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_buy_cash_currency,
                                       lambda c: c.data == USD_BTN,
                                       state=FSMClient.buy_cash_currency
                                       )

    dp.register_callback_query_handler(handle_buy_cash_currency,
                                       lambda c: c.data == EUR_BTN,
                                       state=FSMClient.buy_cash_currency
                                       )

    dp.register_callback_query_handler(handle_buy_cash_currency,
                                       lambda c: c.data == RUB_BTN,
                                       state=FSMClient.buy_cash_currency
                                       )

    dp.register_message_handler(handle_buy_cash_amount,
                                content_types=["text"],
                                state=FSMClient.buy_cash_amount
                                )

    dp.register_callback_query_handler(handle_buy_cash_other_currency,
                                       lambda c: c.data == OTHER_BTN_ENG,
                                       state=FSMClient.buy_cash_currency
                                       )

    dp.register_callback_query_handler(handle_buy_cash_other_currency,
                                       lambda c: c.data == OTHER_BTN_RUS,
                                       state=FSMClient.buy_cash_currency
                                       )

    dp.register_callback_query_handler(handle_buy_cash_other_currency,
                                       lambda c: c.data == OTHER_BTN_TUR,
                                       state=FSMClient.buy_cash_currency
                                       )

    dp.register_message_handler(handle_buy_cash_other_amount,
                                content_types=["text"],
                                state=FSMClient.buy_cash_other_amount
                                )

    dp.register_message_handler(handle_buy_cash_other_currency_input,
                                content_types=["text"],
                                state=FSMClient.buy_cash_other_currency_input
                                )

    dp.register_message_handler(handle_buy_cash_other_rate,
                                content_types=["text"],
                                state=FSMClient.buy_cash_other_rate
                                )

    dp.register_callback_query_handler(handle_buy_cash_confirm,
                                       lambda c: c.data == SAVE_BTN_ENG,
                                       state=FSMClient.buy_cash_confirm
                                       )

    dp.register_callback_query_handler(handle_buy_cash_confirm,
                                       lambda c: c.data == SAVE_BTN_RUS,
                                       state=FSMClient.buy_cash_confirm
                                       )

    dp.register_callback_query_handler(handle_buy_cash_confirm,
                                       lambda c: c.data == SAVE_BTN_TUR,
                                       state=FSMClient.buy_cash_confirm
                                       )

    # # # EUR to USD

    dp.register_callback_query_handler(handle_eur_to_usd_start,
                                       lambda c: c.data == EUR_TO_USD_BTN,
                                       state=FSMClient.main_menu
                                       )

    dp.register_message_handler(handle_eur_to_usd_amount,
                                content_types=["text"],
                                state=FSMClient.eur_to_usd_amount
                                )

    dp.register_callback_query_handler(handle_eur_to_usd_confirm,
                                       lambda c: c.data == SAVE_BTN_ENG,
                                       state=FSMClient.eur_to_usd_confirm
                                       )

    dp.register_callback_query_handler(handle_eur_to_usd_confirm,
                                       lambda c: c.data == SAVE_BTN_RUS,
                                       state=FSMClient.eur_to_usd_confirm
                                       )

    dp.register_callback_query_handler(handle_eur_to_usd_confirm,
                                       lambda c: c.data == SAVE_BTN_TUR,
                                       state=FSMClient.eur_to_usd_confirm
                                       )

    # # # USD to EUR

    dp.register_callback_query_handler(handle_usd_to_eur_start,
                                       lambda c: c.data == USD_TO_EUR_BTN,
                                       state=FSMClient.main_menu
                                       )

    dp.register_message_handler(handle_usd_to_eur_amount,
                                content_types=["text"],
                                state=FSMClient.usd_to_eur_amount
                                )

    dp.register_callback_query_handler(handle_usd_to_eur_confirm,
                                       lambda c: c.data == SAVE_BTN_ENG,
                                       state=FSMClient.usd_to_eur_confirm
                                       )

    dp.register_callback_query_handler(handle_usd_to_eur_confirm,
                                       lambda c: c.data == SAVE_BTN_RUS,
                                       state=FSMClient.usd_to_eur_confirm
                                       )

    dp.register_callback_query_handler(handle_usd_to_eur_confirm,
                                       lambda c: c.data == SAVE_BTN_TUR,
                                       state=FSMClient.usd_to_eur_confirm
                                       )

    # # # USDT for USD

    dp.register_callback_query_handler(handle_usdt_for_usd_start,
                                       lambda c: c.data == USDT_USD_BTN_ENG,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_usdt_for_usd_start,
                                       lambda c: c.data == USDT_USD_BTN_RUS,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_usdt_for_usd_start,
                                       lambda c: c.data == USDT_USD_BTN_TUR,
                                       state=FSMClient.main_menu
                                       )

    dp.register_message_handler(handle_usdt_for_usd_amount,
                                content_types=["text"],
                                state=FSMClient.usdt_for_usd_amount
                                )

    dp.register_callback_query_handler(handle_usdt_for_usd_confirm,
                                       lambda c: c.data == SAVE_BTN_ENG,
                                       state=FSMClient.usdt_for_usd_confirm
                                       )

    dp.register_callback_query_handler(handle_usdt_for_usd_confirm,
                                       lambda c: c.data == SAVE_BTN_RUS,
                                       state=FSMClient.usdt_for_usd_confirm
                                       )

    dp.register_callback_query_handler(handle_usdt_for_usd_confirm,
                                       lambda c: c.data == SAVE_BTN_TUR,
                                       state=FSMClient.usdt_for_usd_confirm
                                       )

    # # # USDT for TL

    dp.register_callback_query_handler(handle_usdt_for_tl_start,
                                       lambda c: c.data == USDT_TL_BTN_ENG,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_usdt_for_tl_start,
                                       lambda c: c.data == USDT_TL_BTN_RUS,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_usdt_for_tl_start,
                                       lambda c: c.data == USDT_TL_BTN_TUR,
                                       state=FSMClient.main_menu
                                       )

    dp.register_message_handler(handle_usdt_for_tl_amount,
                                content_types=["text"],
                                state=FSMClient.usdt_for_tl_amount
                                )

    dp.register_callback_query_handler(handle_usdt_for_tl_confirm,
                                       lambda c: c.data == SAVE_BTN_ENG,
                                       state=FSMClient.usdt_for_tl_confirm
                                       )

    dp.register_callback_query_handler(handle_usdt_for_tl_confirm,
                                       lambda c: c.data == SAVE_BTN_RUS,
                                       state=FSMClient.usdt_for_tl_confirm
                                       )

    dp.register_callback_query_handler(handle_usdt_for_tl_confirm,
                                       lambda c: c.data == SAVE_BTN_TUR,
                                       state=FSMClient.usdt_for_tl_confirm
                                       )

    # # # WU receive

    dp.register_callback_query_handler(handle_wu_receive_start,
                                       lambda c: c.data == WU_RECEIVE_BTN_ENG,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_wu_receive_start,
                                       lambda c: c.data == WU_RECEIVE_BTN_RUS,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_wu_receive_start,
                                       lambda c: c.data == WU_RECEIVE_BTN_TUR,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_wu_receive_currency,
                                       lambda c: c.data == TL_BTN,
                                       state=FSMClient.wu_receive_currency
                                       )

    dp.register_callback_query_handler(handle_wu_receive_currency,
                                       lambda c: c.data == USD_BTN,
                                       state=FSMClient.wu_receive_currency
                                       )

    dp.register_callback_query_handler(handle_wu_receive_currency,
                                       lambda c: c.data == EUR_BTN,
                                       state=FSMClient.wu_receive_currency
                                       )

    dp.register_callback_query_handler(handle_wu_receive_currency,
                                       lambda c: c.data == RUB_BTN,
                                       state=FSMClient.wu_receive_currency
                                       )

    dp.register_message_handler(handle_wu_receive_amount,
                                content_types=["text"],
                                state=FSMClient.wu_receive_amount
                                )

    dp.register_callback_query_handler(handle_wu_receive_confirm,
                                       lambda c: c.data == SAVE_BTN_ENG,
                                       state=FSMClient.wu_receive_confirm
                                       )

    dp.register_callback_query_handler(handle_wu_receive_confirm,
                                       lambda c: c.data == SAVE_BTN_RUS,
                                       state=FSMClient.wu_receive_confirm
                                       )

    dp.register_callback_query_handler(handle_wu_receive_confirm,
                                       lambda c: c.data == SAVE_BTN_TUR,
                                       state=FSMClient.wu_receive_confirm
                                       )

    # # # WU sending

    dp.register_callback_query_handler(handle_wu_sending_start,
                                       lambda c: c.data == WU_SENDING_BTN_ENG,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_wu_sending_start,
                                       lambda c: c.data == WU_SENDING_BTN_RUS,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_wu_sending_start,
                                       lambda c: c.data == WU_SENDING_BTN_TUR,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_wu_sending_currency,
                                       lambda c: c.data == TL_BTN,
                                       state=FSMClient.wu_sending_currency
                                       )

    dp.register_callback_query_handler(handle_wu_sending_currency,
                                       lambda c: c.data == USD_BTN,
                                       state=FSMClient.wu_sending_currency
                                       )

    dp.register_callback_query_handler(handle_wu_sending_currency,
                                       lambda c: c.data == EUR_BTN,
                                       state=FSMClient.wu_sending_currency
                                       )

    dp.register_callback_query_handler(handle_wu_sending_currency,
                                       lambda c: c.data == RUB_BTN,
                                       state=FSMClient.wu_sending_currency
                                       )

    dp.register_message_handler(handle_wu_sending_amount,
                                content_types=["text"],
                                state=FSMClient.wu_sending_amount
                                )

    dp.register_callback_query_handler(handle_wu_sending_confirm,
                                       lambda c: c.data == SAVE_BTN_ENG,
                                       state=FSMClient.wu_sending_confirm
                                       )

    dp.register_callback_query_handler(handle_wu_sending_confirm,
                                       lambda c: c.data == SAVE_BTN_RUS,
                                       state=FSMClient.wu_sending_confirm
                                       )

    dp.register_callback_query_handler(handle_wu_sending_confirm,
                                       lambda c: c.data == SAVE_BTN_TUR,
                                       state=FSMClient.wu_sending_confirm
                                       )

    # # # EXPENSES

    dp.register_callback_query_handler(handle_expenses_start,
                                       lambda c: c.data == EXPENSES_BTN_ENG,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_expenses_start,
                                       lambda c: c.data == EXPENSES_BTN_RUS,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_expenses_start,
                                       lambda c: c.data == EXPENSES_BTN_TUR,
                                       state=FSMClient.main_menu
                                       )

    dp.register_callback_query_handler(handle_expenses_currency,
                                       lambda c: c.data == TL_BTN,
                                       state=FSMClient.expenses_currency
                                       )

    dp.register_callback_query_handler(handle_expenses_currency,
                                       lambda c: c.data == USD_BTN,
                                       state=FSMClient.expenses_currency
                                       )

    dp.register_callback_query_handler(handle_expenses_currency,
                                       lambda c: c.data == EUR_BTN,
                                       state=FSMClient.expenses_currency
                                       )

    dp.register_callback_query_handler(handle_expenses_currency,
                                       lambda c: c.data == RUB_BTN,
                                       state=FSMClient.expenses_currency
                                       )

    dp.register_callback_query_handler(handle_expenses_other_currency,
                                       lambda c: c.data == OTHER_BTN_ENG,
                                       state=FSMClient.expenses_currency
                                       )

    dp.register_callback_query_handler(handle_expenses_other_currency,
                                       lambda c: c.data == OTHER_BTN_RUS,
                                       state=FSMClient.expenses_currency
                                       )

    dp.register_callback_query_handler(handle_expenses_other_currency,
                                       lambda c: c.data == OTHER_BTN_TUR,
                                       state=FSMClient.expenses_currency
                                       )

    dp.register_message_handler(handle_expenses_other_currency_input,
                                content_types=["text"],
                                state=FSMClient.expenses_other_currency_input
                                )

    dp.register_message_handler(handle_expenses_amount,
                                content_types=["text"],
                                state=FSMClient.expenses_amount
                                )

    dp.register_message_handler(handle_expenses_explanation,
                                content_types=["text"],
                                state=FSMClient.expenses_explanation
                                )

    dp.register_callback_query_handler(handle_expenses_confirm,
                                       lambda c: c.data == SAVE_BTN_ENG,
                                       state=FSMClient.expenses_confirm
                                       )

    dp.register_callback_query_handler(handle_expenses_confirm,
                                       lambda c: c.data == SAVE_BTN_RUS,
                                       state=FSMClient.expenses_confirm
                                       )

    dp.register_callback_query_handler(handle_expenses_confirm,
                                       lambda c: c.data == SAVE_BTN_TUR,
                                       state=FSMClient.expenses_confirm
                                       )
