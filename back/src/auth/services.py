from fastapi import status
from fastapi.exceptions import HTTPException

from users.schemas import UserAuth, UserCreate, UserInfo
from users.services import UsersService

from utils.uow import IUnitOfWork

from .utils import validate_password


class AuthenticationService:
    async def validate_auth_user(self, uow: IUnitOfWork, user: UserAuth):
        user_db = await UsersService().select_user(uow, user)
        if validate_password(user.password, user_db.hashed_password.encode()):
            return user_db

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found"
        )
