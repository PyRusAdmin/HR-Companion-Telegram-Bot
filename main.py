import asyncio
import logging
import sys

from aiogram import html
from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger

from keyboards.keyboards import employee_menu_keyboard
from system.system import dp, bot


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Отвечает на команду /start
    """

    # Фиксируем пользователей, которые отправили команду /start
    id_user = message.from_user.id  # id пользователя
    username = message.from_user.username  # username пользователя
    first_name = message.from_user.first_name  # имя пользователя
    last_name = message.from_user.last_name  # фамилия пользователя

    logger.info(
        f"Пользователь c id {id_user} username {username} first_name {first_name} last_name {last_name} отправил команду /start")

    # Отправляем приветственное сообщение пользователю
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=employee_menu_keyboard())


async def main() -> None:
    # И диспетчеризация событий запуска
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
