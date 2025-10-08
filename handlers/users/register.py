# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.types import CallbackQuery
from loguru import logger

from database.database import write_database
from keyboards.keyboards import back, confirmation_keyboard
from system.system import TARGET_USER_ID, bot, router


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


def register_handler() -> None:
    router.callback_query.register(callback_register_handler)  # Регистрация
    router.callback_query.register(confirm_user)  # Подтверждение регистрации
