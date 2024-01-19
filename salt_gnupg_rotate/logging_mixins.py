"""Additions to the logging module."""

from typing import Optional, Union

import logging
import logging.handlers

import rich.logging
import rich.console


def add_trace_logging_level():
    trace_level_num = 5
    logging.addLevelName(trace_level_num, "TRACE")

    def trace(self, message, *args, **kwargs):
        if self.isEnabledFor(trace_level_num):
            self._log(trace_level_num, message, args, **kwargs)
    
    logging.Logger.trace = trace

def create_logger(
    app_name: str,
    child_name: Optional[str]=None,
    reset_handlers: bool=False,
    log_level: Optional[Union[int, str]]=None,
    console: Optional[rich.console.Console]=None,
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
        logger = logging.getLogger(f"{app_name}.{child_name}")
        logger.propagate = False
    else:
        logger = logging.getLogger(f"{app_name}")

    if reset_handlers:
        logger.handlers = []

    if not logger.hasHandlers():
        syslog_handler = logging.handlers.SysLogHandler("/dev/log")
        syslog_handler.formatter = logging.Formatter(
            f"{app_name}:"
            ' { "loggerName": "%(name)s", '
            '"timestamp": "%(asctime)s", "pathName": "%(pathname)s", '
            '"logRecordCreationTime": "%(created)f", '
            '"functionName": "%(funcName)s", "levelNo": "%(levelno)s", '
            '"lineNo": "%(lineno)d", "time": "%(msecs)d", '
            '"levelName": "%(levelname)s", "message": "%(message)s"}'
        )
        logger.addHandler(syslog_handler)
        logger.addHandler(
            rich.logging.RichHandler(rich_tracebacks=True, console=console, show_path=False)
        )

    logger.setLevel((log_level or "NOTSET").upper())

    return logger

add_trace_logging_level()
