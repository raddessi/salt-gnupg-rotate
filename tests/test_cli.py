"""Tests for the `salt_gnupg_rotate.cli` submodule."""

from collections.abc import Sequence

import pytest
from click.testing import CliRunner
from pytest_mock import MockerFixture

from salt_gnupg_rotate import cli
from salt_gnupg_rotate.exceptions import DecryptionError, EncryptionError


@pytest.mark.parametrize(
    "args,exception,expected_retcode",
    [
        pytest.param(None, None, 2, id="run_without_args"),
        pytest.param(
            [
                "--directory=./tests/data/salt_pillar",
                "--recipient=pytest",
            ],
            None,
            0,
            id="run_with_minimal_kwargs",
        ),
        pytest.param(
            [
                "--directory=./tests/data/salt_pillar",
                "--recipient=pytest",
            ],
            NameError,
            1,
            id="raise_NameError",
        ),
        pytest.param(
            [
                "--directory=./tests/data/salt_pillar",
                "--recipient=pytest",
            ],
            DecryptionError,
            2,
            id="raise_DecryptionError",
        ),
        pytest.param(
            [
                "--directory=./tests/data/salt_pillar",
                "--recipient=pytest",
            ],
            EncryptionError,
            3,
            id="raise_EncryptionError",
        ),
        pytest.param(
            [
                "--directory=./tests/data/salt_pillar",
                "--recipient=pytest",
            ],
            Exception,
            9,
            id="raise_Exception",
        ),
    ],
)
def test_cli(
    mocker: MockerFixture,
    runner: CliRunner,
    args: Sequence[str] | str,
    exception: Exception | None,
    expected_retcode: int,
) -> None:
    """Verify the CLI runs as expected.

    Args:
        mocker: The pytest-mock mocker fixture
        runner: The Click CLI test runner
        args: Any args to be passed to the cli runner
        exception: The side effect exception to raise from within the call if desired
        expected_retcode: The expected exit status from the invocation

    """
    mocked_main = mocker.patch(
        "salt_gnupg_rotate.cli.main",
        return_value=2,
        side_effect=exception,
    )

    result = runner.invoke(
        cli.cli,
        args=args,
        catch_exceptions=bool(expected_retcode),
    )

    if expected_retcode and not exception:
        mocked_main.assert_not_called()
    else:
        mocked_main.assert_called()

    print(result.output)
    assert result.exit_code == expected_retcode
