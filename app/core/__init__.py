"""Модуль инициализации пакета core проекта CAT_CHARITY_FUND.
Чтение настроек, инициализация работы с базой данных,
настройка системы аутентификации и управления пользователями.
Импорт класса Base и всех моделей для Alembic.
"""


from app.core.db import Base  # noqa
from app.models import CharityProject, Donation, User  # noqa