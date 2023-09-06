import datetime
import uuid

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.orm import Mapped, declarative_base

BaseModel = declarative_base()


class Model(BaseModel):
    """Base model class."""

    __abstract__ = True


class PkModel(Model):
    """Base model that adds a 'primary key' column named ``id``."""

    __abstract__ = True
    id: Mapped[str] = Column(
        "id",
        String(length=36),
        default=lambda: str(uuid.uuid4()),
        primary_key=True,
    )
    created_at: Mapped[datetime.datetime] = Column(DateTime, default=func.current_timestamp())
    updated_at: Mapped[datetime.datetime] = Column(
        DateTime,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
