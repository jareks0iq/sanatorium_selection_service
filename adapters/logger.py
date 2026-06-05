import logging
import sys

import structlog
from structlog.dev import ConsoleRenderer
from structlog.processors import JSONRenderer

from adapters.config import settings


def get_renderer() -> JSONRenderer | ConsoleRenderer:
    if settings.environment == "dev":
        return ConsoleRenderer()

    return JSONRenderer()


def configure_logging() -> None:

    timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)

    structlog_processors: list[structlog.types.Processor] = [
        structlog.stdlib.add_log_level,
        structlog.processors.add_log_level,
        structlog.contextvars.merge_contextvars,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        timestamper,
    ]

    structlog.configure(
        processors=structlog_processors + [get_renderer()],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )


def get_logger(name: str):
    return structlog.get_logger(name)
