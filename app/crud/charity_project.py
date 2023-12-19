"""Модуль для класса CRUD операций модели CharityProject."""


from typing import Optional

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.frequently_used_values import FrequentlyUsedValues as word
from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectUpdate)


class CRUDCharityProject(
    CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]
):
    """Класс CRUD операций для модели CharityProject."""

    async def get_project_by_name(
        self,
        session: AsyncSession,
        project_name: str,
    ) -> Optional[int]:
        """Чтение объекта CharityProject по имени (поле name)."""
        db_project = await session.execute(
            select(CharityProject).where(CharityProject.name == project_name)
        )
        db_project = db_project.scalars().first()
        return db_project

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> list[dict[str, str]]:
        """Чтение закрытых проектов в список словарей
        с полем длительности активности проекта в секундах."""
        projects = await session.execute(
            select(
                [
                    CharityProject.name,
                    (
                        extract(word.EPOCH, CharityProject.close_date) -
                        extract(word.EPOCH, CharityProject.create_date)
                    ).label(settings.FUNDRAISING_TIME_FIELD_NAME),
                    CharityProject.description,
                ]
            )
            .where(CharityProject.fully_invested)
            .order_by(settings.FUNDRAISING_TIME_FIELD_NAME)
        )
        projects = projects.all()
        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
