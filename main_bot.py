from aiogram.utils import executor
from aiogram.types import BotCommand

from os import environ

# own imports

from create_bot import dp, bot, SERVER
from handlers import client, admin
from data_base.db_action import sql_start


async def on_startup(dp):

    client.register_handlers_client(dp)
    admin.register_handlers_admin(dp)
    sql_start()

    if SERVER == "HEROKU":
        uri_app = environ.get('URI_APP')
        await bot.set_webhook(uri_app)

    commands = [
        BotCommand(command="/start", description=chr(0x1F44B) + " START")
    ]

    await bot.set_my_commands(commands)


async def on_shutdown(dp):

    if SERVER == "HEROKU":
        await bot.delete_webhook()
    pass


if SERVER == "HEROKU":
    port = environ.get('PORT', default='8443')
    executor.start_webhook(
                           dispatcher=dp,
                           webhook_path='',
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           skip_updates=True,
                           host="0.0.0.0",
                           port=port
                           )
else:
    executor.start_polling(
                           dispatcher=dp,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           skip_updates=True
                           )
