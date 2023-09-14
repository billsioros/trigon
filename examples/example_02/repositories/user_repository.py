from typing import Any, List

from models.user import User
from sqlalchemy import exc
from trigon.contrib.plugins.database import Database
from trigon.contrib.repository import Repository


class UserRepository(Repository):
    class NotFoundException(Repository.NotFoundException):
        def __init__(self, **kwargs: dict[str, Any]) -> None:
            super().__init__(User, **kwargs)

    class ConflictException(Repository.ConflictException):
        def __init__(self, **kwargs: dict[str, Any]) -> None:
            super().__init__(User, **kwargs)

    def __init__(self, database: Database) -> None:
        self.session_factory = database.session_factory

    def get_all(self) -> List[User]:
        with self.session_factory() as session:
            return session.query(User).all()

    def get_by_id(self, id: str) -> User:
        with self.session_factory() as session:
            user = session.query(User).filter(User.id == id).one_or_none()
            if not user:
                raise UserRepository.NotFoundException(id=id)

            return user

    def get_by_username(self, username: str) -> User:
        with self.session_factory() as session:
            user = session.query(User).filter_by(username=username).one_or_none()
            if not user:
                raise UserRepository.NotFoundException(username=username)

            return user

    def get_by_email(self, email: str) -> User:
        with self.session_factory() as session:
            user = session.query(User).filter_by(email=email).one_or_none()
            if not user:
                raise UserRepository.NotFoundException(email=email)

            return user

    def create(
        self,
        user: User,
    ) -> User:
        try:
            with self.session_factory() as session:
                session.add(user)
                session.commit()
                session.refresh(user)

                return user
        except exc.IntegrityError as exception:
            raise UserRepository.ConflictException(username=user.username) from exception

    def delete(self, id: str) -> None:
        with self.session_factory() as session:
            user = self.get_by_id(id)

            session.delete(user)
            session.commit()
