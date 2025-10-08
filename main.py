# -*- coding: utf-8 -*-
import asyncio
import logging
import sys

from handlers.employee.anonymous_question_handler import register_handlers_anonymous_question_handler
from handlers.employee.dictionary_handler import register_handlers_dictionary_handler
from handlers.employee.faq_handler import register_handlers_faq_handler
from handlers.employee.news_handler import register_handlers_news_handler
from handlers.hr.add_employee_handler import register_handlers_add_employee_handler
from handlers.users.greeting import register_greeting_handler
from handlers.users.register import register_handler
from system.system import dp, bot


async def main() -> None:
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

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
