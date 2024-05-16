from pydantic import BaseModel

from discretionary_access.schemas import Permissions


class FileBase(BaseModel):
    data: str | None
    name: str


class FileCreate(FileBase):
    owner: int


class FileInfo(FileBase):
    id: int 
    owner: int | str

    class Config:
        from_attributes = True

class FilePermissionsInfo(FileBase, Permissions):
    pass

class FileUserPermissions(BaseModel):
    user_name: str
    user_id: int
    permission_id: int | None
    can_read: bool | None
    can_tg: bool | None
    can_write: bool | None