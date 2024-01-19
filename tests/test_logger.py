# -*- coding: utf-8 -*-
"""Tests for the `logger` module."""

import logging
import pytest
from contextlib import ExitStack as does_not_raise
from typing import ContextManager, Union, Any

from salt_gnupg_rotate.logger import create_logger


@pytest.mark.parametrize(
    "child_name,reset_handlers,log_level,expectation",
    [
        pytest.param(
            None,
            False,
            None,
            does_not_raise(),
            id="defaults",
        ),
        pytest.param(
            "childlogger1",
            False,
            None,
            does_not_raise(),
            id="child",
        ),
        pytest.param(
            None,
            True,
            None,
            does_not_raise(),
            id="reset_handlers",
        ),
        pytest.param(
            "childlogger2",
            True,
            None,
            does_not_raise(),
            id="reset_handlers_on_child",
        ),
        pytest.param(
            None,
            False,
            "INFO",
            does_not_raise(),
            id="log_level_INFO",
        ),
        pytest.param(
            None,
            False,
            "FOO",
            pytest.raises(ValueError),
            id="log_level_FOO",
        ),
    ],
)
def test_create_logger(
    child_name: Union[str, None],
    reset_handlers: bool,
    log_level: Union[int, str],
    expectation: ContextManager[Any],
) -> None:
    """Verify that creating a logger works as expected.

    Args:
        child_name: The name of the child logger to set up, if a child is desired
        reset_handlers: True if the existing handlers should be reset
        log_level: The logging level to use
        expectation: The context manager for the expected exception raising condition of
            this test

    """
    with expectation:
        logger = create_logger(
            child_name=child_name, reset_handlers=reset_handlers, log_level=log_level
        )

        assert isinstance(logger, logging.Logger)
        if child_name:
            assert logger.name.endswith(f".{child_name}")
