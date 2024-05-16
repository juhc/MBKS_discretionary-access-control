from sqlalchemy.ext.asyncio import AsyncSession
from repositories import SQLRepository
from database.models import Users


class UsersRepository(SQLRepository):
    def __init__(self, session: AsyncSession, model=Users) -> None:
        super().__init__(session, model)
