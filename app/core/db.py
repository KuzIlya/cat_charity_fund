import sqlalchemy.orm as so
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.config import settings


class PreBase:

    @so.declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: so.Mapped[int] = so.mapped_column(primary_key=True)


Base = so.declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = so.sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
