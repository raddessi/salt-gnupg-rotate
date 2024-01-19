# -*- coding: utf-8 -*-
"""Configuration for the pytest test suite."""

import functools
import sys
from typing import Iterator

import pytest
from click.testing import CliRunner


@pytest.fixture
def runner() -> Iterator[CliRunner]:
    """Yield a click.testing.CliRunner to invoke the CLI.

    Yields:
        click.testing.CliRunner: Runner for the test suite

    """
    class_ = CliRunner

    def invoke_wrapper(func):  # type: ignore
        """Augment CliRunner.invoke to emit its output to stdout.

        This enables pytest to show the output in its logs on test
        failures.

        Args:
            func: The function to be wrapped

        Returns:
            function: The wrapped function

        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):  # type: ignore
            echo = kwargs.pop("echo", False)
            result = func(*args, **kwargs)

            if echo is True:
                sys.stdout.write(result.output)

            return result

        return wrapper

    class_.invoke = invoke_wrapper(class_.invoke)  # type: ignore
    cli_runner = class_()

    yield cli_runner
