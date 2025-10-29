# -*- coding: utf-8 -*-
import os

import openpyxl
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from loguru import logger
from openpyxl.workbook import Workbook
from peewee import IntegrityError

from database.database import get_user_bot_users, get_users, get_admin_ids, Admin
from system.system import router, bot


@router.message(Command('help'))
async def admin_send_start(message: types.Message, state: FSMContext):
    """Обработчик команды /start, он же пост приветствия 👋"""
    await state.clear()  # Завершаем текущее состояние машины состояний

    # Получаем актуальный список админов из БД
    admin_ids = get_admin_ids()

    if message.from_user.id not in admin_ids:
        await message.reply("У вас нет прав на выполнение этой команды.")
        return

    """Админ панель"""

    await message.answer("Команды админа:\n\n"

                         "<b>Редактирование текста и отправка сообщений:</b>\n\n"

                         "<b>Редактирование текста:</b>\n"
                         "/edit_anonymous_question_handler - ❓ Анонимный вопрос\n"
                         "/edit_dictionary_handler - 📖 Справочник\n"
                         "/edit_faq_handler - 🔍 FAQ\n"
                         "/edit_news_handler - 📢 Новости и акции\n\n"

                         "<b>Получение данных:</b>\n"
                         "/get_a_list_of_users_registered_in_the_bot - Получение списка зарегистрированных "
                         "пользователей\n"
                         "/get_users_who_launched_the_bot - Получение данных пользователей, запускающих бота\n\n"

                         "<b>Добавление:</b>\n"
                         "/add_admin - Добавить пользователя в админы. Укажите ID пользователя: /add_admin ID\n\n"

                         "/start - начальное меню\n", parse_mode="HTML")


# Функция для создания файла Excel с данными заказов
def create_excel_file(users_list):
    """
    Создание Excel файла из списка списков.
    Ожидается, что каждый подсписок содержит 7 элементов в порядке:
    [id_user, user_name, first_name, last_name, status, role, departments]
    """
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Пользователи"

    headers = [
        'ID аккаунта пользователя',
        'Username',
        'Имя',
        'Фамилия',
        'Статус (доступ разрешён)',
        'Роль',
        'Отделы'
    ]
    sheet.append(headers)

    for user in users_list:
        # Убедитесь, что в списке ровно 7 элементов
        if len(user) < 7:
            # Дополняем до 7, если не хватает
            user = list(user) + [""] * (7 - len(user))
        sheet.append([
            user[0] or "",
            user[1] or "",
            user[2] or "",
            user[3] or "",
            user[4] or "",
            user[5] or "",
            user[6] or ""
        ])

    for column_cells in sheet.columns:
        length = max(len(str(cell.value or "")) for cell in column_cells)
        sheet.column_dimensions[column_cells[0].column_letter].width = length + 2

    return workbook


@router.message(Command('get_a_list_of_users_registered_in_the_bot'))
async def export_data(message: types.Message, state: FSMContext):
    """Получение списка зарегистрированных пользователей"""
    await state.clear()
    try:
        # Получаем актуальный список админов из БД
        admin_ids = get_admin_ids()

        if message.from_user.id not in admin_ids:
            await message.reply("У вас нет прав на выполнение этой команды.")
            return

        users = get_users()

        if not users:
            await message.reply("⚠️ В базе нет зарегистрированных пользователей.")
            return

        # Создание файла Excel
        workbook = create_excel_file(users)
        filename = 'Зарегистрированные пользователи в боте.xlsx'
        workbook.save(filename)

        # Отправка файла
        await message.answer_document(
            document=FSInputFile(filename),
            caption=("📋 Данные пользователей, зарегистрированных в боте\n\n"
                     "Для возврата в начальное меню нажми /start или /help")
        )

        # Удаляем файл после отправки
        os.remove(filename)

    except Exception as e:
        logger.exception(f"Ошибка при экспорте пользователей: {e}")
        await message.reply("❌ Произошла ошибка при создании отчета.")


def create_excel_file_start(users):
    """
    Создание Excel файла с данными пользователей, запустивших бота.
    """
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Пользователи"

    # Заголовки столбцов
    headers = [
        'ID аккаунта пользователя',
        'username',
        'Имя',
        'Фамилия',
        'Тип чата',
        'Язык Telegram',
        'Дата запуска бота'
    ]
    sheet.append(headers)

    # Заполнение данными
    for user in users:
        sheet.append(user)

    return workbook


@router.message(Command("get_users_who_launched_the_bot"))
async def get_users_who_launched_the_bot(message: types.Message, state: FSMContext):
    """Получение данных пользователей, запускающих бота"""
    await state.clear()  # Завершаем текущее состояние машины состояний
    try:
        # Получаем актуальный список админов из БД
        admin_ids = get_admin_ids()

        if message.from_user.id not in admin_ids:
            await message.reply("У вас нет прав на выполнение этой команды.")
            return

        workbook = create_excel_file_start(get_user_bot_users())  # Создание файла Excel
        filename = 'Данные пользователей запустивших бота.xlsx'
        workbook.save(filename)  # Сохранение файла
        await bot.send_document(message.from_user.id, document=FSInputFile(filename),
                                caption=("Данные пользователей зарегистрированных в боте\n\n"
                                         "Для возврата в начальное меню нажми на /start или /help"))  # Отправка файла пользователю
        os.remove(filename)  # Удаление файла
    except Exception as e:
        logger.error(e)


@router.message(Command('add_admin'))
async def add_admin(message: types.Message):
    """Добавляет пользователя в список админов"""
    admin_ids = get_admin_ids()

    if message.from_user.id not in admin_ids:
        await message.reply("У вас нет прав на выполнение этой команды.")
        return

    # Пример: /add_admin 123456789
    try:
        user_id = int(message.text.split()[1])
        Admin.create(user_id=user_id)
        await message.reply(f"Пользователь {user_id} добавлен в админы.")
    except (IndexError, ValueError):
        await message.reply("Укажите ID пользователя: /add_admin <ID>")
    except IntegrityError:  # Если ID уже есть в БД
        await message.reply(f"Пользователь {user_id} уже является админом.")


def register_admin_greeting_handler():
    """Регистрируем handlers для бота"""
    router.message.register(admin_send_start)
    router.message.register(export_data)
    router.message.register(get_users_who_launched_the_bot)
    router.message.register(add_admin)
