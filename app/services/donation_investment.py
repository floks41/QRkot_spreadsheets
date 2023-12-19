"""Модуль donation_investment пакета services
проекта CAT_CHARITY_FUND на фреймворке FastAPI."""


from datetime import datetime
from typing import Union

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


async def check_to_close_charity(
    charity: Union[CharityProject, Donation]
) -> Union[CharityProject, Donation]:
    """Проверяет сумму инвестированную в проект или из пожертвования,
    при необходимости закрывает проект/пожертвование."""
    if charity.full_amount == charity.invested_amount:
        charity.fully_invested = True
        charity.close_date = datetime.utcnow()
    return charity


async def invest(
    project: CharityProject,
    donation: Donation,
    session: AsyncSession = Depends(get_async_session),
):
    """Осуществляет распределение максимально возможной суммы
    от конкертного пожертвования на конкретный проект."""
    availible_amount = donation.full_amount - donation.invested_amount
    required_amount = project.full_amount - project.invested_amount

    amount_for_investing = (
        availible_amount
        if availible_amount <= required_amount
        else required_amount
    )

    project.invested_amount += amount_for_investing
    donation.invested_amount += amount_for_investing

    project = await check_to_close_charity(project)
    donation = await check_to_close_charity(donation)

    session.add(donation)
    session.add(project)
    await session.commit()


async def run_investing(session: AsyncSession = Depends(get_async_session)):
    """Запуск процесса распределения пожертвований по проектам."""
    # Получаем списки актуальных проектов и пожертвований
    donations = await donation_crud.get_open_charity(session)
    projects = await charity_project_crud.get_open_charity(session)

    # Если есть проекты и пожертвования ...
    if donations and projects:
        # ... перебираем проекты
        for project in projects:
            await session.refresh(project)
            # Для каждого проекта, если он еще не закрыт ...
            if not project.fully_invested:
                # ... перебираем пожертвования
                for donation in donations:
                    await session.refresh(donation)
                    # Для каждого пожертвования, ....
                    if not donation.fully_invested:
                        # если оно еще не закрыто,
                        # распределяем пожартвование по текущему проекту
                        await invest(project, donation, session)
                        await session.refresh(donation)
                        await session.refresh(project)
                    # Если проект "закрылся", остановить перебор
                    # пожертвований, перейти к следующему проекту.
                    if project.fully_invested:
                        break
