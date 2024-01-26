"""Additions to the logging module."""

import logging
import logging.handlers
from typing import Optional, Union

import rich.console
import rich.logging

TRACE_LEVEL_NUM = 5

class CustomLogger(logging.Logger):
    """Logger module with a trace level added."""

    def trace(self, message, *args, **kwargs) -> None:
        if self.isEnabledFor(TRACE_LEVEL_NUM):
            self._log(TRACE_LEVEL_NUM, message, args, **kwargs)

def create_logger(
    app_name: str,
    log_level: Optional[Union[int, str]] = None,
    console: Optional[rich.console.Console] = None,
) -> CustomLogger:
    """Set up the logger instance.

    Args:
        app_name: The name of the logger to create
        log_level: The logging level name or integer to use.
        console: The rich module console to use for output

    Returns:
        CustomLogger: Logger instance

    """
    logger = logging.getLogger(f"{app_name}")

    logger.addHandler(
        rich.logging.RichHandler(rich_tracebacks=True, console=console, show_path=False)
    )

    logger.setLevel((log_level or "NOTSET").upper())

    return logger



logging.setLoggerClass(CustomLogger)
logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")
