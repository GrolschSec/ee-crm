from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from .base import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
