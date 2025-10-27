# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from database.database import Users
from keyboards.keyboards import back, role_keyboard, departments_keyboard, DEPARTMENTS
from states.states import BotContentEditStates
from system.system import router
from loguru import logger


@router.callback_query(F.data == "add_employee_handler")
async def add_employee_handler(query: CallbackQuery, state: FSMContext) -> None:
    """👤 Добавить сотрудника — обработка ID и выбор роли/отдела"""

    logger.info(f"Сотрудник перешел в режим редактирования сотрудника ")
    # Сообщение самому пользователю
    await query.message.answer(
        text="👤 Добавить сотрудника\n\n Напишите ID (Telegram) сотрудника, для присвоения отдела и роли",
        reply_markup=back()
    )
    await state.set_state(BotContentEditStates.add_employee)


@router.message(BotContentEditStates.add_employee)
async def add_employee(message: Message, state: FSMContext) -> None:
    """👤 Добавить сотрудника — обработка ID и выбор роли/отдела"""
    # Проверяем, что введено число
    if not message.text.isdigit():
        await message.answer("❌ Пожалуйста, введите корректный ID (число).")
        return

    target_id = int(message.text)

    # Ищем пользователя в базе
    try:
        user = Users.get(Users.id_user == target_id)
    except Users.DoesNotExist:
        await message.answer(f"❌ Пользователь с ID {target_id} не найден в базе.")
        await state.clear()  # Сбрасываем состояние
        return

    # Сохраняем ID пользователя в состоянии
    await state.update_data(target_user_id=target_id)

    # Отправляем клавиатуру выбора роли
    await message.answer(
        text=f"✅ Найден пользователь: {user.first_name} {user.last_name}\n\nВыберите роль:",
        reply_markup=role_keyboard()
    )
    await state.set_state(BotContentEditStates.select_role)


@router.callback_query(F.data.startswith("role_"), BotContentEditStates.select_role)
async def select_role_handler(query: CallbackQuery, state: FSMContext):
    """Обработка выбора роли"""
    role_map = {
        "role_hr": "HR",
        "role_employee": "Сотрудник",
        "role_admin": "Админ"
    }
    role_key = query.data
    role = role_map.get(role_key)

    if not role:
        await query.answer("Неизвестная роль", show_alert=True)
        return

    await state.update_data(selected_role=role)

    # Отправляем клавиатуру выбора отдела
    await query.message.edit_text(
        text=f"Вы выбрали роль: {role}\n\nТеперь выберите отдел:",
        reply_markup=departments_keyboard()
    )
    await state.set_state(BotContentEditStates.select_department)


@router.callback_query(F.data.startswith("dept_"), BotContentEditStates.select_department)
async def select_department_handler(query: CallbackQuery, state: FSMContext):
    dept_key = query.data.replace("dept_", "", 1).strip()
    department = DEPARTMENTS.get(dept_key)

    if not department:
        await query.answer("Неизвестный отдел", show_alert=True)
        return

    data = await state.get_data()
    target_id = data.get("target_user_id")
    role = data.get("selected_role")

    try:
        user = Users.get(Users.id_user == target_id)
        user.role = role
        user.departments = department
        user.save()

        await query.message.edit_text(
            text=f"✅ Роль и отдел успешно назначены!\n\n"
                 f"Пользователь: {user.first_name} {user.last_name}\n"
                 f"Роль: {role}\n"
                 f"Отдел: {department}"
        )
    except Exception as e:
        logger.error(f"Ошибка при обновлении пользователя {target_id}: {e}")
        await query.message.edit_text("❌ Произошла ошибка при сохранении данных.")

    await state.clear()


def register_handlers_add_employee_handler() -> None:
    router.callback_query.register(add_employee_handler, F.data == "add_employee_handler")
    router.message.register(add_employee, BotContentEditStates.add_employee)
    router.callback_query.register(select_role_handler, F.data.startswith("role_"), BotContentEditStates.select_role)
    router.callback_query.register(select_department_handler, F.data.startswith("dept_"),
                                   BotContentEditStates.select_department)
