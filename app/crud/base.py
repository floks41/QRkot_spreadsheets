"""Модуль для базового класса CRUD операций моделей CAT_CHARITY_FUND."""


from typing import Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый класс CRUD операций."""

    def __init__(self, model: Type[ModelType]):
        """Конструктор базового класса CRUD операций."""
        self.model = model

    async def get(
        self, session: AsyncSession, obj_id: int
    ) -> Optional[ModelType]:
        """Чтение одного объекта модели по id."""
        print(session)
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession,
    ) -> List[ModelType]:
        """Чтение списка объектов модели."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        session: AsyncSession,
        obj_in: CreateSchemaType,
        user: Optional[User] = None,
    ) -> ModelType:
        """Создание объекта модели."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        session: AsyncSession,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
    ) -> ModelType:
        """Обновление объекта модели."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        session: AsyncSession,
        db_obj: ModelType,
    ) -> ModelType:
        """Удаление объекта модели."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_open_charity(self, session: AsyncSession) -> list[ModelType]:
        """Чтение списка объектов моделей CharityProject и Donation
        со значение поля fully_invested равным False, т.е. не закрытых."""
        charities = await session.execute(
            select(self.model).where(
                ~self.model.fully_invested,
            )
        )
        charities = charities.scalars().all()
        return charities
