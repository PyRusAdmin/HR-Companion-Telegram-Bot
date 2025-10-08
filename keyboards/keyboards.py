from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger


def employee_menu_keyboard():
    """Клавиатура для меню сотрудника"""
    logger.info("Запущена клавиатура для сотрудника")

    try:
        # Создание разметки кнопок
        rows = [
            [
                InlineKeyboardButton(
                    text="📢 Новости и акции",  # Текст кнопки
                    callback_data="news_handler"  # URL-ссылка на канал
                )
            ],
        ]

        # Создание клавиатуры с одной кнопкой
        link_to_channel = InlineKeyboardMarkup(inline_keyboard=rows)

        # Возвращаем разметку кнопки
        return link_to_channel
    except Exception as e:
        # Логируем ошибку, если она возникла
        logger.exception(f"Ошибка: {e}")
