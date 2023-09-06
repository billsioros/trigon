from typing import Type

from rapidapi.core.controller import Controller
from rapidapi.core.dependency_injection import ContainerBuilder
from rapidapi.core.event_handler import EventHandler
from rapidapi.core.middleware import Middleware


class Plugin:
    def register_dependencies(self, container: ContainerBuilder) -> ContainerBuilder:
        return container

    def get_controllers(self) -> list[Type[Controller]]:
        return []

    def get_middlewares(self) -> list[Type[Middleware]]:
        return []

    def get_event_handlers(self) -> list[EventHandler]:
        return []
