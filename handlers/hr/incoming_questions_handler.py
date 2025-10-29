# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message, ContentType

from database.database import get_admin_ids
from keyboards.keyboards import back
from states.states import BotContentEditStates
from system.system import bot, CHANNEL_CHAT_ID
from system.system import router


@router.callback_query(F.data == "publish_advertisement_handler")
async def publish_advertisement_handler(query: CallbackQuery) -> None:
    """✍ Публикация объявления"""

    # Сообщение самому пользователю
    await query.message.answer(
        text=(
            "✍ <b>Публикация объявления</b>\n\n"
            "Чтобы разместить новость или объявление в канале <a href='https://t.me/+yjqd0uZQETc4NGEy'>«Новости»</a>, "
            "воспользуйтесь командой:\n"
            "➡️ <code>/send_news</code>\n\n"
            "🔹 Сначала отправьте текст (поддерживается HTML-разметка).\n"
            "🔹 Затем прикрепите изображение — <b>если оно нужно</b>.\n"
            "🔹 Если изображение не требуется, просто отправьте команду <code>/skip</code>.\n\n"
            "Ваше объявление будет опубликовано от имени бота в канале для всех сотрудников. 📢"
        ),
        reply_markup=back(),
        parse_mode="HTML",
        disable_web_page_preview=True
    )


@router.message(Command("send_news"))
async def start_news_sending(message: Message, state: FSMContext):
    """Начало отправки новости — только для админов"""

    # Получаем актуальный список админов из БД
    admin_ids = get_admin_ids()

    if message.from_user.id not in admin_ids:
        await message.reply("У вас нет прав на выполнение этой команды.")
        return

    await message.answer("📝 Отправьте текст новости (можно с HTML-разметкой).")
    await state.set_state(BotContentEditStates.waiting_for_news_text)


@router.message(BotContentEditStates.waiting_for_news_text)
async def receive_news_text(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, отправьте именно текст (можно с форматированием).")
        return

    await state.update_data(news_text=message.html_text)
    await message.answer(
        "🖼️ Теперь пришлите фото (если нужно). Или нажмите /skip, чтобы опубликовать без фото."
    )
    await state.set_state(BotContentEditStates.waiting_for_news_photo)


@router.message(Command("skip"))
async def skip_photo(message: Message, state: FSMContext):
    """Пропустить фото и опубликовать только текст"""

    admin_ids = get_admin_ids()

    if message.from_user.id not in admin_ids:
        return

    data = await state.get_data()
    news_text = data.get("news_text")
    if not news_text:
        await message.answer("❌ Нет текста для публикации.")
        await state.clear()
        return

    try:
        await bot.send_message(
            chat_id=CHANNEL_CHAT_ID,
            text=news_text,
            parse_mode="HTML"
        )
        await message.answer("✅ Новость опубликована в канале!")
    except Exception as e:
        await message.answer(f"❌ Ошибка публикации: {e}")
    finally:
        await state.clear()


@router.message(BotContentEditStates.waiting_for_news_photo, F.content_type.in_([ContentType.PHOTO]))
async def receive_news_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]  # берем самое большое изображение
    caption = message.caption  # если HR добавил подпись к фото

    data = await state.get_data()
    news_text = data.get("news_text")

    final_caption = caption if caption else news_text

    try:
        await bot.send_photo(
            chat_id=CHANNEL_CHAT_ID,
            photo=photo.file_id,
            caption=final_caption,
            parse_mode="HTML"
        )
        await message.answer("✅ Новость с фото опубликована в канале!")
    except Exception as e:
        await message.answer(f"❌ Ошибка публикации: {e}")
    finally:
        await state.clear()


@router.message(BotContentEditStates.waiting_for_news_photo)
async def not_photo(message: Message):
    """Если пользователь прислал не фото — напомнить"""
    await message.answer("Пожалуйста, пришлите фото или используйте /skip для публикации без фото.")


def register_handlers_publish_advertisement_handler() -> None:
    router.callback_query.register(publish_advertisement_handler)  # ✍ Публикация объявления
    router.message.register(skip_photo)  # пропустить фото и опубликовать только текст
    router.message.register(start_news_sending)  # Начало отправки новости — только для админов
