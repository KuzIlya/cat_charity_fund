from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.exceptions.errors_detail import ProjectErrorDetail


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Проверка на наличие проекта с таким названием"""

    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )

    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ProjectErrorDetail.PROJECT_ALREADY_EXISTS,
        )


async def full_amount_lower_then_invested(
        project_id: int,
        amount: int,
        session: AsyncSession
) -> CharityProject:
    """Проверка новой суммы проекта и вложенной суммы"""

    charity_project = await charity_project_crud.get_charity_project_by_id(
        project_id, session
    )

    if charity_project.invested_amount > amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ProjectErrorDetail.PROJECT_AMOUNT_LESS_INVESTING
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверка на существование проекта"""

    project = await charity_project_crud.get_charity_project_by_id(
        project_id, session
    )
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ProjectErrorDetail.PROJECT_NOT_FOUND
        )
    return project


async def check_charity_project_already_invested(
    charity_project: CharityProject
) -> None:
    """Проверка на наличие пожертвований"""

    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ProjectErrorDetail.PROJECT_ALREADY_INVESTED
        )


async def ensure_project_open(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверка проекта на открытость"""

    charity_project = await charity_project_crud.get_charity_project_by_id(
        project_id, session
    )

    if charity_project.close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ProjectErrorDetail.PROJECT_CLOSED
        )

    return charity_project