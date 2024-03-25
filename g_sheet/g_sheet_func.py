import gspread
from gspread.utils import column_letter_to_index
from gspread.exceptions import APIError, WorksheetNotFound
from oauth2client.service_account import ServiceAccountCredentials
from os import environ

# own imports
from create_bot import SERVER, GOOGLE_SHEET_KEY
from data_base.db_action import read_rate
from number_funcs import string_number_to_python,decimal_number_to_string

# constants imports
if SERVER == "HEROKU":
    func_rate = environ.get
else:
    func_rate = read_rate

# GoogleSheetsAuth
s = ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name("g_sheet/gs_credentials.json", s)
client = gspread.authorize(creds)

spreadsheet = client.open_by_key(GOOGLE_SHEET_KEY)

# COMMON FUNCTIONS

def last_index(sheet: gspread.Worksheet, column: str) -> str:

    """
    :param sheet: gspread.Worksheet
    :param column: column letter
    :return: index of the first unfilled cell in inputted column in A1 format
    """

    column_digital_index = column_letter_to_index(column)
    row = str((len(sheet.col_values(column_digital_index)) + 1))
    index = column + row
    return index


def last_total_index(sheet: gspread.Worksheet, column: str, total_column: str) -> str:

    """
    :param sheet: gspread.Worksheet
    :param column: column letter
    :param column: column letter of total amount
    :return: index of the first unfilled cell in inputted column in A1 format
    """

    column_digital_index = column_letter_to_index(total_column)
    row = str((len(sheet.col_values(column_digital_index)) + 1))
    index = column + row
    return index


def create_agent_day_sheet(agent: str,
                           day: str,
                           start_tl: str,
                           start_usd: str,
                           start_eur: str,
                           start_rub: str) -> bool:
    """
    :param agent: Name of agent for new worksheet title
    :param day: Current date DD.MM.YYYY for new worksheet title
    :param start_tl: Amount of TL in the cashier at day's start
    :param start_usd: Amount of USD in the cashier at day's start
    :param start_eur: Amount of EUR in the cashier at day's start
    :param start_rub: Amount of RUB in the cashier at day's start
    :return: True: If worksheet with title 'agent day' successfully created;
    False: If worksheet with title 'agent day' already exist
    """
    try:
        agent_day = agent + ' ' + day
        worksheet_list = spreadsheet.worksheets()
        agent_day_sheet = spreadsheet.duplicate_sheet(0,
                                                      insert_sheet_index=len(worksheet_list),
                                                      new_sheet_id=None,
                                                      new_sheet_name=agent_day
                                                      )
        agent_day_sheet.update('A1', agent)
        agent_day_sheet.update('A2', day)

        agent_day_sheet.update('B3', start_tl, value_input_option='USER_ENTERED')
        agent_day_sheet.update('C3', start_usd, value_input_option='USER_ENTERED')
        agent_day_sheet.update('D3', start_eur, value_input_option='USER_ENTERED')
        agent_day_sheet.update('E3', start_rub, value_input_option='USER_ENTERED')

        return True
    except APIError:
        return False
    except WorksheetNotFound:
        return False


def money_income_save_sheet(agent: str,
                            day: str,
                            amount: str,
                            currency: str,
                            ) -> bool:

    """
    :param agent: Name of agent for search the worksheet title
    :param day: Current date DD.MM.YYYY for search the worksheet title
    :param amount: Amount of money to add in the cashier
    :param currency: Currency of money to add in the cashier
    :return: True: If data successfully added to the worksheet;
    False: If worksheet with the title 'agent day' don't exist
    """

    try:
        agent_day = agent + ' ' + day
        agent_day_sheet = spreadsheet.worksheet(title=agent_day)

        if currency == "TL":
            column = 'AZ'
        elif currency == "USD":
            column = 'BA'
        elif currency == "EUR":
            column = 'BB'
        elif currency == "RUB":
            column = 'BC'
        else:
            return False

        index = last_index(agent_day_sheet, column)
        agent_day_sheet.update(index, amount, value_input_option='USER_ENTERED')

        return True

    except APIError:
        return False
    except WorksheetNotFound:
        return False


