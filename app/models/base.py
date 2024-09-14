from datetime import datetime

from sqlalchemy.dialects.sqlite import INTEGER
from sqlalchemy.orm import Mapped, mapped_column


class DateMixin:
    create_date: Mapped[datetime] = mapped_column(default=datetime.now)
    close_date: Mapped[datetime | None] = mapped_column(default=None)


class InvestmentMixin:
    full_amount: Mapped[int] = mapped_column(INTEGER, nullable=False)
    invested_amount: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        default=0
    )
    fully_invested: Mapped[bool] = mapped_column(nullable=False, default=False)