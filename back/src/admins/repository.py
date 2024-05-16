from sqlalchemy.ext.asyncio import AsyncSession
from repositories import SQLRepository
from database.models import Admins


class AdminsRepository(SQLRepository):
    def __init__(self, session: AsyncSession, model=Admins) -> None:
        super().__init__(session, model)
