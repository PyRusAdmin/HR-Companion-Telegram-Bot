import asyncio
import logging
import sys

from handlers.users.greeting import register_greeting_handler
from handlers.users.register import register_handler
from system.system import dp, bot


async def main() -> None:
    # И диспетчеризация событий запуска

    await dp.start_polling(bot)

    register_handler()  # Регистрация обработчиков событий
    register_greeting_handler()  # Регистрация обработчиков событий


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
