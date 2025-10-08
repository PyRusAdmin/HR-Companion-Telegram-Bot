# -*- coding: utf-8 -*-
from loguru import logger
from peewee import SqliteDatabase, Model, IntegerField, TextField, CharField

# Подключение к БД
db = SqliteDatabase("database/people.db")


class Users(Model):
    """
    Модель для хранения данных пользователей.
    """
    id_user = IntegerField(unique=True)  # ID пользователя
    user_name = TextField(null=True)  # Username пользователя
    last_name = TextField(null=True)  # Фамилия пользователя
    first_name = TextField(null=True)  # Имя пользователя
    status = CharField(default=False)  # Разрешение для пользователя

    class Meta:
        database = db
        table_name = "users"


class BotUsers(Model):
    """
    Таблица пользователей, которые запускали бота.
    """
    user_id = IntegerField(unique=True)  # ID пользователя
    username = CharField(null=True)  # username
    first_name = CharField(null=True)  # Имя
    last_name = CharField(null=True)  # Фамилия
    chat_type = CharField()  # Тип чата (private, group и т.д.)
    language_code = CharField(null=True)  # Язык Telegram
    date_start = CharField()  # Дата первого запуска

    class Meta:
        database = db
        table_name = "bot_users"


# Создаём таблицу при загрузке модуля
db.connect()
db.create_tables([Users, BotUsers], safe=True)
db.close()


async def save_bot_user(message):
    """
    Сохраняет или обновляет данные о пользователе, который запустил бота.
    """
    from datetime import datetime

    try:
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        chat_type = message.chat.type
        lang = message.from_user.language_code
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        user, created = BotUsers.get_or_create(
            user_id=user_id,
            defaults={
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "chat_type": chat_type,
                "language_code": lang,
                "date_start": date_now,
            },
        )

        if not created:
            # обновляем данные, если пользователь уже есть
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.chat_type = chat_type
            user.language_code = lang
            user.save()

        logger.info(f"✅ Пользователь {user_id} сохранён в БД (new={created})")

    except Exception as e:
        logger.info(f"❌ Ошибка при сохранении пользователя: {e}")


def write_database(id_user, user_name, last_name, first_name, status):
    """Сохраняем или обновляем данные пользователя"""
    try:
        with db:
            user, created = Users.get_or_create(
                id_user=id_user,
                defaults={
                    "user_name": user_name,
                    "last_name": last_name,
                    "first_name": first_name,
                    "status": status
                },
            )
            if not created:  # Если уже был в базе — обновим данные
                user.user_name = user_name
                user.last_name = last_name
                user.first_name = first_name
                user.status = status
                user.save()

        logger.info(
            f"Пользователь {id_user} {'зарегистрирован' if created else 'обновлён'} в базе данных."
        )
    except Exception as e:
        logger.error(f"Ошибка записи в базу: {e}")


def is_user_exists(id_user: int) -> bool:
    """Проверяет зарегистрирован пользователь или нет"""
    user = Users.get_or_none(Users.id_user == id_user)
    return user is not None


def is_user_status(id_user: int) -> bool:
    """Проверяет статус пользователя"""
    user = Users.get_or_none(Users.id_user == id_user)
    return user.status if user else None
