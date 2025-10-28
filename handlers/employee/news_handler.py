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
from system.working_with_files import load_bot_info, save_bot_info


@router.callback_query(F.data == "news_handler")
async def news_handler(query: CallbackQuery) -> None:
    """📢 Новости и акции"""

    # Сообщение самому пользователю
    await query.message.answer(
        text=load_bot_info(messages="media/messages/news_handler.json"),
        reply_markup=back(),
        parse_mode="HTML"
    )


# Обработчик команды /edit_news_handler (только для админа)
@router.message(Command("edit_news_handler"))
async def edit_news_handler(message: Message, state: FSMContext):
    """Редактирование: 📢 Новости и акции"""
    if message.from_user.id not in ADMIN_USER_ID:
        await message.reply("У вас нет прав на выполнение этой команды.")
        return
    await message.answer("Введите новый текст, используя разметку HTML.")
    await state.set_state(BotContentEditStates.edit_news_handler)


@router.message(BotContentEditStates.edit_news_handler)
async def update_faq_handler(message: Message, state: FSMContext):
    """Обработчик текстовых сообщений (для админа, чтобы обновить информацию)"""
    save_bot_info(
        message.html_text, file_path='media/messages/news_handler.json'
    )  # Сохраняем информацию в JSON
    await message.reply("Информация обновлена.")
    await state.clear()


def register_handlers_news_handler() -> None:
    router.callback_query.register(news_handler)  # 📢 Новости и акции
    router.message.register(edit_news_handler)  # Редактирование: 📢 Новости и акции
