from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserAuth(UserBase):
    password: str

class UserCreate(UserBase):
    hashed_password: str

class UserInfo(UserCreate):
    id: int

    class Config:
        from_attributes = True
