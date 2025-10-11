# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from keyboards.keyboards import back
from states.states import BotContentEditStates
from system.system import router, ADMIN_USER_ID
from system.working_with_files import save_bot_info, load_bot_info, load_questions_map, save_questions_map
import json
import os
from uuid import uuid4
from aiogram.types import ReplyKeyboardRemove
from system.system import bot, GROUP_CHAT_ID  # Убедитесь, что у вас есть GROUP_CHAT_ID


@router.callback_query(F.data == "anonymous_question_handler")
async def anonymous_question_handler(query: CallbackQuery, state: FSMContext) -> None:
    """❓ Анонимный вопрос"""

    # Сообщение самому пользователю
    await query.message.answer(
        text=load_bot_info(messages="media/messages/anonymous_question_handler.json"),
        reply_markup=back()
    )
    await state.set_state(BotContentEditStates.waiting_for_anonymous_question)
    await query.answer()  # закрываем "часики"


@router.message(BotContentEditStates.waiting_for_anonymous_question)
async def receive_anonymous_question(message: Message, state: FSMContext):
    """Получение вопроса от пользователя и отправка в группу"""
    question_text = message.text.strip()
    if not question_text:
        await message.answer("Вопрос не может быть пустым. Попробуйте снова.")
        return

    # Генерируем уникальный ID вопроса
    question_id = f"Q{str(uuid4().hex)[:8].upper()}"

    # Сохраняем связь: вопрос_id → user_id + текст
    questions_map = load_questions_map()
    questions_map[question_id] = {
        "user_id": message.from_user.id,
        "question_text": question_text
    }
    save_questions_map(questions_map)

    # Отправляем в группу
    group_message = await bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text=f"❓ <b>Анонимный вопрос</b> ({question_id}):\n\n{question_text}",
        parse_mode="HTML"
    )

    # Опционально: сохраняем message_id в группе для будущих ссылок
    # (не обязательно, но полезно при масштабировании)

    await message.answer("Ваш вопрос отправлен в группу. Ответ придёт сюда, как только менеджер ответит.")
    await state.clear()


@router.message(F.chat.id == GROUP_CHAT_ID, F.reply_to_message)
async def handle_manager_reply(message: Message):
    """Обработка ответа менеджера в группе на вопрос"""
    reply_msg = message.reply_to_message
    if not reply_msg or not reply_msg.text:
        return

    # Ищем question_id в тексте (например: "❓ Анонимный вопрос (Q123ABCD): ...")
    text = reply_msg.text
    if "Анонимный вопрос (" not in text:
        return

    # Извлекаем ID
    try:
        start = text.find("(") + 1
        end = text.find(")")
        question_id = text[start:end]
    except:
        return

    # Находим пользователя
    questions_map = load_questions_map()
    if question_id not in questions_map:
        return

    user_id = questions_map[question_id]["user_id"]

    # Отправляем ответ пользователю
    try:
        await bot.send_message(
            chat_id=user_id,
            text=f"📬 <b>Ответ на ваш анонимный вопрос:</b>\n\n{message.text}",
            parse_mode="HTML"
        )
        # Опционально: удаляем запись из карты (или оставить для истории)
        # del questions_map[question_id]
        # save_questions_map(questions_map)
    except Exception as e:
        await bot.send_message(GROUP_CHAT_ID, f"Не удалось отправить ответ пользователю: {e}")


# Обработчик команды /edit_anonymous_question_handler (только для админа)
@router.message(Command("edit_anonymous_question_handler"))
async def edit_anonymous_question_handler(message: Message, state: FSMContext):
    """Редактирование: ❓ Анонимный вопрос"""
    if message.from_user.id not in ADMIN_USER_ID:
        await message.reply("У вас нет прав на выполнение этой команды.")
        return
    await message.answer("Введите новый текст, используя разметку HTML.")
    await state.set_state(BotContentEditStates.edit_anonymous_question_handler)


@router.message(BotContentEditStates.edit_anonymous_question_handler)
async def update_anonymous_question_handler(message: Message, state: FSMContext):
    """Обработчик текстовых сообщений (для админа, чтобы обновить информацию)"""
    save_bot_info(
        message.html_text, file_path='media/messages/anonymous_question_handler.json'
    )  # Сохраняем информацию в JSON
    await message.reply("Информация обновлена.")
    await state.clear()


def register_handlers_anonymous_question_handler() -> None:
    router.callback_query.register(anonymous_question_handler)  # ❓ Анонимный вопрос
    router.message.register(edit_anonymous_question_handler)  # Редактирование: ❓ Анонимный вопрос

    router.message.register(handle_manager_reply)
