from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger


def employee_menu_keyboard() -> InlineKeyboardMarkup | None:
    """Клавиатура для меню сотрудника"""
    logger.info("Запущена клавиатура для сотрудника")
    try:
        # Возвращаем разметку кнопки
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Новости и акции",  # Текст кнопки
                    callback_data="news_handler"  # Данные для обработки в обработчике
                )
            ],
            [
                InlineKeyboardButton(
                    text="📖 Справочник",  # Текст кнопки
                    callback_data="dictionary_handler"  # Данные для обработки в обработчике
                )
            ],
            [
                InlineKeyboardButton(
                    text="❓ Анонимный вопрос",  # Текст кнопки
                    callback_data="anonymous_question_handler"  # Данные для обработки в обработчике
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔍 FAQ",  # Текст кнопки
                    callback_data="faq_handler"  # Данные для обработки в обработчике
                )
            ],
        ])
    except Exception as error:
        logger.exception(f"Ошибка: {error}")
        return None
