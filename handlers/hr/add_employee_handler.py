# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.types import CallbackQuery

from keyboards.keyboards import back
from system.system import router


@router.callback_query(F.data == "add_employee_handler")
async def add_employee_handler(query: CallbackQuery) -> None:
    """👤 Добавить сотрудника"""

    # Сообщение самому пользователю
    await query.message.answer(
        text="👤 Добавить сотрудника", reply_markup=back()
    )


def register_handlers_add_employee_handler() -> None:
    router.callback_query.register(add_employee_handler)  # 👤 Добавить сотрудника
