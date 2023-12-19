"""Модуль схем благотворительных проектов."""


from typing import Optional

from pydantic import Extra, Field

from .abstract_charity import AbstractCreate, AbstractDB, AbstractUpdate


class CharityProjectCreate(AbstractCreate):
    """Схема создания благотворительного проекта."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)

    class Config:
        """Конфигурация схемы создания благотворительного проекта."""
        schema_extra = {
            'example': {
                'full_amount': 100,
                'name': 'Название самого важного проекта',
                'description': 'Описание самого важного проекта',
            }
        }


class CharityProjectUpdate(AbstractUpdate):
    """Схема обновления благотворительного проекта."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)

    class Config(CharityProjectCreate.Config):
        """Конфигурация схемы обновления благотворительного проекта."""
        extra = Extra.forbid


class CharityProjectDB(AbstractDB, CharityProjectCreate):
    """Схема чтения из базы данных благотворительного проекта."""
    pass

    class Config(AbstractDB.Config):
        """Конфигурация схемы чтения из базы данных
        благотворительного проекта."""
        pass
