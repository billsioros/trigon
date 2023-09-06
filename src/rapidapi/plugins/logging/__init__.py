from rapidapi.plugins import Plugin
from rapidapi.plugins.logging.middleware import LoggingMiddleware
from rapidapi.plugins.logging.event_handler import LoggingEventHandler
from rapidapi.core.event_handler import EventHandler
from rapidapi.core.middleware import Middleware
from typing import Type


class LoggingPlugin(Plugin):
    def get_event_handlers(self) -> list[EventHandler]:
        return [LoggingEventHandler]

    def get_middlewares(self) -> list[Type[Middleware]]:
        return [LoggingMiddleware]
