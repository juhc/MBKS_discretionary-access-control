from sqlalchemy.ext.asyncio import AsyncSession
from repositories import SQLRepository
from database.models import Files


class FilesRepository(SQLRepository):
    def __init__(self, session: AsyncSession, model=Files) -> None:
        super().__init__(session, model)
