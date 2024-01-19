# -*- coding: utf-8 -*-
"""Logging setup."""

import logging
import logging.handlers
from typing import Optional, Union

# pylint: disable=import-error
import rich.logging

from salt_gnupg_rotate.config import (
    APP_NAME,
    CONSOLE,
    DEFAULTS,
)


def create_logger(
    child_name: Optional[str]=None,
    reset_handlers: bool=False,
    log_level: Optional[Union[int, str]]=None,
) -> logging.Logger:
    """Set up the logger instance.

    Args:
        child_name: A child name to use for the logger. If not specified the
            main logger name will be used
        reset_handlers: If True, all existing handlers will be reset.
        log_level: The logging level name or integer to use.

    Returns:
        logging.Logger: Logger instance

    """
    if child_name:
        logger = logging.getLogger(f"{APP_NAME}.{child_name}")
        logger.propagate = False
    else:
        logger = logging.getLogger(f"{APP_NAME}")

    if reset_handlers:
        logger.handlers = []

    if not logger.hasHandlers():
        syslog_handler = logging.handlers.SysLogHandler("/dev/log")
        syslog_handler.formatter = logging.Formatter(
            f"{APP_NAME}:"
            ' { "loggerName": "%(name)s", '
            '"timestamp": "%(asctime)s", "pathName": "%(pathname)s", '
            '"logRecordCreationTime": "%(created)f", '
            '"functionName": "%(funcName)s", "levelNo": "%(levelno)s", '
            '"lineNo": "%(lineno)d", "time": "%(msecs)d", '
            '"levelName": "%(levelname)s", "message": "%(message)s"}'
        )
        logger.addHandler(syslog_handler)
        logger.addHandler(
            rich.logging.RichHandler(rich_tracebacks=True, console=CONSOLE)
        )

    logger.setLevel(log_level or DEFAULTS.get("log_level", None) or "NOTSET")

    return logger
