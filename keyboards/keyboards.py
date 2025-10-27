# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger

DEPARTMENTS = {
    "prod_apit": "Производство АПИТ",
    "prod_all": "Производство АПИТ все участки",
    "spec_fiesta": "Спец фиеста",
    "bron_zavod": "БРОНЕЗАВОД «АПИТ»",
    "logistics": "Транспортное управление, внутренняя логистика",
    "sales": "Отдел продаж"
}


def role_keyboard():
    """Клавиатура для выбора роли"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="HR", callback_data="role_hr")],
            [InlineKeyboardButton(text="Сотрудник", callback_data="role_employee")],
            [InlineKeyboardButton(text="Админ", callback_data="role_admin")],
        ]
    )


def departments_keyboard():
    """Клавиатура для выбора отдела"""

    # Формируем список списков кнопок: каждая кнопка — в отдельной строке
    inline_keyboard = [
        [InlineKeyboardButton(text=name, callback_data=f"dept_{key}")]
        for key, name in DEPARTMENTS.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def register_keyboard():
    """Клавиатура для регистрации"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Регистрация",
                                  callback_data="registration")],
        ]
    )


def back():
    """Клавиатура для возврата"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Главное меню", callback_data="back")

            ]
        ]
    )


def confirmation_keyboard(user_id: int):
    """Клавиатура для подтверждения регистрации"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подтвердить", callback_data=f"confirm:{user_id}"
                ),
                InlineKeyboardButton(
                    text="Отклонить", callback_data=f"reject:{user_id}"
                )
            ]
        ]
    )


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
