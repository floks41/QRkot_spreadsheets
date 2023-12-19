"""Модуль для класса CRUD операций модели Donation."""


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.schemas.donation import DonationCreate, DonationUpdate


class CRUDDonation(CRUDBase[Donation, DonationCreate, DonationUpdate]):
    """Класс CRUD операций для модели Donation."""

    async def get_by_user(
        self,
        user: User,
        session: AsyncSession,
    ) -> list[Donation]:
        """Чтение списка объектов Donation,
        связанных с объектом модели пользователя (User)."""
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id,
            )
        )
        donations = donations.scalars().all()
        return donations


donation_crud = CRUDDonation(Donation)
