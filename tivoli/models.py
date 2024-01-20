import uuid
from uuid import UUID

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from tivoli.database.base import Base


class User(Base):
    __tablename__ = "core_user"

    id: Mapped[UUID] = mapped_column(
        index=True,
        primary_key=True,
        insert_default=uuid.uuid4()
    )