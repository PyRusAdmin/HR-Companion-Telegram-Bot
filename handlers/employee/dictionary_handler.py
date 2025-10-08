# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.types import CallbackQuery

from keyboards.keyboards import back
from system.system import router


@router.callback_query(F.data == "dictionary_handler")
async def dictionary_handler(query: CallbackQuery) -> None:
    """📖 Справочник"""

    # Сообщение самому пользователю
    await query.message.answer(
        text="📖 Справочник", reply_markup=back()
    )


def register_handlers_dictionary_handler() -> None:
    router.callback_query.register(dictionary_handler)  # 📖 Справочник
