# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.types import CallbackQuery

from keyboards.keyboards import back
from system.system import router


@router.callback_query(F.data == "publish_advertisement_handler")
async def publish_advertisement_handler(query: CallbackQuery) -> None:
    """✍ Публикация объявления"""

    # Сообщение самому пользователю
    await query.message.answer(
        text="✍ Публикация объявления", reply_markup=back()
    )


def register_handlers_publish_advertisement_handler() -> None:
    router.callback_query.register(publish_advertisement_handler)  # ✍ Публикация объявления
