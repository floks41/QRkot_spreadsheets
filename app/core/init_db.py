"""Модуль для создания пользователей при инициализации базы данных."""


import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate

# Превращаем асинхронные генераторы в асинхронные менеджеры контекста.
get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    email: EmailStr, password: str, is_superuser: bool = False
):
    """Создает пользователя с переданным email и паролем.
    Возможно создание суперпользователя при передаче аргумента
    is_superuser=True."""
    try:
        # Получение объекта асинхронной сессии.
        async with get_async_session_context() as session:
            # Получение объекта класса SQLAlchemyUserDatabase.
            async with get_user_db_context(session) as user_db:
                # Получение объекта класса UserManager.
                async with get_user_manager_context(user_db) as user_manager:
                    # Создание пользователя.
                    await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                        )
                    )
    # В случае, если такой пользователь уже есть, ничего не предпринимать.
    except UserAlreadyExists:
        pass


async def create_first_superuser():
    """Проверяет, указаны ли в настройках данные для суперпользователя.
    Если да, то вызывается корутина create_user для создания
    суперпользователя.
    """
    if (
        (settings.first_superuser_email is not None) and
        (settings.first_superuser_password is not None)
    ):
        await create_user(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            is_superuser=True,
        )
