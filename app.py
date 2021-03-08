import config
import logging
import handlers.handlers
from data.config import ADMIN_ID
from aiogram import Bot, Dispatcher, executor, types
from loader import bot, dp


async def on_shutdown(dp):
    await bot.close()


async def on_startup(dp):
    await bot.send_message(ADMIN_ID, "Я запущен!")


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)
