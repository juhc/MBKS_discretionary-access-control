from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .utils import jwt_decode

from users.schemas import UserBase, UserInfo
from users.services import UsersService

from admins.services import AdminsService

from utils.dependecies import UOWDep


def get_token_payload(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]
) -> dict:
    token = credentials.credentials
    payload = jwt_decode(token)
    return payload


async def get_current_auth_user(
    payload: Annotated[str, Depends(get_token_payload)], uow: UOWDep
) -> UserInfo:
    username: str | None = payload.get("sub")

    user = await UsersService().select_user(uow, UserBase(name=username))

    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


async def check_user_is_admin(
    payload: Annotated[str, Depends(get_token_payload)], uow: UOWDep
) -> bool:
    current_user = await get_current_auth_user(payload, uow)
    admin = await AdminsService().get_admin_by_user(uow, current_user)

    return True if admin else False
