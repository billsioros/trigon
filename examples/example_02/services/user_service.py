from typing import List

from models.user import User
from repositories.user_repository import UserRepository
from schemas.user import UserCreate
from services import Conflict, NotFound, Ok, ServiceResult, Unauthorized
from trigon.contrib.service import Service


class UserService(Service):
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self._user_repository: UserRepository = user_repository

    def get_all(self) -> ServiceResult[List[User]]:
        return Ok(self._user_repository.get_all())

    def get_by_id(self, id: str) -> ServiceResult[User]:
        try:
            return Ok(self._user_repository.get_by_id(id))
        except UserRepository.NotFoundException as exception:
            return NotFound(exception.message)

    def get_by_username(self, username: str) -> ServiceResult[User]:
        try:
            return Ok(self._user_repository.get_by_username(username))
        except UserRepository.NotFoundException as exception:
            return NotFound(exception.message)

    def get_by_email(self, email: str) -> ServiceResult[User]:
        try:
            return Ok(self._user_repository.get_by_email(email))
        except UserRepository.NotFoundException as exception:
            return NotFound(exception.message)

    def create(self, user_create: UserCreate) -> ServiceResult[User]:
        try:
            user_result = self.get_by_username(user_create.username)
            if not user_result:
                user_result = self.get_by_email(user_create.email)

            if user_result:
                raise UserRepository.ConflictException(id=user_result.payload.id)

            user = User(
                username=user_create.username,
                email=user_create.email,
                first_name=user_create.first_name,
                last_name=user_create.last_name,
            )

            user = self._user_repository.create(user)

            return Ok(user)
        except UserRepository.ConflictException as exception:
            return Conflict(exception.message)

    def delete(self, id: str) -> ServiceResult[None]:
        try:
            return Ok(self._user_repository.delete(id))
        except UserRepository.NotFoundException as exception:
            return NotFound(exception.message)

    def authenticate(self, username: str) -> ServiceResult[User]:
        user_result = self.get_by_username(username)
        if user_result:
            return user_result

        return Unauthorized("Invalid username or password")
