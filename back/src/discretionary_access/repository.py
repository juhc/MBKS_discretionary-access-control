from sqlalchemy.ext.asyncio import AsyncSession
from repositories import SQLRepository
from database.models import DiscretionaryAccesses

class DiscretionaryAccessRepository(SQLRepository):
    def __init__(self, session: AsyncSession, model=DiscretionaryAccesses) -> None:
        super().__init__(session, model)