def sell_rubcard_save_sheet(agent: str,
                            day: str,
                            amount: str,
                            currency: str,
                            ) -> bool:
    """
        :param agent: Name of agent for search the worksheet title
        :param day: Current date DD.MM.YYYY for search the worksheet title
        :param amount: Amount of money to sell for RUB CARD
        :param currency: Currency of money to sell for RUB CARD
        :return: True: If data successfully added to the worksheet;
        False: If worksheet with the title 'agent day' don't exist
    """

    try:
        agent_day = agent + ' ' + day
        agent_day_sheet = spreadsheet.worksheet(title=agent_day)

        column_result = 'F'

        if currency == "TL":
            column_amount = 'H'
            column_rate = 'G'
            rate = func_rate("MIR_TL")
        elif currency == "USD":
            column_amount = 'J'
            column_rate = 'I'
            rate = func_rate("MIR_USD")
        elif currency == "EUR":
            column_amount = 'L'
            column_rate = 'K'
            rate = func_rate("MIR_EUR")
        else:
            return False

        index_rate = last_total_index(agent_day_sheet, column_rate, column_result)
        agent_day_sheet.update(index_rate, rate, value_input_option='USER_ENTERED')

        index_amount = last_total_index(agent_day_sheet, column_amount, column_result)
        agent_day_sheet.update(index_amount, amount, value_input_option='USER_ENTERED')

        index_result = last_index(agent_day_sheet, column_result)

        result_amount = string_number_to_python(amount)
        result_rate = string_number_to_python(rate)
        result = result_amount * result_rate
        result_string = decimal_number_to_string(result)

        agent_day_sheet.update(index_result, result_string, value_input_option='USER_ENTERED')
        return True

    except APIError:
        return False
    except WorksheetNotFound:
        return False


def buy_rubcard_save_sheet(agent: str,
                           day: str,
                           amount: str,
                           currency: str,
                           ) -> bool:
    """
        :param agent: Name of agent for search the worksheet title
        :param day: Current date DD.MM.YYYY for search the worksheet title
        :param amount: Amount of money to purchase from client for RUB CARD
        :param currency: Currency of money  to purchase from client for RUB CARD
        :return: True: If data successfully added to the worksheet;
        False: If worksheet with the title 'agent day' don't exist
    """

    try:
        agent_day = agent + ' ' + day
        agent_day_sheet = spreadsheet.worksheet(title=agent_day)

        column_result = 'M'

        if currency == "TL":
            column_amount = 'O'
            column_rate = 'N'
            rate = func_rate("MIR_TL")

        elif currency == "USD":
            column_amount = 'Q'
            column_rate = 'P'
            rate = func_rate("MIR_USD")

        elif currency == "EUR":
            column_amount = 'S'
            column_rate = 'R'
            rate = func_rate("MIR_EUR")

        else:
            return False

        index_rate = last_total_index(agent_day_sheet, column_rate, column_result)
        agent_day_sheet.update(index_rate, rate, value_input_option='USER_ENTERED')

        index_amount = last_total_index(agent_day_sheet, column_amount, column_result)
        agent_day_sheet.update(index_amount, amount, value_input_option='USER_ENTERED')

        index_result = last_index(agent_day_sheet, column_result)

        result_amount = string_number_to_python(amount)
        result_rate = string_number_to_python(rate)
        result = result_amount * result_rate
        result_string = decimal_number_to_string(result)

        agent_day_sheet.update(index_result, result_string, value_input_option='USER_ENTERED')
        return True

    except APIError:
        return False
    except WorksheetNotFound:
        return False


