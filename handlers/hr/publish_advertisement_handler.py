# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.types import CallbackQuery

from keyboards.keyboards import back
from system.system import router


@router.callback_query(F.data == "incoming_questions_handler")
async def incoming_questions_handler(query: CallbackQuery) -> None:
    """📥 Входящие вопросы"""

    # Сообщение самому пользователю
    await query.message.answer(
        text=(
            "📥 <b>Входящие вопросы</b>\n\n"
            "Все анонимные вопросы от сотрудников публикуются в группе:\n"
            "👉 <a href='https://t.me/+5jmCdAeFd50zMmRi'>HR-вопросы</a>\n\n"
            "🔹 Чтобы ответ пришёл автору вопроса, <b>обязательно используйте функцию Telegram «Ответить»</b> (reply) на сообщение с вопросом.\n"
            "🔹 Вопросы анонимны — будьте тактичны и уважительны.\n"
            "🔹 Пожалуйста, не дублируйте ответы и старайтесь давать содержательные, полезные комментарии.\n\n"
            "Спасибо за поддержку команды! 💬"
        ),
        reply_markup=back(),
        parse_mode="HTML",
        disable_web_page_preview=True
    )


def register_handlers_incoming_questions_handler() -> None:
    router.callback_query.register(incoming_questions_handler)  # 📥 Входящие вопросы
