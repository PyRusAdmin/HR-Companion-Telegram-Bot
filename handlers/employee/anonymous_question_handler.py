# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from keyboards.keyboards import back
from states.states import BotContentEditStates
from system.system import router, ADMIN_USER_ID
from system.working_with_files import save_bot_info, load_bot_info


@router.callback_query(F.data == "anonymous_question_handler")
async def anonymous_question_handler(query: CallbackQuery) -> None:
    """❓ Анонимный вопрос"""

    # Сообщение самому пользователю
    await query.message.answer(
        text=load_bot_info(messages="media/messages/anonymous_question_handler.json"),
        reply_markup=back()
    )


# Обработчик команды /edit_anonymous_question_handler (только для админа)
@router.message(Command("edit_anonymous_question_handler"))
async def prompt_for_new_payment_info(message: Message, state: FSMContext):
    """Редактирование: ❓ Анонимный вопрос"""
    if message.from_user.id not in ADMIN_USER_ID:
        await message.reply("У вас нет прав на выполнение этой команды.")
        return
    await message.answer("Введите новый текст, используя разметку HTML.")
    await state.set_state(BotContentEditStates.edit_anonymous_question_handler)


@router.message(BotContentEditStates.edit_anonymous_question_handler)
async def update_payment_info(message: Message, state: FSMContext):
    """Обработчик текстовых сообщений (для админа, чтобы обновить информацию)"""
    save_bot_info(
        message.html_text, file_path='media/messages/anonymous_question_handler.json'
    )  # Сохраняем информацию в JSON
    await message.reply("Информация обновлена.")
    await state.clear()


def register_handlers_anonymous_question_handler() -> None:
    router.callback_query.register(anonymous_question_handler)  # ❓ Анонимный вопрос
    router.message.register(prompt_for_new_payment_info)  # Редактирование: ❓ Анонимный вопрос
