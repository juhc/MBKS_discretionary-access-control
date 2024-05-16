from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from .base import Base

if TYPE_CHECKING:
    from .files import Files
    from .discretionary_access import DiscretionaryAccesses


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(16), unique=True)
    password: Mapped[str] = mapped_column("hashed_password")

    files: Mapped[list["Files"]] = relationship(back_populates="user_owner")
    permissions: Mapped[list["DiscretionaryAccesses"]] = relationship(back_populates="user")
