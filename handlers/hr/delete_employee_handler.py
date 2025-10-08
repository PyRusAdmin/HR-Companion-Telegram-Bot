# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.types import CallbackQuery

from keyboards.keyboards import back
from system.system import router


@router.callback_query(F.data == "delete_employee_handler")
async def delete_employee_handler(query: CallbackQuery) -> None:
    """🚪 Удалить сотрудника"""

    # Сообщение самому пользователю
    await query.message.answer(
        text="🚪 Удалить сотрудника", reply_markup=back()
    )


def register_handlers_delete_employee_handler() -> None:
    router.callback_query.register(delete_employee_handler)  # 🚪 Удалить сотрудника
