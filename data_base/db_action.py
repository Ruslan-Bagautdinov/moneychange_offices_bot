import sqlite3
from number_funcs import string_number_to_python, decimal_number_to_string


def sql_start():
    global base, cursor
    base = sqlite3.connect('agents_and_rates.db')
    cursor = base.cursor()
    if base:
        print('Data_base connection: OK')
    cursor.execute("CREATE TABLE IF NOT EXISTS agents (agent TEXT PRIMARY KEY, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS rates (rate TEXT PRIMARY KEY, value REAL)")
    base.commit()


def read_password(agent):
    cursor.execute("SELECT password FROM agents WHERE agent = ?", (agent,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None


def change_password(agent, new_password):

    cursor.execute("UPDATE agents SET password = ? WHERE agent = ?", (new_password, agent))
    base.commit()


def read_rate(rate):
    cursor.execute("SELECT value FROM rates WHERE rate = ?", (rate,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None


def change_rate(rate, new_value):

    new_value = string_number_to_python(new_value, bank_round=False)
    new_value = decimal_number_to_string(new_value, bank_round=False)

    cursor.execute("UPDATE rates SET value = ? WHERE rate = ?", (new_value, rate))
    base.commit()
