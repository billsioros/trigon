import functools
import logging
import sys

from graypy.rabbitmq import GELFRabbitHandler
from loguru import _defaults, logger
from rapidapi.core.logging.handlers.intercept import InterceptHandler
from rapidapi.middlewares.correlation_id import get_correlation_id
from rapidapi.settings import Settings


def setup(settings: Settings):
    """Replaces logging handlers with a handler for using the custom handler.

    WARNING!
    if you call the setup in startup event function,
    then the first logs before the application start will be in the old format

    >>> app.add_event_handler("startup", setup)
    stdout:
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [11528] using statreload
    INFO:     Started server process [6036]
    INFO:     Waiting for application startup.
    2020-07-25 02:19:21.357 | INFO     | uvicorn.lifespan.on:startup:34 - Application startup complete.
    """
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
            "filter": correlation_id_filter,
        },
        {
            "sink": sys.stdout,
            "format": default_formatter,
            "filter": correlation_id_filter_factory(
                lambda record: record["level"].no < _defaults.LOGURU_WARNING_NO,
            ),
        },
        {
            "sink": sys.stderr,
            "format": default_formatter,
            "filter": correlation_id_filter_factory(
                lambda record: record["level"].no >= _defaults.LOGURU_WARNING_NO,
            ),
        },
    ]

    rabbitmq_url = str(settings.logging.uri)

    rabbitmq_logging_exchange = settings.logging.exchange
    rabbitmq_logging_routing_key = settings.logging.routing_key

    handlers.append(
        {
            "sink": GELFRabbitHandler(
                rabbitmq_url,
                exchange=rabbitmq_logging_exchange,
                routing_key=rabbitmq_logging_routing_key,
            ),
            "format": graylog_formatter,
            "filter": correlation_id_filter,
        },
    )

    logger.configure(handlers=handlers)


def correlation_id_filter_factory(method):
    @functools.wraps(method)
    def wrapper(record):
        if method(record):
            return correlation_id_filter(record)
        return None

    return wrapper


def correlation_id_filter(record):
    record["correlation_id"] = get_correlation_id()
    return True


def default_formatter(record):
    return (
        "[<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>] "
        f"{'[<magenta>{correlation_id}</magenta>]' if record['correlation_id'] is not None else ''}"
        "[<level>{level}</level>] "
        "[<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>] "
        "<level>{message}</level>\n"
        "{exception}"
    )


def graylog_formatter(record):
    return (
        f"{'{correlation_id}' if record['correlation_id'] is not None else ''}"
        "{message}\n"
        "{exception}"
    )
