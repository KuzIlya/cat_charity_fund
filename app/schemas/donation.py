from datetime import datetime

from pydantic import BaseModel, NonNegativeInt, PositiveInt, Field


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: str | None = Field(None)


class DonationCreate(DonationBase):
    pass


class DonationResponse(DonationBase):
    id: int
    create_date: datetime

    class Config:
        from_attributes = True


class DonationDB(DonationResponse):
    user_id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    close_date: datetime | None = Field(None)
