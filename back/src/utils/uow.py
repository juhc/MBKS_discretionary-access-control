from abc import ABC, abstractmethod
from typing import Type

from database import db_helper
from users import UsersRepository
from files import FilesRepository
from discretionary_access import DiscretionaryAccessRepository
from admins import AdminsRepository


class IUnitOfWork(ABC):
    users: Type[UsersRepository]
    files: Type[FilesRepository]
    discretionary_access: Type[DiscretionaryAccessRepository]
    admins: Type[AdminsRepository]

    @abstractmethod
    async def __aenter__():
        pass

    @abstractmethod
    async def __aexit__():
        pass

    @abstractmethod
    async def commit():
        pass

    @abstractmethod
    async def rollback():
        pass


class UnitOfWork(IUnitOfWork):
    def __init__(self) -> None:
        self.session_factory = db_helper.session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.files = FilesRepository(self.session)
        self.discretionary_access = DiscretionaryAccessRepository(self.session)
        self.admins = AdminsRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
