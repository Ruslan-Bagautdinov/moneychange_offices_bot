from decimal import Decimal, ROUND_HALF_UP, InvalidOperation


def number_processing(input_number: str, bank_round=True, zero=False) -> str:

    """ Function for checking inputted data. Takes a string, tries to convert it into Decimal,
    rounds the decimal number according a bank rules, and converts it back into string with
    comma separator, for further writing into Google or Excel Sheets.
    If key 'bank_round=True' - rounds the decimal number according a bank rules.
    If key 'zero=True' - allows to input 0.
    If failed, will raise the InvalidOperation"""

    input_number = input_number.replace(',', '.')
    input_number = Decimal(input_number)
    if input_number < 0:
        raise InvalidOperation
    if not zero and input_number == 0:
        raise InvalidOperation
    if bank_round:
        input_number = input_number.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    comma_number = str(input_number).replace('.', ',')
    comma_number = comma_number.strip("'")
    return comma_number


def string_number_to_python(input_number: [str, float], bank_round=True) -> Decimal:

    """ Function takes a string, tries to convert it into Decimal number.
    If key 'bank_round=True' - rounds the decimal number according a bank rules.
    If failed, will raise the InvalidOperation"""

    if type(input_number) == str:
        input_number = input_number.replace(',', '.')
    result_number = Decimal(input_number)
    if bank_round:
        result_number = result_number.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    return result_number


def decimal_number_to_string(input_number: Decimal, bank_round=True) -> str:

    """ Function takes a Decimal number, converts into string with replacing
    dot by comma and returns string.
    If key 'bank_round=True' - rounds the decimal number according a bank rules.
    If failed, will raise the InvalidOperation"""

    if bank_round:
        input_number = input_number.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    result_string = str(input_number).replace('.', ',')
    return result_string


def b_r(number: [str, float, Decimal]) -> str:

    """
    Beautiful_Result -
    function for converting inputted number into string with
    spaces as a thousand's separators and rounded according bank rules.
    :param number: str | float | Decimal
    :return: str
    """

    if type(number) == str:
        number = string_number_to_python(number, bank_round=False)

    number = '{:,.2f}'.format(number).replace(",", " ").replace(".", ",")

    return number
