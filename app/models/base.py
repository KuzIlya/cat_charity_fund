from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.sqlite import INTEGER


class DateMixin:
    create_date: Mapped[datetime] = mapped_column(default=datetime.now)
    close_date: Mapped[datetime | None] = mapped_column(default=datetime.now)


class InvestmentMixin:
    full_amount: Mapped[int] = mapped_column(INTEGER)
    invested_amount: Mapped[int] = mapped_column(INTEGER, default=0)
    fully_invested: Mapped[bool] = mapped_column(default=False)