def buy_cash_save_sheet(agent: str,
                        day: str,
                        amount: str,
                        currency: str,
                        standard_rate=None,
                        rate=None
                        ) -> bool:
    """
        :param agent: Name of agent for search the worksheet title
        :param day: Current date DD.MM.YYYY for search the worksheet title
        :param amount: Amount of cash to purchase from client for TL
        :param currency: Currency of cash to purchase from client for TL
        :param standard_rate: If the chosen currency is USD, EUR or RUB
        - filled automatically from environment variables
        :param rate: If the chosen currency is different from USD, EUR or RUB,
        - the agent must enter its exchange rate to the TL
        :return: True: If data successfully added to the worksheet;
        False: If worksheet with the title 'agent day' don't exist
    """

    try:
        agent_day = agent + ' ' + day
        agent_day_sheet = spreadsheet.worksheet(title=agent_day)

        if currency == "USD":
            column_amount = 'T'
            column_rate = 'U'
            column_result = 'V'
            standard_rate = func_rate("USD_RATE")

            result_rate = string_number_to_python(standard_rate)

        elif currency == "EUR":
            column_amount = 'W'
            column_rate = 'X'
            column_result = 'Y'
            standard_rate = func_rate("EUR_RATE")
            result_rate = string_number_to_python(standard_rate)

        elif currency == "RUB":
            column_amount = 'Z'
            column_rate = 'AA'
            column_result = 'AB'
            standard_rate = func_rate("RUB_RATE")
            result_rate = (1 / string_number_to_python(standard_rate))

        else:
            amount_for_other_result = amount
            amount = amount + ' ' + currency
            column_amount = 'AC'
            column_rate = 'AD'
            column_result = 'AE'

        index_amount = last_index(agent_day_sheet, column_amount)
        agent_day_sheet.update(index_amount, amount, value_input_option='USER_ENTERED')

        if standard_rate:

            index_rate = last_index(agent_day_sheet, column_rate)
            agent_day_sheet.update(index_rate, standard_rate, value_input_option='USER_ENTERED')

            result_amount = string_number_to_python(amount)

        else:

            index_rate = last_index(agent_day_sheet, column_rate)
            agent_day_sheet.update(index_rate, rate, value_input_option='USER_ENTERED')
            result_rate = string_number_to_python(rate)
            result_amount = string_number_to_python(amount_for_other_result)

        result = result_amount * result_rate
        result_string = decimal_number_to_string(result)

        index_result = last_index(agent_day_sheet, column_result)
        agent_day_sheet.update(index_result, result_string, value_input_option='USER_ENTERED')

        return True

    except APIError:
        return False
    except WorksheetNotFound:
        return False


def eur_to_usd_save_sheet(agent: str,
                          day: str,
                          amount: str,) -> bool:
    """
        :param agent: Name of agent for search the worksheet title
        :param day: Current date DD.MM.YYYY for search the worksheet title
        :param amount: Amount of EUR to exchange for USD
        :return: True: If data successfully added to the worksheet;
        False: If worksheet with the title 'agent day' don't exist
    """

    try:
        agent_day = agent + ' ' + day
        agent_day_sheet = spreadsheet.worksheet(title=agent_day)

        column_amount = 'AF'
        column_rate = 'AG'
        column_result = 'AH'

        eur_rate = func_rate("EUR_RATE")
        usd_rate = func_rate("USD_RATE")

        result_rate = string_number_to_python(eur_rate) / string_number_to_python(usd_rate)
        result_amount = string_number_to_python(amount)
        result = result_amount * result_rate
        result_string = decimal_number_to_string(result)
        rate_string = decimal_number_to_string(result_rate)

        index_amount = last_index(agent_day_sheet, column_amount)
        agent_day_sheet.update(index_amount, amount, value_input_option='USER_ENTERED')

        index_result = last_index(agent_day_sheet, column_result)
        agent_day_sheet.update(index_result, result_string, value_input_option='USER_ENTERED')

        index_rate = last_index(agent_day_sheet, column_rate)
        agent_day_sheet.update(index_rate, rate_string, value_input_option='USER_ENTERED')
        return True

    except APIError:
        return False
    except WorksheetNotFound:
        return False


