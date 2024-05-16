from utils import IUnitOfWork

from .schemas import (
    DiscretionaryAccessCreate,
    Permissions,
    DiscretionaryAccessInfo,
    DiscretionaryAccessUpdate,
    DiscretionaryAccessUpdateRequest,
)

from files.schemas import FileInfo

from users.schemas import UserInfo

from database.models import DiscretionaryAccesses, Files


class DiscretionaryAccessService:
    async def create_permission(
        self, uow: IUnitOfWork, file_in: FileInfo, **permissions
    ):
        file_dict = DiscretionaryAccessCreate(
            user_id=file_in.owner, file_id=file_in.id, **permissions
        ).model_dump()
        async with uow:
            created_permision = await uow.discretionary_access.insert_one(file_dict)
            await uow.commit()

        return created_permision

    async def get_user_file_permissions(
        self, uow: IUnitOfWork, file_in: DiscretionaryAccessCreate
    ) -> Permissions:
        async with uow:
            permissions_db = await uow.discretionary_access.select_one(
                user_id=file_in.user_id, file_id=file_in.file_id
            )
            permissions = Permissions.model_validate(permissions_db)

        return permissions

    async def get_user_files_permissions(
        self, uow: IUnitOfWork, user: UserInfo
    ) -> list[DiscretionaryAccessInfo]:
        async with uow:
            files_permissions_db = (
                await uow.discretionary_access.select_with_related_all(
                    DiscretionaryAccesses.file,
                    DiscretionaryAccesses.user,
                    user_id=user.id,
                )
            )

            files_permissions = []
            for permission in files_permissions_db:
                dam_info = DiscretionaryAccessInfo(
                    can_read=permission.can_read,
                    can_write=permission.can_write,
                    can_tg=permission.can_tg,
                    user_id=permission.user_id,
                    file_id=permission.file_id,
                    file_name=permission.file.name,
                    user_name=permission.file.user_owner.name,
                    id=permission.id,
                )

                files_permissions.append(dam_info.model_dump())

        return files_permissions

    async def update_file_permission(
        self, uow: IUnitOfWork, permission_id: int, permissions_in: Permissions
    ) -> DiscretionaryAccessInfo:
        permissions = permissions_in.model_dump()
        async with uow:
            updated_file_perimssion_db = await uow.discretionary_access.update_one(
                permission_id, permissions
            )
            updated_file_perimssion = DiscretionaryAccessInfo.model_validate(
                updated_file_perimssion_db
            )
            await uow.commit()

        return updated_file_perimssion

    async def update_file_permissions(
        self,
        uow: IUnitOfWork,
        file_id: int,
        permissions_in: list[DiscretionaryAccessUpdateRequest],
    ) -> list[DiscretionaryAccessUpdateRequest]:
        permissions = [
            DiscretionaryAccessUpdate(
                file_id=file_id, **permission_in.model_dump()
            ).model_dump()
            for permission_in in permissions_in
        ]
        
        for permission in permissions:
            if permission["id"] is None:
                permission.pop("id", None)

        async with uow:
            await uow.discretionary_access.update_all(
                data=permissions
            )
            await uow.commit()

        return permissions_in
