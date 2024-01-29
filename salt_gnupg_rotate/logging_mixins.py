"""Additions to the logging module."""

import logging
from typing import Any, Optional

import rich.console
import rich.logging

TRACE_LEVEL_NUM = 5


class CustomLogger(logging.Logger):
    """Logger module with a trace level added."""

    def trace(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Emit a trace log message.

        Args:
            message: The log message contents
            *args: Any args
            **kwargs: Any keyword args

        """
        if self.isEnabledFor(TRACE_LEVEL_NUM):
            self._log(TRACE_LEVEL_NUM, message, args, **kwargs)


logging.setLoggerClass(CustomLogger)
logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")


def create_logger(
    app_name: str,
    log_level: Optional[str] = None,
    console: Optional[rich.console.Console] = None,
) -> CustomLogger:
    """Set up the logger instance.

    Args:
        app_name: The name of the logger to create
        log_level: The logging level name or integer to use.
        console: The rich module console to use for output

    Returns:
        CustomLogger: Logger instance

    Raises:
        TypeError: If the logger class is not as expected

    """
    logger = logging.getLogger(app_name)

    if not isinstance(logger, CustomLogger):
        raise TypeError(f"Logger instance not of type CustomLogger: {type(logger)}")

    logger.addHandler(
        rich.logging.RichHandler(rich_tracebacks=True, console=console, show_path=False)
    )

    logger.setLevel((log_level or "NOTSET").upper())

    return logger
