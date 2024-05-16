from pydantic import BaseModel


class DiscretionaryAccessCreate(BaseModel):
    user_id: int
    file_id: int

    class Config:
        from_attributes = True


class Permissions(BaseModel):
    can_read: bool
    can_write: bool
    can_tg: bool

    class Config:
        from_attributes = True


class DiscretionaryAccessInfo(DiscretionaryAccessCreate, Permissions):
    id: int
    file_name: str
    user_name: str

    class Config:
        from_attributes = True


class DiscretionaryAccessUpdateRequest(Permissions):
    user_name: str
    user_id: int
    id: int | None

class DiscretionaryAccessUpdate(Permissions):
    file_id: int
    user_id: int
    id: int | None
