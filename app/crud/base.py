from typing import Generic, TypeVar, Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
            self,
            model: ModelType
    ) -> None:
        self.model = model

    async def get(
            self,
            session: AsyncSession,
            obj_id: int,
    ) -> Optional[ModelType]:
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession,
    ) -> list[ModelType]:
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in: CreateSchemaType,
            session: AsyncSession,
            user: Optional[User] = None
    ) -> ModelType:
        obj_in_data = obj_in.model_dump()
        if user:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            session: AsyncSession,
            db_obj: ModelType,
            obj_in: UpdateSchemaType,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            session: AsyncSession,
            db_obj: ModelType,
    ) -> ModelType:
        await session.delete(db_obj)
        await session.commit()
        return db_obj
