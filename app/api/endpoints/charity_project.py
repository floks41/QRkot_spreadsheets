"""Модуль эндпоинтов для благотворительных проектов."""


from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_before_remove,
    check_charity_project_exists,
    check_charity_project_is_closed,
    check_name_duplicate,
    check_new_full_amount,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.donation_investment import run_investing

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Чтение списка всех проектов."""
    all_charity_projects = await charity_project_crud.get_multi(session)
    return all_charity_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание проекта. Только для суперпользователя."""
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        session, charity_project
    )
    await run_investing(session)
    await session.refresh(new_charity_project)
    return new_charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Редактирование проекта. Только для суперпользователя."""
    charity_project = await check_charity_project_exists(project_id, session)
    await check_charity_project_is_closed(charity_project)
    # Проверка уникальности имени
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    # Проверка не уменьшения суммы проекта
    if obj_in.full_amount is not None:
        await check_new_full_amount(
            obj_in.full_amount, charity_project.invested_amount
        )
    # Замените вызов функции на вызов метода.
    charity_project = await charity_project_crud.update(
        session,
        charity_project,
        obj_in,
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление проекта. Только для суперпользователя."""
    charity_project = await check_charity_project_exists(project_id, session)
    await check_charity_project_before_remove(charity_project)
    charity_project = await charity_project_crud.remove(
        session=session, db_obj=charity_project
    )
    return charity_project
