from fastapi import Depends, status, HTTPException

from auth.dependencies import get_current_auth_user

from utils.dependecies import UOWDep

from discretionary_access.services import DiscretionaryAccessService
from discretionary_access.schemas import DiscretionaryAccessCreate

from .services import FilesService
from .schemas import FileInfo


async def can_user_read_file(
    file_name: str, uow: UOWDep, user=Depends(get_current_auth_user)
) -> FileInfo:
    file = await FilesService().get_file(uow=uow, name=file_name)
    file_permissions = await DiscretionaryAccessService().get_user_file_permissions(
        uow=uow, file_in=DiscretionaryAccessCreate(user_id=user.id, file_id=file.id)
    )
    if file_permissions.can_read:
        return file

    raise HTTPException(status.HTTP_403_FORBIDDEN, "NO READ")


async def can_user_write_file(
    file_name: str, uow: UOWDep, user=Depends(get_current_auth_user)
) -> FileInfo:
    file = await FilesService().get_file(uow=uow, name=file_name)
    file_permissions = await DiscretionaryAccessService().get_user_file_permissions(
        uow=uow, file_in=DiscretionaryAccessCreate(user_id=user.id, file_id=file.id)
    )
    if file_permissions.can_write:
        return file

    raise HTTPException(status.HTTP_403_FORBIDDEN, "NO WRITE")


async def can_user_take_grant_file(
    file_name: str, uow: UOWDep, user=Depends(get_current_auth_user)
) -> FileInfo:
    file = await FilesService().get_file(uow=uow, name=file_name)
    file_permissions = await DiscretionaryAccessService().get_user_file_permissions(
        uow=uow, file_in=DiscretionaryAccessCreate(user_id=user.id, file_id=file.id)
    )
    if file_permissions.can_tg:
        return file

    raise HTTPException(status.HTTP_403_FORBIDDEN, "NO TG")
