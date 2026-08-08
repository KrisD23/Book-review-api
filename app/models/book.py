from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    author: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
    ForeignKey("users.id"),
    nullable=False,
    )