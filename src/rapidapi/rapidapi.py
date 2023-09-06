"""A batteries-included python web framework."""


from types import ModuleType
from typing import Any, Dict, Optional, Type, Union

from fastapi import APIRouter, FastAPI

from rapidapi.core.controller import Controller
from rapidapi.core.dependency_injection import Container
from rapidapi.core.event_handler import EventHandler
from rapidapi.core.middleware import Middleware
from rapidapi.core.settings import RapidAPISettings
from rapidapi.helpers.resolution import get_constructor_arguments, get_types
from rapidapi.plugins import Plugin


class RapidAPI(FastAPI):
    def configure(
        self,
        title: str = "RapidAPI",
        description: str = "A batteries-included python web framework",
        version: str = "1.0.0",
        contact: Optional[Dict[str, Union[str, Any]]] = None,
        docs_url: str = "/",
    ) -> "RapidAPI":
        self.title = title
        self.description = description
        self.version = version
        self.contact = contact
        self.docs_url = docs_url

        return self

    def register_config(self, settings: RapidAPISettings) -> "RapidAPI":
        self.state.settings = settings

    def register_container(self, container: Container):
        self.state.container = container._build()

        return self

    def register_controllers(self, *controller_types: Type[Controller]) -> "RapidAPI":
        def _(controller_type: Type[Controller]):
            arguments = get_constructor_arguments(controller_type)

            resolved_arguments = {}
            for arg_name, arg_type in arguments.items():
                try:
                    resolved_arguments[arg_name] = self.state.container[arg_type]
                except KeyError as e:
                    msg = f"Missing dependency for argument '{arg_name}' of type '{arg_type}'"
                    raise KeyError(
                        msg,
                    ) from e

            return controller_type(**resolved_arguments)

        api = APIRouter(prefix="/api")

        for controller in map(_, controller_types):
            api.include_router(controller.as_view())

        self.include_router(api)

        return self

    def discover_controllers(self, module: ModuleType) -> "RapidAPI":
        return self.register_controllers(*get_types(module, Controller))

    def register_middlewares(self, *middleware_types: Type[Middleware]) -> "RapidAPI":
        for middleware_type in middleware_types:
            self.add_middleware(middleware_type)

        return self

    def register_event_handlers(self, *handler_types: Type[EventHandler]) -> "RapidAPI":
        for handler_type in handler_types:
            handler = handler_type()
            self.add_event_handler(handler.event_type, handler)

        return self

    def register_plugins(self, *plugins: Plugin) -> "RapidAPI":
        for plugin in plugins:
            self.register_event_handlers(*plugin.get_event_handlers())
            self.register_middlewares(*plugin.get_middlewares())

        return self

    def build(self) -> FastAPI:
        return self
