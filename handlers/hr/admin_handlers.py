import os

import openpyxl
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from loguru import logger

from system.system import router, bot, ADMIN_USER_ID


@router.message(Command('help'))
async def admin_send_start(message: types.Message, state: FSMContext):
    """Обработчик команды /start, он же пост приветствия 👋"""
    await state.clear()  # Завершаем текущее состояние машины состояний
    """Админ панель"""
    if message.from_user.id not in ADMIN_USER_ID:
        await message.reply("У вас нет прав на выполнение этой команды.")
        return
    await message.answer("Команды админа:\n\n"

                         "<b>Редактирование текста и отправка сообщений:</b>\n\n"

                         "<b>Редактирование текста:</b>\n"
                         "/edit_anonymous_question_handler - ❓ Анонимный вопрос\n"
                         "/edit_dictionary_handler - 📖 Справочник\n"
                         "/edit_faq_handler - 🔍 FAQ\n"
                         "/edit_news_handler - 📢 Новости и акции\n"

                         "<b>Получение данных:</b>\n"
                         "/get_a_list_of_users_registered_in_the_bot - Получение списка зарегистрированных "
                         "пользователей\n"
                         "/get_users_who_launched_the_bot - Получение данных пользователей, запускающих бота\n\n"

                         "/start - начальное меню\n", parse_mode="HTML")


# Функция для создания файла Excel с данными заказов
def create_excel_file(orders):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    # Заголовки столбцов
    sheet['A1'] = 'ID аккаунта пользователя'
    sheet['B1'] = 'Имя'
    sheet['C1'] = 'Фамилия'
    sheet['D1'] = 'Город'
    sheet['E1'] = 'Номер телефона'
    sheet['F1'] = 'Дата регистрации'
    # Заполнение данными заказов
    for index, order in enumerate(orders, start=2):
        sheet.cell(row=index, column=1).value = order[0]  # ID аккаунта пользователя
        sheet.cell(row=index, column=2).value = order[1]  # Имя
        sheet.cell(row=index, column=3).value = order[2]  # Фамилия
        sheet.cell(row=index, column=4).value = order[3]  # Город
        sheet.cell(row=index, column=5).value = order[4]  # Номер телефона
        sheet.cell(row=index, column=6).value = order[5]  # Дата регистрации

    return workbook


@router.message(Command('get_a_list_of_users_registered_in_the_bot'))
async def export_data(message: types.Message, state: FSMContext):
    """Получение списка зарегистрированных пользователей"""
    await state.clear()  # Завершаем текущее состояние машины состояний
    try:
        if message.from_user.id not in [535185511, 301634256]:
            await message.reply('У вас нет доступа к этой команде.')
            return
        # Создание файла Excel
        workbook = create_excel_file(reading_from_database())
        filename = 'Зарегистрированные пользователи в боте.xlsx'
        workbook.save(filename)  # Сохранение файла
        await bot.send_document(message.from_user.id,
                                document=FSInputFile(filename),
                                caption=("Данные пользователей зарегистрированных в боте\n\n"
                                         "Для возврата в начальное меню нажми на /start или /help")
                                )  # Отправка файла пользователю
        os.remove(filename)  # Удаление файла
    except Exception as e:
        logger.error(e)


def create_excel_file_start(orders):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    # Заголовки столбцов
    sheet['A1'] = 'ID аккаунта пользователя'
    sheet['B1'] = 'username'
    sheet['C1'] = 'Имя'
    sheet['D1'] = 'Фамилия'
    sheet['E1'] = 'Дата запуска бота'
    # Заполнение данными заказов
    for index, order in enumerate(orders, start=2):
        sheet.cell(row=index, column=1).value = order[0]  # ID аккаунта пользователя
        sheet.cell(row=index, column=2).value = order[1]  # username
        sheet.cell(row=index, column=3).value = order[2]  # Имя
        sheet.cell(row=index, column=4).value = order[3]  # Фамилия
        sheet.cell(row=index, column=5).value = order[4]  # Дата запуска бота

    return workbook


@router.message(Command("get_users_who_launched_the_bot"))
async def get_users_who_launched_the_bot(message: types.Message, state: FSMContext):
    """Получение данных пользователей, запускающих бота"""
    await state.clear()  # Завершаем текущее состояние машины состояний
    try:
        if message.from_user.id not in [535185511, 301634256]:
            await message.reply('У вас нет доступа к этой команде.')
            return
        workbook = create_excel_file_start(reading_from_database())  # Создание файла Excel
        filename = 'Данные пользователей запустивших бота.xlsx'
        workbook.save(filename)  # Сохранение файла
        await bot.send_document(message.from_user.id, document=FSInputFile(filename),
                                caption=("Данные пользователей зарегистрированных в боте\n\n"
                                         "Для возврата в начальное меню нажми на /start или /help"))  # Отправка файла пользователю
        os.remove(filename)  # Удаление файла
    except Exception as e:
        logger.error(e)


def register_admin_greeting_handler():
    """Регистрируем handlers для бота"""
    router.message.register(admin_send_start)
    router.message.register(export_data)
    router.message.register(get_users_who_launched_the_bot)
