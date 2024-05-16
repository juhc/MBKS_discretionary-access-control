from asyncio import current_task
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    create_async_engine,
    async_sessionmaker,
)

from config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine = create_async_engine(url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory, scopefunc=current_task
        )
        return session
    

    async def session_dependency(self):
        scoped_session = self.get_scoped_session()
        async with scoped_session() as session:
            yield session
            await session.close()


db_helper = DatabaseHelper(
    url=settings.db.database_url,
    echo=True
)