from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models.base import DateMixin, InvestmentMixin
from app.constants import MAX_LENGTH_FOR_NAME


class CharityProject(InvestmentMixin, DateMixin, Base):
    name: Mapped[str] = mapped_column(
        String(MAX_LENGTH_FOR_NAME),
        unique=True,
        nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self):
        return (
            f'Благотворительный проект {self.name}: {self.description}'
        )
