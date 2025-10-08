# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.types import CallbackQuery

from keyboards.keyboards import back
from system.system import router


@router.callback_query(F.data == "news_handler")
async def news_handler(query: CallbackQuery) -> None:
    """📢 Новости и акции"""

    # Сообщение самому пользователю
    await query.message.answer(
        text="📢 Новости и акции", reply_markup=back()
    )


def register_handlers_news_handler() -> None:
    router.callback_query.register(news_handler)  # 📢 Новости и акции
