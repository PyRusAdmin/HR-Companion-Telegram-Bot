from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from aiogram.types import Message
from loguru import logger

from database.database import save_bot_user, is_user_exists, is_user_status
from keyboards.keyboards import employee_menu_keyboard, register_keyboard, hr_menu_keyboard
from system.system import router, bot, dp


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Отвечает на команду /start"""
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} начал работу с ботом")
    await save_bot_user(message)  # Записываем пользователя, который запустил бота.
    # user = is_user_exists(id_user=message.from_user.id)

    if is_user_exists(id_user=message.from_user.id):
        logger.info("Пользователь найден ✅")

        status = is_user_status(id_user=message.from_user.id)
        if status == "False":
            await bot.send_message(
                text="Дождитесь одобрения регистрации администратором",
                chat_id=message.chat.id,
                # reply_markup=register_keyboard()
            )
        else:
            if message.from_user.id == 5429188565:
                await  bot.send_message(
                    text="Добро пожаловать, администратор!",
                    chat_id=message.chat.id,
                    reply_markup=hr_menu_keyboard()
                )
            else:
                await bot.send_message(
                    text="Приветствуем в боте!",
                    chat_id=message.chat.id,
                    reply_markup=employee_menu_keyboard()
                )
    else:
        logger.info("Пользователь отсутствует ❌")
        await bot.send_message(
            text="Для работы с ботом, нужно пройти небольшую регистрацию",
            chat_id=message.chat.id,
            reply_markup=register_keyboard()
        )


@router.callback_query(F.data == "back")
async def callback_back_handler(query: CallbackQuery) -> None:
    """Выводит главное меню бота"""
    if query.from_user.id == 5429188565:
        await query.message.answer(text="Добро пожаловать, администратор!", reply_markup=hr_menu_keyboard())
    else:
        await query.message.answer(text="Приветствуем в боте!", reply_markup=employee_menu_keyboard())


def register_greeting_handler() -> None:
    router.message.register(command_start_handler)
    router.callback_query.register(callback_back_handler)  # Отправка главного меню
