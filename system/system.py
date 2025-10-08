import os

from aiogram import Dispatcher
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из .env

# Bot token can be obtained via https://t.me/BotFather
BOT_TOKEN = os.environ.get("BOT_TOKEN")

dp = Dispatcher()
