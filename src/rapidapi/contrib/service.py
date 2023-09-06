from enum import IntEnum, auto
from typing import Generic, TypeVar

from pydantic import BaseModel


class ErrorEnum(IntEnum):
    INVALID = auto()
    CONFLICT = auto()
    UNAUTHORIZED = auto()
    NOT_FOUND = auto()
    INTERNAL = auto()


class Error(BaseModel):
    error_type: ErrorEnum
    message: str


T = TypeVar("T", bound="ServiceResult")
A = TypeVar("A")


class ServiceResult(Generic[A]):
    error: Error | None = None
    payload: A | None = None

    def __init__(self, error: Error | None = None, payload: A | None = None) -> None:
        super().__init__()

        self.error = error
        self.payload = payload

    def __bool__(self) -> bool:
        return self.error is None


class Ok(ServiceResult[A]):
    def __init__(self, payload: A | None = None) -> None:
        super().__init__(payload=payload)


class Fail(ServiceResult[A]):
    def __init__(self, error_type: ErrorEnum, message: str) -> None:
        super().__init__(error=Error(error_type=error_type, message=message))


class Invalid(ServiceResult[A]):
    def __init__(self, message: str) -> None:
        super().__init__(error=Error(error_type=ErrorEnum.INVALID, message=message))


class Conflict(ServiceResult[A]):
    def __init__(self, message: str) -> None:
        super().__init__(error=Error(error_type=ErrorEnum.CONFLICT, message=message))


class Unauthorized(ServiceResult[A]):
    def __init__(self, message: str) -> None:
        super().__init__(error=Error(error_type=ErrorEnum.UNAUTHORIZED, message=message))


class NotFound(ServiceResult[A]):
    def __init__(self, message: str) -> None:
        super().__init__(error=Error(error_type=ErrorEnum.NOT_FOUND, message=message))
