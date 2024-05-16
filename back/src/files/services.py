from utils import IUnitOfWork

from .schemas import FileCreate, FileInfo, FileBase, FilePermissionsInfo

from database.models import Files, Users, DiscretionaryAccesses

from sqlalchemy import select

from .schemas import FileUserPermissions


class FilesService:
    async def create_file(self, uow: IUnitOfWork, file_in: FileCreate) -> FileInfo:
        file_dict = file_in.model_dump()
        async with uow:
            created_file = await uow.files.insert_one(file_dict)
            await uow.commit()

        return created_file

    async def delete_file(self, uow: IUnitOfWork, file: Files):
        async with uow:
            await uow.files.delete_one(file)

    async def get_files(self, uow: IUnitOfWork, **filter_by) -> list[FileInfo]:
        async with uow:
            files = await uow.files.select_with_related(
                Files.users, Files.permissions, **filter_by
            )
            files = [
                FileInfo(
                    data=file.data,
                    id=file.id,
                    owner=file.user_owner.name,
                    name=file.name,
                )
                for file in files
            ]

        return files

    async def edit_file(self, uow: IUnitOfWork, data: dict, **filter_by) -> FileInfo:
        async with uow:
            file_db = await uow.files.update_one(data=data, **filter_by)
            await uow.commit()
            file = FileInfo.model_validate(file_db)

        return file

    async def get_file(self, uow: IUnitOfWork, **filter_by) -> FileInfo:
        async with uow:
            file_db = await uow.files.select_one(**filter_by)
            file = FileInfo.model_validate(file_db)

        return file

    async def get_users_file_permissions(
        self, uow: IUnitOfWork, file_in: FileInfo
    ) -> list[FileUserPermissions]:
        async with uow:
            query = (
                select(
                    Users.name,
                    Users.id,
                    DiscretionaryAccesses.id,
                    DiscretionaryAccesses.can_read,
                    DiscretionaryAccesses.can_tg,
                    DiscretionaryAccesses.can_write,
                )
                .join(DiscretionaryAccesses, (DiscretionaryAccesses.file_id == file_in.id) & (DiscretionaryAccesses.user_id == Users.id), isouter=True)
    
            )
            users_permissions = await uow.users.session.execute(query)

            result: list[FileUserPermissions] = []
            for perm in users_permissions:
                result.append(
                    FileUserPermissions(
                        **dict(
                            zip(
                                [
                                    "user_name",
                                    "user_id",
                                    "permission_id",
                                    "can_read",
                                    "can_tg",
                                    "can_write",
                                ],
                                perm,
                            )
                        )
                    )
                )

        for item in result:
            if item.permission_id is None:
                item.can_read = False
                item.can_write = False
                item.can_tg = False

        return result
