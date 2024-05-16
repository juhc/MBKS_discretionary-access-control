from fastapi import APIRouter, Depends, HTTPException, status

from .services import FilesService
from .schemas import FileBase, FileCreate, FileInfo, FileUserPermissions
from .dependepcies import (
    can_user_read_file,
    can_user_write_file,
    can_user_take_grant_file,
)

from utils import UOWDep

from discretionary_access.services import DiscretionaryAccessService
from discretionary_access.schemas import (
    DiscretionaryAccessCreate,
    Permissions,
    DiscretionaryAccessInfo,
    DiscretionaryAccessUpdateRequest,
    DiscretionaryAccessUpdate,
)

from auth.dependencies import get_current_auth_user

from users.services import UsersService

router = APIRouter(prefix="/files", tags=["Files"])


@router.get("/")
async def get_files():
    pass


@router.post("/")
async def add_file(
    file_in: FileBase, uow: UOWDep, user=Depends(get_current_auth_user)
) -> FileInfo:
    file = FileCreate(data=file_in.data, owner=user.id, name=file_in.name)
    created_file = await FilesService().create_file(uow, file)
    await DiscretionaryAccessService().create_permission(uow, created_file)
    return created_file


@router.get("/{file_name}")
async def get_file_info(uow: UOWDep, file=Depends(can_user_read_file)) -> FileInfo:
    return file


@router.patch("/{file_name}")
async def update_file_info(
    data: FileBase, uow: UOWDep, file=Depends(can_user_write_file)
):
    updated_file = await FilesService().edit_file(
        uow=uow, data=data.model_dump(), id=file.id
    )
    return updated_file


@router.get("/{file_id}/permissions/me")
async def get_current_user_file_permissions(
    uow: UOWDep, file_id: int, user=Depends(get_current_auth_user)
) -> Permissions:
    file_in = DiscretionaryAccessCreate(file_id=file_id, user_id=user.id)
    permissions = await DiscretionaryAccessService().get_user_file_permissions(
        uow, file_in
    )

    if permissions:
        return permissions

    raise HTTPException(
        status.HTTP_403_FORBIDDEN, "user dose not have permission for this file"
    )


@router.get("/{file_name}/users/permissions/")
async def get_users_file_permissions(
    uow: UOWDep, file=Depends(can_user_take_grant_file)
) -> list[FileUserPermissions]:
    users_permissions = await FilesService().get_users_file_permissions(
        uow=uow, file_in=file
    )
    return users_permissions


@router.patch("/{file_name}/users/permissions/")
async def change_users_file_permissions(
    uow: UOWDep,
    permissions_in: list[DiscretionaryAccessUpdateRequest],
    file=Depends(can_user_take_grant_file),
) -> list[DiscretionaryAccessUpdateRequest]:
    users_permissions = await DiscretionaryAccessService().update_file_permissions(
        uow=uow, file_id=file.id, permissions_in=permissions_in
    )
    return users_permissions


@router.patch("/{permission_id}/permissions/me")
async def change_user_file_permission(
    uow: UOWDep,
    permission_id: int,
    new_permissions: Permissions,
    user=Depends(get_current_auth_user),
) -> DiscretionaryAccessInfo:
    updated_permissions = await DiscretionaryAccessService().update_file_permission(
        uow, permission_id, new_permissions
    )
    return updated_permissions


@router.get("/permissions/me")
async def get_current_user_files_permissions(
    uow: UOWDep, user=Depends(get_current_auth_user)
) -> list[DiscretionaryAccessInfo]:
    files_permissions = await DiscretionaryAccessService().get_user_files_permissions(
        uow, user
    )

    return files_permissions


@router.get("/me")
async def get_user_files(
    uow: UOWDep, user=Depends(get_current_auth_user)
) -> list[FileInfo]:
    files = await UsersService().select_files(uow, id=user.id)

    return files
