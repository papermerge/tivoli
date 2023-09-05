from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from tivoli.database.base import Base


class User(Base):
    __tablename__ = "core_user"

    id: Mapped[str] = mapped_column(
        String(32),
        primary_key=True,
        index=True
    )
