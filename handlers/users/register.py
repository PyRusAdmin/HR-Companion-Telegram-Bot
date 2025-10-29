# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from database.database import write_database, Users
from keyboards.keyboards import back, confirmation_keyboard, role_keyboard, departments_keyboard, DEPARTMENTS, role_map
from states.states import BotContentEditStates
from system.system import TARGET_USER_ID, bot, router
from system.working_with_files import load_department_channels


@router.callback_query(F.data == "registration")
async def callback_register_handler(query: CallbackQuery) -> None:
    """Регистрация пользователя"""
    logger.debug(
        f"ID: {query.from_user.id}, username: {query.from_user.username}, "
        f"last_name: {query.from_user.last_name}, first_name: {query.from_user.first_name}"
    )
    """
    Запись в базу данных (database/people.db), данных пользователя, таких как: id, username, имя, фамилия, статус.
    По умолчанию статус "False", так как нужно подтверждение регистрации от администратора телеграмм бота.
    После подтверждения регистрации статус меняется на "True".
    """
    # если пользователь сам админ → сразу True
    status = "True" if query.from_user.id in TARGET_USER_ID else "False"

    write_database(
        id_user=query.from_user.id,  # id пользователя
        user_name=query.from_user.username,  # username
        last_name=query.from_user.last_name,  # фамилия
        first_name=query.from_user.first_name,  # имя
        status=status  # статус по умолчанию "False"
    )
    # Сообщение самому пользователю
    await query.message.answer(
        text="✅ Регистрация пройдена. Ожидайте подтверждения от администратора.",
    )

    # Сообщение всем админам
    for admin_id in TARGET_USER_ID:
        await bot.send_message(
            chat_id=admin_id,  # здесь точно int, не список!
            text=f"Пользователь @{query.from_user.username or query.from_user.id} "
                 f"отправил данные для подтверждения регистрации.\n",
            reply_markup=confirmation_keyboard(query.from_user.id),
        )


@router.callback_query(F.data.startswith("confirm:"))
async def confirm_user(query: CallbackQuery) -> None:
    """Подтверждение регистрации администратором бота"""
    target_id = int(query.data.split(":")[1])  # достаем id пользователя

    logger.debug(f"Подтверждение регистрации пользователя: {target_id}")

    write_database(
        id_user=target_id,  # меняем только id
        user_name=None,  # меняем только статус
        last_name=None,
        first_name=None,
        status="True"
    )

    await query.message.answer(f"✅ Пользователь {target_id} подтвержден.")
    await bot.send_message(
        chat_id=target_id,
        text="✅ Ваша регистрация подтверждена.",
        reply_markup=back(),
    )


@router.callback_query(F.data.startswith("assign_role:"))
async def assign_role_start(query: CallbackQuery, state: FSMContext):
    target_id = int(query.data.split(":")[1])

    # Сохраняем ID в состоянии
    await state.update_data(target_user_id=target_id)

    await query.message.edit_text(
        text="Выберите роль для пользователя:",
        reply_markup=role_keyboard()
    )
    await state.set_state(BotContentEditStates.select_role_for_new_user)


@router.callback_query(F.data.startswith("role_"), BotContentEditStates.select_role_for_new_user)
async def select_role_for_new_user(query: CallbackQuery, state: FSMContext):
    """Выбор роли для нового пользователя"""

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
    await state.set_state(BotContentEditStates.select_department_for_new_user)


@router.callback_query(F.data.startswith("dept_"), BotContentEditStates.select_department_for_new_user)
async def select_department_for_new_user(query: CallbackQuery, state: FSMContext):
    try:
        dept_key = query.data.replace("dept_", "", 1).strip()
        department = DEPARTMENTS.get(dept_key)

        if not department:
            await query.answer("Неизвестный отдел", show_alert=True)
            return

        data = await state.get_data()
        target_id = data.get("target_user_id")
        role = data.get("selected_role")

        if not target_id or not role:
            await query.message.edit_text("❌ Недостаточно данных для завершения регистрации.")
            await state.clear()
            return

        # Получаем или создаём запись (на случай, если что-то пошло не так при регистрации)
        user, created = Users.get_or_create(
            id_user=target_id,
            defaults={
                "user_name": None,
                "first_name": None,
                "last_name": None,
                "status": "True",
                "role": role,
                "departments": department
            }
        )
        if not created:
            # Обновляем существующую запись
            user.status = "True"
            user.role = role
            user.departments = department
            user.save()

        await query.message.edit_text(
            text=f"✅ Пользователь успешно зарегистрирован!\n"
                 f"ID: {target_id}\nРоль: {role}\nОтдел: {department}"
        )

        DEPARTMENT_CHANNELS = load_department_channels()
        # Отправляем пользователю сообщение с группами
        channels = DEPARTMENT_CHANNELS.get(department, [])
        links_text = "\n".join(f"• {link}" for link in channels)

        await bot.send_message(
            chat_id=target_id,
            text=(
                "✅ Ваша регистрация подтверждена!\n\n"
                "📌 Пожалуйста, подпишитесь на следующие группы:\n"
                f"{links_text}"
            ),
            reply_markup=back()
        )

        await state.clear()
    except Exception as e:
        logger.exception(e)


def register_handler() -> None:
    router.callback_query.register(callback_register_handler)  # Регистрация
    router.callback_query.register(confirm_user)  # Подтверждение регистрации
    router.callback_query.register(assign_role_start)  # Выбор роли
    router.callback_query.register(select_role_for_new_user)  # Выбор отдела
    router.callback_query.register(select_department_for_new_user)  # Выбор отдела
