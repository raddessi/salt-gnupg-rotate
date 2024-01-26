"""Tests for the `salt_gnupg_rotate.logging_mixins` submodule."""

import logging
from contextlib import ExitStack as does_not_raise
from typing import Any, ContextManager, Union

import pytest
import rich.console

from salt_gnupg_rotate.logging_mixins import create_logger


@pytest.mark.parametrize(
    "app_name,log_level,expectation,expected_log_level",
    [
        pytest.param(
            "mylogger",
            None,
            does_not_raise(),
            "NOTSET",
            id="defaults",
        ),
        pytest.param(
            "mylogger",
            "debug",
            does_not_raise(),
            "DEBUG",
            id="log_level_debug_lowercase",
        ),
        pytest.param(
            "mylogger",
            "TRACE",
            does_not_raise(),
            "TRACE",
            id="log_level_trace",
        ),
        pytest.param(
            "mylogger",
            "FOO",
            pytest.raises(ValueError),
            None,
            id="invalid_log_level",
        ),
    ],
)
def test_create_logger(
    app_name: str,
    log_level: Union[int, str],
    expectation: ContextManager[Any],
    expected_log_level: str,
) -> None:
    """Verify that creating a logger works as expected.

    Args:
        app_name: The name of the application
        log_level: The logging level to use
        expectation: The context manager for the expected exception raising condition of
            this test
        expected_log_level: The expected log level the logger shoudl be set to

    """
    console = rich.console.Console(stderr=True)
    with expectation:
        logger = create_logger(app_name=app_name, log_level=log_level, console=console)

        assert isinstance(logger, logging.Logger)
        assert logging._levelToName[logger.level] == expected_log_level

        logger.trace("verify trace level logging works")
