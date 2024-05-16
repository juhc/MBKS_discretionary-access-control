from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, Result, update, text
from sqlalchemy.orm import selectinload, joinedload

from pydantic import BaseModel

from database.models import Base


class AbstractRepository(ABC):
    @abstractmethod
    async def insert_one():
        pass

    @abstractmethod
    async def select_one():
        pass

    @abstractmethod
    async def delete_one():
        pass

    @abstractmethod
    async def select_all():
        pass


class SQLRepository(AbstractRepository):
    def __init__(self, session: AsyncSession, model=None) -> None:
        self.session = session
        self.__model = model

    async def insert_one(self, data: dict):
        query = insert(self.__model).values(**data).returning(self.__model)
        result: Result = await self.session.execute(query)
        return result.scalar_one()

    async def select_one(self, **filter_by):
        query = select(self.__model).filter_by(**filter_by)
        result: Result = await self.session.execute(query)
        return result.scalar_one()

    async def select_all(self, **filter_by):
        query = select(self.__model).filter_by(**filter_by)
        result: Result = await self.session.execute(query)
        return result.scalars().all()

    async def select_with_related_all(self, *args, **filter_by):
        loads = []
        for arg in args:
            loads.append(selectinload(arg))
        query = select(self.__model).filter_by(**filter_by).options(*loads)
        result: Result = await self.session.execute(query)
        return result.scalars().all()

    async def select_joined_all(self, *args, filter_by):
        loads = []
        for arg in args:
            loads.append(joinedload(arg))

        filters = filter_by.get("filters", [])
        query = select(self.__model).options(*loads).filter(*filters)
        result: Result = await self.session.execute(query)
        return result.unique().scalars().all()

    async def select_with_related_one(self, *args, **filter_by):
        query = select(self.__model).filter_by(**filter_by).options(selectinload(*args))
        result: Result = await self.session.execute(query)
        return result.scalar_one()

    async def delete_one(self, obj: Base) -> None:
        await self.session.delete(obj)

    async def update_one(self, data: dict, **filter_by):
        query = (
            update(self.__model)
            .values(**data)
            .filter_by(**filter_by)
            .returning(self.__model)
        )
        result: Result = await self.session.execute(query)
        return result.scalar_one()

    async def update_all(self, data: list[dict], **filter_by):
        new_data = [self.__model(**item) for item in data]

        for item in new_data:
            result = await self.session.merge(item)
