"""Модуль абстрактной модели для благотворительных проектов
и пожертвований."""


from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class AbstractCharityModel(Base):
    """Абстрактная модель для благотворительных проектов
    и пожертвований."""
    full_amount = Column(Integer, nullable=False)  # Больше нуля
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    close_date = Column(DateTime)
    __abstract__ = True
