"""Модуль валидаторов для эндпоинтов api."""


from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверяет существование объекта CharityProject по id.
    Возвращает объект CharityProject, либо вызывает исключение."""
    charity_project = await charity_project_crud.get(session, project_id)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Проект не найдена!'
        )
    return charity_project


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Проверяет существование объекта CharityProject с указанным именем.
    При существовании объекта вызывает исключение."""
    project = await charity_project_crud.get_project_by_name(
        session, project_name
    )
    if project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_new_full_amount(
    new_full_amount: int,
    current_invested_amount: int,
) -> None:
    """Проверяет, что обновленное значение стоимости проекта не ниже суммы
    уже инвестированных в проект пожертвований.
    В противном случае вызывает исключение."""
    if new_full_amount < current_invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя снижать полную стоимость проекта!',
        )


async def check_charity_project_is_closed(project: CharityProject) -> None:
    """Проверяет перед редактированием, что проект не закрыт.
    В противном случае вызывает исключение."""
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )


async def check_charity_project_before_remove(project: CharityProject) -> None:
    """Проверяет перед удалением, что в проект
    не внесены пожертвования или он не закрыт.
    В противном случае вызывает исключение."""
    if project.fully_invested or project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
