from models._model import PkModel
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import Mapped


class User(PkModel):
    """A user of the app."""

    __tablename__ = "users"
    username: Mapped[str] = Column(String(80), unique=True, nullable=False)
    email: Mapped[str] = Column(String(80), unique=True, nullable=False)
    first_name: Mapped[str] = Column(String(30), nullable=False)
    last_name: Mapped[str] = Column(String(30), nullable=False)
    active: Mapped[bool] = Column(Boolean(), default=False)

    @property
    def full_name(self):
        """Full user name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"
