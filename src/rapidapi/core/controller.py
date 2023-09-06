import inspect
from functools import wraps

from fastapi import APIRouter


class Controller:
    def __init__(self) -> None:
        entity = f"{self.__class__.__name__.replace('Controller', '')}s"

        self.router = APIRouter(prefix=f"/{entity.lower()}", tags=[entity.title()])

    def as_view(self):
        for name, method in inspect.getmembers(self, inspect.ismethod):
            if hasattr(method, "_http_get"):
                setattr(self, name, self.router.get("/")(method))

        return self.router


def get(prefix: str):
    def _(method):
        method._http_get = True
        method._prefix = prefix

        @wraps(method)
        def __(*args, **kwargs):
            return method(*args, **kwargs)

        return __

    return _
