from enum import IntEnum, auto
from typing import TypeVar

from trigon.contrib.service import ServiceError as BaseServiceError
from trigon.contrib.service import ServiceResult

A = TypeVar("A")


class ErrorEnum(IntEnum):
    INVALID = auto()
    CONFLICT = auto()
    UNAUTHORIZED = auto()
    NOT_FOUND = auto()
    INTERNAL = auto()


class ServiceError(BaseServiceError):
    error_type: ErrorEnum


class Ok(ServiceResult[A]):
    def __init__(self, payload: A | None = None) -> None:
        super().__init__(payload=payload)


class Fail(ServiceResult[A]):
    def __init__(self, error_type: ErrorEnum, message: str) -> None:
        super().__init__(payload=ServiceError(error_type=error_type, message=message))


class Invalid(ServiceResult[A]):
    def __init__(self, message: str) -> None:
        super().__init__(payload=ServiceError(error_type=ErrorEnum.INVALID, message=message))


class Conflict(ServiceResult[A]):
    def __init__(self, message: str) -> None:
        super().__init__(payload=ServiceError(error_type=ErrorEnum.CONFLICT, message=message))


class Unauthorized(ServiceResult[A]):
    def __init__(self, message: str) -> None:
        super().__init__(payload=ServiceError(error_type=ErrorEnum.UNAUTHORIZED, message=message))


class NotFound(ServiceResult[A]):
    def __init__(self, message: str) -> None:
        super().__init__(payload=ServiceError(error_type=ErrorEnum.NOT_FOUND, message=message))
