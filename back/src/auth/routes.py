from typing import Annotated

from fastapi import APIRouter, Depends

from users.schemas import UserAuth, UserCreate
from users.services import UsersService
from utils.dependecies import UOWDep

from .utils import jwt_encode, hash_password
from .services import AuthenticationService
from .schemas import AuthInfo, TokenInfo


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/sign-up")
async def register_user(user_in: UserAuth, uow: UOWDep):
    user_in = UserCreate(
        name=user_in.name, hashed_password=hash_password(user_in.password)
    )
    user = await UsersService().create_user(uow, user_in)

    return user


@router.post("/sign-in")
async def login_user(user: UserAuth, uow: UOWDep) -> AuthInfo:
    user = await AuthenticationService().validate_auth_user(uow, user)
    if user:
        jwt_payload = {
            "sub": user.name,
        }
        token = jwt_encode(jwt_payload)
        return AuthInfo(
            access_token=token, token_type="Bearer", username=user.name, user_id=user.id
        )
