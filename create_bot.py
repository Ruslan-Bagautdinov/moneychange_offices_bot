from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import environ

SERVER = environ.get('SERVER', default=False)

if SERVER:
    TOKEN = environ.get('TOKEN')
    GOOGLE_SHEET_LINK = environ.get("GOOGLE_SHEET_LINK")
    GOOGLE_SHEET_KEY = environ.get("GOOGLE_SHEET_KEY")

    if SERVER == "HEROKU":
        HEROKU_APP_NAME = environ.get('HEROKU_APP_NAME')
        HEROKU_APP_TOKEN = environ.get('HEROKU_APP_TOKEN')

else:
    from config import *
    TOKEN = TOKEN
    GOOGLE_SHEET_LINK = GOOGLE_SHEET_LINK
    GOOGLE_SHEET_KEY = GOOGLE_SHEET_KEY


storage = MemoryStorage()

bot = Bot(
          token=TOKEN
         )
dp = Dispatcher(bot, storage=storage)
