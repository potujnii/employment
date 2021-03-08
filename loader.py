from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from data.config import TOKEN
from database.db import SQLighter
import logging
from loguru import logger


# bot logging
logsDirect = "logs/requestlogs.log"
logging = logging.basicConfig(level=logging.INFO)
logger.add(logsDirect, format="{time}", enqueue=True, rotation="00:00", compression="zip", level="INFO", catch=True)


# Set up storage
storage = MemoryStorage()

# bot
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)

# database
db = SQLighter('database/main.db')