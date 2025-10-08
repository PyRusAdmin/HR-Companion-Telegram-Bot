# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.types import CallbackQuery

from keyboards.keyboards import back
from system.system import router


@router.callback_query(F.data == "anonymous_question_handler")
async def anonymous_question_handler(query: CallbackQuery) -> None:
    """❓ Анонимный вопрос"""

    # Сообщение самому пользователю
    await query.message.answer(
        text="❓ Анонимный вопрос", reply_markup=back()
    )


def register_handlers_anonymous_question_handler() -> None:
    router.callback_query.register(anonymous_question_handler)  # ❓ Анонимный вопрос
