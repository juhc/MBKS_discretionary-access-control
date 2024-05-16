from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint

from .base import Base

if TYPE_CHECKING:
    from .users import Users
    from .files import Files


class DiscretionaryAccesses(Base):
    __tablename__ = "discretionary_access"
    __table_args__ = (UniqueConstraint("user_id", "file_id", name="unique_user_file"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    file_id: Mapped[int] = mapped_column(ForeignKey("files.id", ondelete="CASCADE"))
    can_read: Mapped[bool] = mapped_column(nullable=False, default=True)
    can_write: Mapped[bool] = mapped_column(nullable=False, default=True)
    can_tg: Mapped[bool] = mapped_column(nullable=False, default=True)
    
    file: Mapped["Files"] = relationship(back_populates="permissions")
    user: Mapped["Users"] = relationship(back_populates="permissions")