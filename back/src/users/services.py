from utils import IUnitOfWork

from .schemas import UserAuth, UserBase, UserInfo

from files.schemas import FileInfo

from database.models import Users


class UsersService:
    async def create_user(self, uow: IUnitOfWork, user: UserAuth) -> Users:
        user_dict = user.model_dump()
        async with uow:
            created_user = await uow.users.insert_one(user_dict)
            await uow.commit()

        return created_user

    async def select_user(self, uow: IUnitOfWork, user: UserBase) -> UserInfo:
        async with uow:
            user_db = await uow.users.select_one(name=user.name)
            user_info = UserInfo(
                name=user_db.name, hashed_password=user_db.password, id=user_db.id
            )

        return user_info

    async def select_files(self, uow: IUnitOfWork, **filter_by) -> list[UserInfo]:
        async with uow:
            user_db = await uow.users.select_with_related_one(Users.files, **filter_by)
            files = [
                FileInfo(id=file.id, data=file.data, owner=user_db.name)
                for file in user_db.files
            ]

        return files