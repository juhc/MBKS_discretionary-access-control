from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .base import Base

if TYPE_CHECKING:
    from .users import Users
    from .discretionary_access import DiscretionaryAccesses


class Files(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[str]
    owner: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    user_owner: Mapped["Users"] = relationship(back_populates="files", lazy='subquery')
    users: Mapped[list["Users"]] = relationship(
        back_populates="files", secondary="discretionary_access"
    )

    permissions: Mapped[list["DiscretionaryAccesses"]] = relationship(back_populates="file")
