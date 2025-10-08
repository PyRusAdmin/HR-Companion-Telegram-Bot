from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger


def employee_menu_keyboard() -> InlineKeyboardMarkup | None:
    """Клавиатура для Меню сотрудника"""
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



def hr_menu_keyboard() -> InlineKeyboardMarkup | None:
    """Клавиатура для Меню HR"""
    logger.info("Запущена клавиатура для сотрудника")
    try:
        # Возвращаем разметку кнопки
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👤 Добавить сотрудника",  # Текст кнопки
                    callback_data="add_employee_handler"  # Данные для обработки в обработчике
                )
            ],
            [
                InlineKeyboardButton(
                    text="🚪 Удалить сотрудника",  # Текст кнопки
                    callback_data="delete_employee_handler"  # Данные для обработки в обработчике
                )
            ],
            [
                InlineKeyboardButton(
                    text="✍ Публикация объявления",  # Текст кнопки
                    callback_data="publish_advertisement_handler"  # Данные для обработки в обработчике
                )
            ],
            [
                InlineKeyboardButton(
                    text="📥 Входящие вопросы",  # Текст кнопки
                    callback_data="incoming_questions_handler"  # Данные для обработки в обработчике
                )
            ],
        ])
    except Exception as error:
        logger.exception(f"Ошибка: {error}")
        return None