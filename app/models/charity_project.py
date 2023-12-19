"""Модуль модели благотворительных проектов."""


from sqlalchemy import Column, String, Text

from app.models.abstract_charity_model import AbstractCharityModel


class CharityProject(AbstractCharityModel):
    """Модель благотворительных проектов."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
