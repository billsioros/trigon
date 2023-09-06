from rapidapi.core.controller import Controller
from rapidapi.core.middleware import Middleware
from rapidapi.core.event_handler import EventHandler
from typing import Type


class Plugin(object):
    def get_controllers(self) -> list[Type[Controller]]:
        return []

    def get_middlewares(self) -> list[Type[Middleware]]:
        return []

    def get_event_handlers(self) -> list[Type[EventHandler]]:
        return []
