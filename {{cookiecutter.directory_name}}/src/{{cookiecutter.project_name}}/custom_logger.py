"""Custom Logger delegates to click for actual printing.

Note: actual logging system is 'loguru' which enables easy configuration
of structured logging.
"""
import datetime
import json
import logging

import click
import loguru
from loguru import logger

fg_color_map = {
    logging.CRITICAL: "red",
    logging.FATAL: "red",
    logging.ERROR: "red",
    logging.WARNING: "blue",
    logging.WARN: "blue",
    logging.INFO: "yellow",
    logging.DEBUG: "green",
    logging.NOTSET: "green",
}

bg_color_map = {
    logging.CRITICAL: "blue",
    logging.FATAL: "magenta",
    logging.ERROR: "black",
    logging.WARNING: "black",
    logging.WARN: "black",
    logging.INFO: "black",
    logging.DEBUG: "black",
    logging.NOTSET: "black",
}


class ClickLoggingHandler(logging.Handler):
    """ClickLoggingHandler delegates log messages to click.

    The `click framework` captures stdout and stderr. Logging to
    either stdout or stderr therefore requires a way to delegate
    back to click.
    """

    def emit(self, record: logging.LogRecord) -> None:
        """Emits a structured log record via 'click.secho'."""
        click.secho(
            message=json.dumps(format_record(record), skipkeys=True, default=str),
            bg=bg_color_map[record.levelno],
            fg=fg_color_map[record.levelno],
        )


class InterceptHandler(logging.Handler):
    """Intercept standard logging and redirect to loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        """Intercept standard logging event and emit a loguru event."""
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            if frame.f_back is None:
                break
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def format_record(record: logging.LogRecord) -> dict:
    """Format a record as a dict, for rendering as a json structured log."""
    a = {
        "level": record.levelname,
        "module": record.module,
        "lineno": record.lineno,
        "msg": record.getMessage(),
        "utc": datetime.datetime.utcnow(),
    }
    b = {**a, **record.extra}  # type: ignore
    return b


def init_click_logger(level: str) -> None:
    """Invoked by application entry point to set logging level."""
    logger.remove()
    logger.add(
        ClickLoggingHandler(),
        format="{message}",
        serialize=False,
        level=f"{level.upper()}",
    )
    loguru.logger = logger
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
