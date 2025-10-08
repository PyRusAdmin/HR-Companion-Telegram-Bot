# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.types import CallbackQuery

from keyboards.keyboards import back
from system.system import router


@router.callback_query(F.data == "incoming_questions_handler")
async def incoming_questions_handler(query: CallbackQuery) -> None:
    """📥 Входящие вопросы"""

    # Сообщение самому пользователю
    await query.message.answer(
        text="📥 Входящие вопросы", reply_markup=back()
    )


def register_handlers_incoming_questions_handler() -> None:
    router.callback_query.register(incoming_questions_handler)  # 📥 Входящие вопросы
