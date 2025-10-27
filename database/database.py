# -*- coding: utf-8 -*-
from loguru import logger
from peewee import SqliteDatabase, Model, IntegerField, TextField, CharField, IntegrityError

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
    role = CharField()  # Роль пользователя (HR, Сотрудник, Администратор)
    departments = CharField()  # Отделы предприятия

    class Meta:
        database = db
        table_name = "users"


def get_users():
    """Получаем всех пользователей, зарегистрированных в базе данных."""
    datas = []
    for data in Users.select():
        datas.append([
            data.id_user,
            data.user_name or "",
            data.last_name or "",
            data.first_name or "",
            data.status or "",
        ])
    return datas


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


def get_user_bot_users():
    """
    Получаем всех пользователей, запустивших бота.
    Возвращаем список списков (для удобства записи в Excel).
    """
    datas = []
    for data in BotUsers.select():
        datas.append([
            data.user_id,
            data.username or "",
            data.first_name or "",
            data.last_name or "",
            data.chat_type or "",
            data.language_code or "",
            data.date_start or ""
        ])
    return datas


# Создаём таблицу при загрузке модуля
db.connect()
db.create_tables([Users, BotUsers], safe=True)
db.close()

async def save_bot_employeers(message):
    """Сохраняет или обновляет данные пользователя в базе при запуске /start"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    try:
        # Пытаемся создать новую запись
        Users.create(
            id_user=user_id,
            user_name=username,
            first_name=first_name,
            last_name=last_name,
            status="False",  # По умолчанию не подтверждён
            role="Сотрудник",  # Можно оставить заглушку — HR позже назначит
            departments=""     # Пусто до назначения
        )
        logger.info(f"Новый пользователь добавлен в БД: {user_id}")

    except IntegrityError:
        # Пользователь уже существует — можно обновить имя/username, если нужно
        user = Users.get(Users.id_user == user_id)
        updated = False
        if user.user_name != username:
            user.user_name = username
            updated = True
        if user.first_name != first_name:
            user.first_name = first_name
            updated = True
        if user.last_name != last_name:
            user.last_name = last_name
            updated = True
        if updated:
            user.save()
            logger.info(f"Данные пользователя {user_id} обновлены")

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
