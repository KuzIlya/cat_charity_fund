from typing import Optional
from datetime import datetime

from pydantic import (
    BaseModel, Extra, Field, NonNegativeInt, PositiveInt, validator
)

from app.constants import MAX_LENGTH_FOR_NAME, MIN_LENGTH_FOR_NAME
from app.exceptions.charity_project import (
    BlankProjectDescription, BlankProjectName
)


class CharityProjectBase(BaseModel):
    """Базовая схема модели проекта"""

    name: str = Field(
        ...,
        min_length=MIN_LENGTH_FOR_NAME,
        max_length=MAX_LENGTH_FOR_NAME
    )
    description: str = Field(
        ...,
        min_length=MIN_LENGTH_FOR_NAME
    )
    full_amount: PositiveInt


class CharityProjectUpdate(BaseModel):
    """Схема модели проекта на обновление"""

    name: Optional[str] = Field(
        None,
        min_length=MIN_LENGTH_FOR_NAME,
        max_length=MAX_LENGTH_FOR_NAME
    )
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt] = Field(None)

    class Config:
        from_attributes = True
        extra = Extra.forbid

    @validator('name')
    def name_cannot_be_empty(cls, name: Optional[str]):
        if name is not None and not name.strip():
            raise BlankProjectName()
        return name

    @validator('description')
    def description_cannot_be_empty(cls, description: Optional[str]):
        if description is not None and not description.strip():
            raise BlankProjectDescription()
        return description


class CharityProjectCreate(CharityProjectBase):
    """Схема модели проекта на создание"""


class CharityProjectDB(CharityProjectBase):
    """Схема модели проекта из бд"""

    id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = Field(None)

    class Config:
        from_attributes = True