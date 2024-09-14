from typing import Optional
from datetime import datetime

from pydantic import (
    BaseModel, Extra, Field, NonNegativeInt, PositiveInt, validator
)


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt] = Field(None)

    class Config:
        from_attributes = True
        extra = Extra.forbid

    @validator('name')
    def name_cannot_be_empty(cls, name: Optional[str]):
        if name is not None and not name.strip():
            raise ValueError('Название проекта не может быть пустым!')
        return name

    @validator('description')
    def description_cannot_be_empty(cls, description: Optional[str]):
        if description is not None and not description.strip():
            raise ValueError('Описание проекта не может быть пустым!')
        return description


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = Field(None)

    class Config:
        from_attributes = True