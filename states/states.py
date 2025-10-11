from aiogram.fsm.state import StatesGroup, State


class BotContentEditStates(StatesGroup):
    """Замена текста в боте"""
    edit_main_menu = State()
    edit_anonymous_question_handler = State()  # Замена текста в разделе "❓ Анонимный вопрос"
    edit_dictionary_handler = State()  # Замена текста в разделе "📖 Справочник"
    edit_faq_handler = State()  # Замена текста в разделе "🔍 FAQ"
    edit_news_handler = State()  # Замена текста в разделе "📢 Новости и акции"

    """Работа с ответами пользователей"""
    waiting_for_anonymous_question = State()  # Ожидание ответа от пользователя
