# -*- coding: utf-8 -*-
import asyncio
import logging
import sys

from handlers.employee.anonymous_question_handler import register_handlers_anonymous_question_handler
from handlers.employee.dictionary_handler import register_handlers_dictionary_handler
from handlers.employee.faq_handler import register_handlers_faq_handler
from handlers.employee.news_handler import register_handlers_news_handler
from handlers.hr.add_employee_handler import register_handlers_add_employee_handler
from handlers.hr.admin_handlers import register_admin_greeting_handler
from handlers.hr.delete_employee_handler import register_handlers_delete_employee_handler
from handlers.hr.incoming_questions_handler import register_handlers_publish_advertisement_handler
from handlers.hr.publish_advertisement_handler import register_handlers_incoming_questions_handler
from handlers.users.greeting import register_greeting_handler
from handlers.users.register import register_handler
from system.system import dp, bot
from loguru import logger

logger.add("log/log.log", rotation="10 MB", compression="zip")


async def main() -> None:
    try:
        # И диспетчеризация событий запуска

        register_greeting_handler()  # Регистрация обработчиков событий
        register_handler()  # Регистрация обработчиков событий

        # Регистрация обработчиков событий для сотрудников
        register_handlers_anonymous_question_handler()  # Регистрация обработчиков событий ❓ Анонимный вопрос
        register_handlers_dictionary_handler()  # Регистрация обработчиков событий 📖 Справочник
        register_handlers_faq_handler()  # Регистрация обработчиков событий 🔍 FAQ
        register_handlers_news_handler()  # Регистрация обработчиков событий 📢 Новости и акции

        # Регистрация обработчиков событий для HR
        register_handlers_add_employee_handler()  # Регистрация обработчиков событий 👤 Добавить сотрудника
        register_handlers_delete_employee_handler()  # Регистрация обработчиков событий 🚪 Удалить сотрудника
        register_handlers_publish_advertisement_handler()  # Регистрация обработчиков событий ✍ Публикация объявления
        register_handlers_incoming_questions_handler()  # Регистрация обработчиков событий 📥 Входящие вопросы

        # Админ панель
        register_admin_greeting_handler()  # Регистрация обработчиков событий для админки

        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
