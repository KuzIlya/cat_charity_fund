from typing import Optional

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models.base import DateMixin, InvestmentMixin


class Donation(InvestmentMixin, DateMixin, Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    comment: Mapped[Optional[str]] = mapped_column(Text)
