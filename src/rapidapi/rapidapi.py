"""A batteries-included python web framework."""


from types import ModuleType
from typing import Any, Dict, Optional, Type, Union

from fastapi import APIRouter, FastAPI

from rapidapi.core.controller import Controller
from rapidapi.core.dependency_injection import Container
from rapidapi.core.settings import RapidAPISettings
from rapidapi.helpers.resolution import get_constructor_arguments, get_types
from rapidapi.middlewares import Middleware


class RapidAPI:
    def __init__(self) -> None:
        self.app: FastAPI | None = None

    def configure(
        self,
        title: str = "RapidAPI",
        description: str = "A batteries-included python web framework",
        version: str = "1.0.0",
        contact: Optional[Dict[str, Union[str, Any]]] = None,
        docs_url: str = "/",
    ) -> "RapidAPI":
        self.app = FastAPI(
            title=title,
            description=description,
            version=version,
            contact=contact,
            docs_url=docs_url,
        )

        return self

    def register_config(self, settings: RapidAPISettings) -> "RapidAPI":
        self.app.state.settings = settings

    def register_container(self, container: Container):
        self.app.state.container = container._build()

        return self

    def register_controllers(self, *controllers: list[Type[Controller]]) -> "RapidAPI":
        def _(controller_type: Type[Controller]):
            arguments = get_constructor_arguments(controller_type)

            resolved_arguments = {}
            for arg_name, arg_type in arguments.items():
                try:
                    resolved_arguments[arg_name] = self.app.state.container[arg_type]
                except KeyError as e:
                    msg = f"Missing dependency for argument '{arg_name}' of type '{arg_type}'"
                    raise KeyError(
                        msg,
                    ) from e

            return controller_type(**resolved_arguments)

        api = APIRouter(prefix="/api")

        for controller in map(_, controllers):
            api.include_router(controller.as_view())

        self.app.include_router(api)

        return self

    def discover_controllers(self, module: ModuleType) -> "RapidAPI":
        return self.register_controllers(*get_types(module, Controller))

    def register_middlewares(self, middlewares: list[Middleware]) -> "RapidAPI":
        for middleware in middlewares:
            self.app.add_middleware(middleware)

        return self

    # def register_events(self, handlers: list[EventHandler]) -> "RapidAPI":
    #     for handler in handlers:


    def build(self) -> FastAPI:
        return self.app
