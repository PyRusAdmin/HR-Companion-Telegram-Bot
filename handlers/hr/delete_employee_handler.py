# -*- coding: utf-8 -*-
import json

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message
from loguru import logger

from database.database import Users
from keyboards.keyboards import back
from states.states import BotContentEditStates
from system.system import ADMIN_USER_ID, bot
from system.system import router


def load_chat_ids():
    try:
        with open("database/chats.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Не удалось загрузить chats.json: {e}")
        return {}


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

    # Загружаем список чатов
    all_chats = load_chat_ids()
    chat_ids_to_kick = set()
    for chat_list in all_chats.values():
        for chat_id in chat_list:
            chat_ids_to_kick.add(chat_id)

    # Исключаем из всех чатов
    kicked_from = []
    for chat_id in chat_ids_to_kick:
        try:
            await bot.ban_chat_member(chat_id=chat_id, user_id=employee_id)
            # Опционально: разбанить сразу, чтобы не блокировать навсегда
            await bot.unban_chat_member(chat_id=chat_id, user_id=employee_id)
            kicked_from.append(chat_id)
        except Exception as e:
            logger.warning(f"Не удалось исключить {employee_id} из чата {chat_id}: {e}")

    # Проверяем, существует ли пользователь. Удаляем из БД
    try:
        user = Users.get(Users.id_user == employee_id)
        user.delete_instance()
        result_msg = f"✅ Сотрудник с ID {employee_id} удалён из БД."
        if kicked_from:
            result_msg += f"\nИсключён из {len(kicked_from)} групп."
        await message.answer(result_msg)
    except Users.DoesNotExist:
        await message.answer(f"⚠️ Сотрудник с ID {employee_id} не найден в БД.")

    await state.clear()


def register_handlers_delete_employee_handler() -> None:
    router.callback_query.register(delete_employee_handler)  # 🚪 Удалить сотрудника