def usd_to_eur_save_sheet(agent: str,
                          day: str,
                          amount: str, ) -> bool:
    """
        :param agent: Name of agent for search the worksheet title
        :param day: Current date DD.MM.YYYY for search the worksheet title
        :param amount: Amount of USD to exchange for EUR
        :return: True: If data successfully added to the worksheet;
        False: If worksheet with the title 'agent day' don't exist
    """

    try:
        agent_day = agent + ' ' + day
        agent_day_sheet = spreadsheet.worksheet(title=agent_day)

        column_amount = 'AI'
        column_rate = 'AJ'
        column_result = 'AK'

        eur_rate = func_rate("EUR_RATE")
        usd_rate = func_rate("USD_RATE")

        result_rate = string_number_to_python(usd_rate) / string_number_to_python(eur_rate)
        result_amount = string_number_to_python(amount)
        result = result_amount * result_rate
        result_string = decimal_number_to_string(result)
        rate_string = decimal_number_to_string(result_rate)

        index_amount = last_index(agent_day_sheet, column_amount)
        agent_day_sheet.update(index_amount, amount, value_input_option='USER_ENTERED')

        index_result = last_index(agent_day_sheet, column_result)
        agent_day_sheet.update(index_result, result_string, value_input_option='USER_ENTERED')

        index_rate = last_index(agent_day_sheet, column_rate)
        agent_day_sheet.update(index_rate, rate_string, value_input_option='USER_ENTERED')
        return True

    except APIError:
        return False
    except WorksheetNotFound:
        return False


def usdt_for_usd_save_sheet(agent: str,
                            day: str,
                            amount: str, ) -> bool:
    """
        :param agent: Name of agent for search the worksheet title
        :param day: Current date DD.MM.YYYY for search the worksheet title
        :param amount: Amount of USDT to exchange for USD
        :return: True: If data successfully added to the worksheet;
        False: If worksheet with the title 'agent day' don't exist
    """

    try:
        agent_day = agent + ' ' + day
        agent_day_sheet = spreadsheet.worksheet(title=agent_day)

        column_amount = 'AL'
        column_result = 'AN'

        index_amount = last_index(agent_day_sheet, column_amount)
        agent_day_sheet.update(index_amount, amount, value_input_option='USER_ENTERED')

        index_result = last_index(agent_day_sheet, column_result)
        agent_day_sheet.update(index_result, amount, value_input_option='USER_ENTERED')

        return True

    except APIError:
        return False
    except WorksheetNotFound:
        return False


def usdt_for_tl_save_sheet(agent: str,
                           day: str,
                           amount: str, ) -> bool:
    """
        :param agent: Name of agent for search the worksheet title
        :param day: Current date DD.MM.YYYY for search the worksheet title
        :param amount: Amount of USDT to exchange for TL
        :return: True: If data successfully added to the worksheet;
        False: If worksheet with the title 'agent day' don't exist
    """

    try:
        agent_day = agent + ' ' + day
        agent_day_sheet = spreadsheet.worksheet(title=agent_day)

        column_amount = 'AO'
        column_rate = 'AP'
        column_result = 'AQ'

        rate = func_rate("USDT_TL")

        result_rate = string_number_to_python(rate)
        result_amount = string_number_to_python(amount)
        result = result_amount * result_rate
        result_string = decimal_number_to_string(result)
        rate_string = decimal_number_to_string(result_rate)

        index_amount = last_index(agent_day_sheet, column_amount)
        agent_day_sheet.update(index_amount, amount, value_input_option='USER_ENTERED')

        index_result = last_index(agent_day_sheet, column_result)
        agent_day_sheet.update(index_result, result_string, value_input_option='USER_ENTERED')

        index_rate = last_index(agent_day_sheet, column_rate)
        agent_day_sheet.update(index_rate, rate_string, value_input_option='USER_ENTERED')
        return True

    except APIError:
        return False
    except WorksheetNotFound:
        return False


