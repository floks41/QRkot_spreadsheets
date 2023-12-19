"""Модуль модели пожертвований."""


from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.abstract_charity_model import AbstractCharityModel


class Donation(AbstractCharityModel):
    """Модель пожертвований."""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
