"""Модуль настройки работы с базой данных."""


from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    """Абстрактный класс для моделей.
    Задается имя таблицы в БД по умолчанию и первичный ключ id.
    """
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        """Именем таблицы будет название модели в нижнем регистре."""
        return cls.__name__.lower()


# В качестве основы для базового класса укажем класс PreBase.
Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """Асинхронный генератор сессий.
    Через асинхронный контекстный менеджер и sessionmaker
    открывается сессия.
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
