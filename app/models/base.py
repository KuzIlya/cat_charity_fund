from datetime import datetime
from typing import Optional

from sqlalchemy.dialects.sqlite import INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from app.constants import DEFAULT_INVESTED_AMOUNT


class DateMixin:
    create_date: Mapped[datetime] = mapped_column(default=datetime.now)
    close_date: Mapped[Optional[datetime]] = mapped_column(default=None)


class InvestmentMixin:
    full_amount: Mapped[int] = mapped_column(INTEGER, nullable=False)
    invested_amount: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        default=DEFAULT_INVESTED_AMOUNT
    )
    fully_invested: Mapped[bool] = mapped_column(nullable=False, default=False)
