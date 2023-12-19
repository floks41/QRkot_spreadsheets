"""Модуль абстрактны схем для благотворительных проектов и пожертвований."""


from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from typing_extensions import Annotated

PositiveInt = Annotated[int, Field(gt=0)]


class AbstractCreate(BaseModel):
    """Абстрактная схема создания объектов."""
    full_amount: PositiveInt


class AbstractUpdate(AbstractCreate):
    """Абстрактная схема обновления объектов."""
    full_amount: Optional[PositiveInt]


class AbstractDB(AbstractCreate):
    """Абстрактная схема чтения объектов из базы данных."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        """Конфигурация абстрактной схемы чтения объектов из базы данных."""
        orm_mode = True
