# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from keyboards.keyboards import back
from states.states import BotContentEditStates
from system.system import ADMIN_USER_ID
from system.system import router
from system.working_with_files import load_bot_info
from system.working_with_files import save_bot_info


@router.callback_query(F.data == "dictionary_handler")
async def dictionary_handler(query: CallbackQuery) -> None:
    """📖 Справочник"""

    # Сообщение самому пользователю
    await query.message.answer(
        text=load_bot_info(
            messages="media/messages/dictionary_handler.json"
        ),
        reply_markup=back(),
        parse_mode="HTML"
    )


# Обработчик команды /edit_dictionary_handler (только для админа)
@router.message(Command("edit_dictionary_handler"))
async def edit_dictionary_handler(message: Message, state: FSMContext):
    """Редактирование: 📖 Справочник"""
    if message.from_user.id not in ADMIN_USER_ID:
        await message.reply("У вас нет прав на выполнение этой команды.")
        return
    await message.answer("Введите новый текст, используя разметку HTML.")
    await state.set_state(BotContentEditStates.edit_dictionary_handler)


@router.message(BotContentEditStates.edit_dictionary_handler)
async def update_dictionary_handler(message: Message, state: FSMContext):
    """Обработчик текстовых сообщений (для админа, чтобы обновить информацию)"""
    save_bot_info(
        message.html_text, file_path='media/messages/dictionary_handler.json'
    )  # Сохраняем информацию в JSON
    await message.reply("Информация обновлена.")
    await state.clear()


def register_handlers_dictionary_handler() -> None:
    router.callback_query.register(dictionary_handler)  # 📖 Справочник
    router.message.register(edit_dictionary_handler)  # Редактирование: 📖 Справочник
