"""Модуль схем пожертвований."""


from typing import Optional

from .abstract_charity import AbstractCreate, AbstractDB, AbstractUpdate


class DonationCreate(AbstractCreate):
    """Схема создания пожертвований."""
    comment: Optional[str]

    class Config:
        """Конфигурация схемы создания пожертвований."""
        schema_extra = {
            'example': {
                'full_amount': 100,
                'comment': 'Комментарий к пожертвованию',
            }
        }


class DonationUpdate(AbstractUpdate):
    """Схема обновления пожертвований."""
    pass


class DonationDB(AbstractDB, DonationCreate):
    """Схема чтения из базы данных пожертвований."""
    user_id: int

    class Config(AbstractDB.Config):
        """Конфигурация схемы чтения из базы данных пожертвований."""
        pass
