# -*- coding: utf-8 -*-
import asyncio
import logging
import sys

from handlers.employee.anonymous_question_handler import register_handlers_anonymous_question_handler
from handlers.users.greeting import register_greeting_handler
from handlers.users.register import register_handler
from system.system import dp, bot


async def main() -> None:
    # И диспетчеризация событий запуска

    register_greeting_handler()  # Регистрация обработчиков событий
    register_handler()  # Регистрация обработчиков событий

    register_handlers_anonymous_question_handler()  # Регистрация обработчиков событий ❓ Анонимный вопрос

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
