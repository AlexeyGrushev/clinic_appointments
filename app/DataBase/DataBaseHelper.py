from sqlalchemy import (
    delete,
    insert,
    select,
    text,
)

from app.DataBase.Base import async_session


class DataBaseHelper:
    """
    Base class for database manipulations
    """

    model = None

    @classmethod
    async def find_all(cls, **kwargs):
        async with async_session() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.fetchall()

    @classmethod
    async def find_one_or_none(cls, *args, **kwargs):
        async with async_session() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.one_or_none()

    @classmethod
    async def find_max_id(cls, *args, **kwargs):
        async with async_session() as session:
            query = select(cls.model.id).order_by(cls.model.id.desc()).limit(1)
            result = await session.execute(query)
            return result

    @classmethod
    async def insert_values(cls, *args, **kwargs):
        async with async_session() as session:
            query = insert(cls.model).values(**kwargs).returning(cls.model.id)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    @classmethod
    async def get_seq(cls, *args, **kwargs) -> int:
        if cls.model is None:
            raise ValueError("Model is not set for DataBaseHelper subclass.")
        async with async_session() as session:
            seq = cls.model.__table__.name + "_id_seq"
            query = text(f"select last_value from {seq}")
            result = await session.execute(query)
            return result.fetchone()[0]

    @classmethod
    async def delete_values(cls, *args, **kwargs):
        async with async_session() as session:
            query = delete(cls.model).filter_by(**kwargs)
            await session.execute(query)
            await session.commit()
