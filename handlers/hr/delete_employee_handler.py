# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from database.database import Users
from keyboards.keyboards import back
from states.states import BotContentEditStates
from system.system import ADMIN_USER_ID
from system.system import router


@router.callback_query(F.data == "delete_employee_handler")
async def delete_employee_handler(query: CallbackQuery, state: FSMContext) -> None:
    """🚪 Удалить сотрудника"""

    if query.from_user.id not in ADMIN_USER_ID:
        await query.reply("У вас нет прав на выполнение этой команды.")
        return

    # Сообщение самому пользователю
    await query.message.answer("Введите ID сотрудника для удаления:", reply_markup=back())
    await state.set_state(BotContentEditStates.waiting_for_employee_id)
    await query.answer()


@router.message(BotContentEditStates.waiting_for_employee_id)
async def process_employee_id(message: Message, state: FSMContext) -> None:
    try:
        employee_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Некорректный ID. Введите целое число.")
        return

    # Проверяем, существует ли пользователь
    try:
        user = Users.get(Users.id_user == employee_id)
        # Удаляем пользователя
        user.delete_instance()
        await message.answer(f"✅ Сотрудник с ID {employee_id} успешно удалён.")
    except Users.DoesNotExist:
        await message.answer(f"⚠️ Сотрудник с ID {employee_id} не найден.")

    await state.clear()


def register_handlers_delete_employee_handler() -> None:
    router.callback_query.register(delete_employee_handler)  # 🚪 Удалить сотрудника