def wu_receive_save_sheet(agent: str,
                          day: str,
                          amount: str,
                          currency: str) -> bool:
    """
        :param agent: Name of agent for search the worksheet title
        :param day: Current date DD.MM.YYYY for search the worksheet title
        :param amount: Amount of money which client receiving from Western Union
        :param currency: In which currency client receiving money from Western Union
        :return: True: If data successfully added to the worksheet;
        False: If worksheet with the title 'agent day' don't exist
    """

    try:
        agent_day = agent + ' ' + day
        agent_day_sheet = spreadsheet.worksheet(title=agent_day)

        if currency == "TL":
            column_amount = 'AR'
        elif currency == "USD":
            column_amount = 'AS'
        elif currency == "EUR":
            column_amount = 'AT'
        elif currency == "RUB":
            column_amount = 'AU'

        index_amount = last_index(agent_day_sheet, column_amount)
        agent_day_sheet.update(index_amount, amount, value_input_option='USER_ENTERED')

        return True

    except APIError:
        return False
    except WorksheetNotFound:
        return False


def wu_sending_save_sheet(agent: str,
                          day: str,
                          amount: str,
                          currency: str) -> bool:
    """
        :param agent: Name of agent for search the worksheet title
        :param day: Current date DD.MM.YYYY for search the worksheet title
        :param amount: Amount of money which client sending via Western Union
        :param currency: In which currency client sending money via Western Union
        :return: True: If data successfully added to the worksheet;
        False: If worksheet with the title 'agent day' don't exist
    """

    try:
        agent_day = agent + ' ' + day
        agent_day_sheet = spreadsheet.worksheet(title=agent_day)

        if currency == "TL":
            column_amount = 'AV'
        elif currency == "USD":
            column_amount = 'AW'
        elif currency == "EUR":
            column_amount = 'AX'
        elif currency == "RUB":
            column_amount = 'AY'

        index_amount = last_index(agent_day_sheet, column_amount)
        agent_day_sheet.update(index_amount, amount, value_input_option='USER_ENTERED')

        return True

    except APIError:
        return False
    except WorksheetNotFound:
        return False


def expenses_save_sheet(agent: str,
                        day: str,
                        amount: str,
                        currency: str,
                        explanation: str) -> bool:
    """
        :param agent: Name of agent for search the worksheet title
        :param day: Current date DD.MM.YYYY for search the worksheet title
        :param amount: Amount of money which will be added to Expenses column
        :param currency: What is the currency of money added to the Expenses column
        :param explanation: Short explanation of the expenses
        :return: True: If data successfully added to the worksheet;
        False: If worksheet with the title 'agent day' don't exist
    """

    try:
        agent_day = agent + ' ' + day
        agent_day_sheet = spreadsheet.worksheet(title=agent_day)

        if currency == "TL":
            column_expenses = 'BD'
        elif currency == "USD":
            column_expenses = 'BE'
        elif currency == "EUR":
            column_expenses = 'BF'
        elif currency == "RUB":
            column_expenses = 'BG'
        else:
            column_expenses = 'BH'
            amount = amount + currency
        column_explanation = "BI"

        column_digital_index = column_letter_to_index(column_explanation)
        row_expenses = str((len(agent_day_sheet.col_values(column_digital_index)) + 1))
        index_expenses = column_expenses + row_expenses

        agent_day_sheet.update(index_expenses, amount, value_input_option='USER_ENTERED')

        index_explanation = last_index(agent_day_sheet, column_explanation)
        agent_day_sheet.update(index_explanation, explanation, value_input_option='USER_ENTERED')

        return True

    except APIError:
        return False
    except WorksheetNotFound:
        return False
