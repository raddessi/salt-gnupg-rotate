"""Tests for the `salt_gnupg_rotate.logging_mixins` submodule."""

import logging
from contextlib import AbstractContextManager, nullcontext

import pytest
import rich.console
from pytest_mock import MockerFixture

from salt_gnupg_rotate.logging_mixins import create_logger


@pytest.mark.parametrize(
    ("app_name", "log_level", "expectation", "expected_log_level"),
    [
        pytest.param(
            "mylogger",
            None,
            nullcontext(),
            "NOTSET",
            id="defaults",
        ),
        pytest.param(
            "mylogger",
            "debug",
            nullcontext(),
            "DEBUG",
            id="log_level_debug_lowercase",
        ),
        pytest.param(
            "mylogger",
            "TRACE",
            nullcontext(),
            "TRACE",
            id="log_level_trace",
        ),
        pytest.param(
            "mylogger",
            "FOO",
            pytest.raises(ValueError, match="Unknown level:"),
            None,
            id="invalid_log_level",
        ),
    ],
)
def test_create_logger(
    app_name: str,
    log_level: str,
    expectation: AbstractContextManager,
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
        assert logging._levelToName[logger.level] == expected_log_level  # noqa: SLF001

        logger.trace("verify trace level logging works")


def test_create_logger_custom_logger(mocker: MockerFixture) -> None:
    """Verify that create_logger will always return a CustomLogger.

    Args:
        mocker: pytest-mock mocker fixture
    """
    mocker.patch(
        "salt_gnupg_rotate.logging_mixins.logging.getLogger",
        return_value=mocker.Mock(__class__=logging.Logger),
    )
    with pytest.raises(TypeError):
        create_logger(app_name="blah", log_level="INFO", console=mocker.Mock())
