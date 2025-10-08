# -*- coding: utf-8 -*-
import os

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

TARGET_USER_ID = [5429188565]  # список ID админов

load_dotenv()  # Загружаем переменные окружения из .env

# Bot token can be obtained via https://t.me/BotFather
BOT_TOKEN = os.environ.get("BOT_TOKEN")

dp = Dispatcher()


# Инициализируйте экземпляр бота свойствами бота по умолчанию, которые будут передаваться во все вызовы API
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


# Создаём роутер
router = Router()
# Подключаем роутеры
dp.include_router(router)