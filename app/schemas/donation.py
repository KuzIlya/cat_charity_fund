from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt


class DonationBase(BaseModel):
    """Базовая схема модели пожертвования"""

    full_amount: PositiveInt
    comment: Optional[str] = Field(None)


class DonationCreate(DonationBase):
    """Схема модели пожертвования на создание"""


class DonationRead(DonationBase):
    """Схема модели пожертвования на чтение"""

    id: int
    create_date: datetime

    class Config:
        from_attributes = True


class DonationDB(DonationRead):
    """Схема модели пожертвования из бд"""

    user_id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    close_date: Optional[datetime] = Field(None)
