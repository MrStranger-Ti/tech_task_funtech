import logging.config

from app.core.settings import settings

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "[%(asctime)s] - %(levelname)s - %(module)s:%(funcName)s >> %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "base": {
            "level": settings.server.LOGGING_LEVEL,
            "formatter": "base",
            "class": "logging.StreamHandler",
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "root": {
        "level": settings.server.LOGGING_LEVEL,
        "handlers": ["base"],
    },
    "loggers": {
        "sqlalchemy": {
            "level": "CRITICAL",
            "handlers": ["null"],
            "propagate": False,
        },
    },
}


def configure_logging() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
