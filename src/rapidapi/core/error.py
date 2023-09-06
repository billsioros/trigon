from enum import IntEnum, auto

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
