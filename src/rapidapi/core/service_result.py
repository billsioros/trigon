from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

from rapidapi.core.error import Error, ErrorEnum

T = TypeVar("T", bound="ServiceResult")
A = TypeVar("A")


class ServiceResult(BaseModel, Generic[A]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    error: Error | None = None
    payload: A | None = None

    def __bool__(self) -> bool:
        return self.error is None

    @classmethod
    def ok(cls: type[T], payload: A | None = None) -> T:
        return cls(payload=payload)

    @classmethod
    def fail(cls: type[T], error_type: ErrorEnum, message: str) -> T:
        return cls(error=Error(error_type=error_type, message=message))

    @classmethod
    def invalid(cls: type[T], message: str) -> T:
        return cls.fail(ErrorEnum.INVALID, message)

    @classmethod
    def conflict(cls: type[T], message: str) -> T:
        return cls.fail(ErrorEnum.CONFLICT, message)

    @classmethod
    def unauthorized(cls: type[T], message: str) -> T:
        return cls.fail(ErrorEnum.UNAUTHORIZED, message)

    @classmethod
    def not_found(cls: type[T], message: str) -> T:
        return cls.fail(ErrorEnum.NOT_FOUND, message)
