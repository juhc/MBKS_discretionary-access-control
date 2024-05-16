from fastapi import APIRouter, Depends

from files.schemas import FileInfo

from users.services import UsersService
from users.schemas import UserInfo

from utils.dependecies import UOWDep

from auth.dependencies import get_current_auth_user

from files.dependepcies import can_user_take_grant_file


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def get_current_user_info(user=Depends(get_current_auth_user)) -> UserInfo:
    return user

@router.get("/file/{file_name}/permissions")
async def get_users_file_permissions(uow: UOWDep, file=Depends(can_user_take_grant_file)):
    await UsersService().get_users_file_permissions(uow=uow, file_in=file)