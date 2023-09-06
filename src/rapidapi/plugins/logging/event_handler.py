import logging
import sys

from loguru import _defaults, logger

from rapidapi.core.event_handler import EventHandler


class InterceptHandler(logging.Handler):
    """Default handler from examples in loguru documentation.

    See
    https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging.
    """

    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def default_formatter(record):
    return (
        "[<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>] "
        "[<level>{level}</level>] "
        "[<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>] "
        "<level>{message}</level>\n"
        "{exception}"
    )


class LoggingEventHandler(EventHandler):
    event_type = 'startup'

    def __call__(self) -> None:
        """Replaces logging handlers with a handler for using the custom handler."""
        # disable handlers for specific uvicorn loggers
        # to redirect their output to the default uvicorn logger
        # works with uvicorn==0.11.6
        loggers = (
            logging.getLogger(name)
            for name in logging.root.manager.loggerDict
            if name.startswith("uvicorn.")
        )
        for uvicorn_logger in loggers:
            uvicorn_logger.handlers = []

        # change handler for default uvicorn logger
        intercept_handler = InterceptHandler()
        logging.getLogger("uvicorn").handlers = [intercept_handler]

        handlers = [
            {
                "sink": "logs/backend_{time}.log",
                "format": default_formatter,
                "colorize": False,
                "retention": "7 days",
                "compression": "zip",
                "rotation": "500 MB",
            },
            {
                "sink": sys.stdout,
                "format": default_formatter,
                "filter": lambda record: record["level"].no < _defaults.LOGURU_WARNING_NO,
            },
            {
                "sink": sys.stderr,
                "format": default_formatter,
                "filter": lambda record: record["level"].no >= _defaults.LOGURU_WARNING_NO,
            },
        ]

        logger.configure(handlers=handlers)
