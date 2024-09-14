from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_already_invested,
                                ensure_project_open,
                                check_charity_project_exists,
                                full_amount_lower_then_invested,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.utils.investing import investing

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""

    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(
        charity_project, session
    )
    await investing(new_project, Donation, session)

    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    project = await check_charity_project_exists(
        project_id, session
    )
    await check_charity_project_already_invested(project)
    removed_project = await charity_project_crud.remove(
        session, project
    )

    return removed_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    project = await check_charity_project_exists(
        project_id, session
    )

    await ensure_project_open(project_id, session)

    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)

    if obj_in.full_amount:
        await full_amount_lower_then_invested(
            project_id, obj_in.full_amount, session
        )

    if project.invested_amount >= project.full_amount:
        project.fully_invested = True
        await session.commit()
        await session.refresh(project)

    charity_project = await charity_project_crud.update(
        session, project, obj_in
    )

    return charity_project
