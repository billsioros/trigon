import logging
import sys
from typing import Any, Dict, Type

from loguru import _defaults, logger

from rapidapi.core.event_handler import EventHandler
from rapidapi.core.logging.middleware import LoggingMiddleware
from rapidapi.core.middleware import Middleware
from rapidapi.core.logging.handlers import InterceptHandler


def default_formatter(record):
    return (
        "[<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>] "
        "[<level>{level}</level>] "
        "[<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>] "
        "<level>{message}</level>\n"
        "{exception}"
    )


class LoggerBuilder:
    def __init__(self) -> None:
        self.override_tags: list[str] = []
        self.middleware_type: Type[Middleware] | None = None
        self.handlers: list[Dict[str, Any]] = []

    def override(self, *tags: str):
        self.override_tags = tags

        return self

    def add_file_handler(
        self,
        sink: str,
        format=default_formatter,
        retention="7 days",
        compression="zip",
        rotation="500 MB",
    ):
        self.handlers.append(
            {
                "sink": sink,
                "format": format,
                "colorize": False,
                "retention": retention,
                "compression": compression,
                "rotation": rotation,
            },
        )

        return self

    def add_console_handler(
        self,
        error=False,
        format=default_formatter,
    ):
        sink, filter = None, None

        if error:
            sink = sys.stderr

            def filter(record):
                return record["level"].no >= _defaults.LOGURU_WARNING_NO

        else:
            sink = sys.stdout

            def filter(record):
                return record["level"].no < _defaults.LOGURU_WARNING_NO

        self.handlers.append(
            {
                "sink": sink,
                "format": format,
                "filter": filter,
            },
        )

        return self

    def register_middleware(self, middleware_type: Type[Middleware] | None = None):
        self.middleware_type = middleware_type

        if self.middleware_type is None:
            self.middleware_type = LoggingMiddleware

        return self

    def _get_event_handler(self):
        class LoggingEventHandler(EventHandler):
            event_type = "startup"

            def __call__(__event_handler_self__) -> None:
                if self.override_tags:
                    for tag in self.override_tags:
                        conventional_loggers = (
                            logging.getLogger(name)
                            for name in logging.root.manager.loggerDict
                            if name.startswith(f"{tag}.")
                        )
                        for conventional_logger in conventional_loggers:
                            conventional_logger.handlers = []

                        intercept_handler = InterceptHandler()
                        logging.getLogger(tag).handlers = [intercept_handler]

                logger.configure(handlers=self.handlers)

        return LoggingEventHandler
