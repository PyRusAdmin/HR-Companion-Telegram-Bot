# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.types import CallbackQuery

from keyboards.keyboards import back
from system.system import router


@router.callback_query(F.data == "faq_handler")
async def faq_handler(query: CallbackQuery) -> None:
    """🔍 FAQ"""

    # Сообщение самому пользователю
    await query.message.answer(
        text="🔍 FAQ", reply_markup=back()
    )


def register_handlers_faq_handler() -> None:
    router.callback_query.register(faq_handler)  # 🔍 FAQ
