from fastapi import status
from fastapi.exceptions import HTTPException

from utils import IUnitOfWork

from users.schemas import UserInfo


class AdminsService:
    async def get_admin_by_user(self, uow: IUnitOfWork, user: UserInfo) -> UserInfo:
        async with uow:
            admin_db = await uow.admins.select_one(user_id=user.id)
        
        if admin_db:
            return user


