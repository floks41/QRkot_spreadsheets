"""Модуль эндпоинтов для пожертвований."""


from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.donation_investment import run_investing

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Чтение списка пожертвований. Только для суперпользователя."""
    get_all_donations = await donation_crud.get_multi(session)
    return get_all_donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={
        'invested_amount',
        'fully_invested',
        'close_date',
        'user_id',
    },
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Создание пожертвования."""
    new_donation = await donation_crud.create(session, donation, user)
    await run_investing(session)
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    response_model_exclude={
        'invested_amount',
        'fully_invested',
        'close_date',
        'user_id',
    },
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Чтение списка пожертвований пользователя."""
    user_donations = await donation_crud.get_by_user(user, session)
    return user_donations
