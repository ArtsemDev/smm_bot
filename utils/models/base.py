from sqlalchemy import INT, Column, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    id = Column(INT, primary_key=True, autoincrement=True)

    engine = create_async_engine("postgresql+asyncpg://smm:password@0.0.0.0:5432/smm")
    _Session = async_sessionmaker(bind=engine)

    @staticmethod
    def create_session(func):
        async def wrapper(*args, **kwargs):
            async with Base._Session() as session:
                return await func(*args, **kwargs, session=session)

        return wrapper

    @create_session
    async def save(self, session: AsyncSession = None):
        session.add(self)
        await session.commit()
        await session.refresh(self)

    @classmethod
    @create_session
    async def get(cls, pk, session: AsyncSession = None):
        return await session.get(cls, pk)

    @classmethod
    @create_session
    async def all(
            cls,
            order_by: str = "id",
            limit: int = None,
            offset: int = None,
            session: AsyncSession = None,
            **kwargs
    ):
        objs = await session.scalars(
            select(cls)
            .filter_by(**kwargs)
            .order_by(order_by)
            .limit(limit)
            .offset(offset)
        )
        return objs.all()

    @create_session
    async def delete(self, session: AsyncSession = None):
        await session.delete(self)
        await session.commit()
