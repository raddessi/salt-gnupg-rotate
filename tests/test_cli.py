# -*- coding: utf-8 -*-
"""Tests for the `cli` module."""

import pytest
from typing import Union, Optional, Sequence, Mapping
from click.testing import CliRunner
from salt_gnupg_rotate import cli


@pytest.mark.parametrize(
    "args,env,config_files,expected_retcode",
    [
        pytest.param(None, {}, {}, 2, id="run_without_args"),
        pytest.param(["--show-config"], {}, {}, 2, id="show_config"),
        pytest.param(
            ["--something-unhandled", "--show-config"],
            {},
            {},
            2,
            id="show_config_with_unhandled_arg",
        ),
        pytest.param(
            [
                "--required-config-key=foo",
            ],
            {"SALT_GNUPG_ROTATE_unhandled": "bar"},
            {},
            0,
            id="run_with_unhandled_env_config_key",
        ),
        pytest.param(
            [
                "--required-config-key=foo",
                "--optional-config-key=4",
            ],
            {},
            {},
            0,
            id="run_with_both_config_keys",
        ),
        pytest.param(
            ["--required-config-key=foo"],
            {"SALT_GNUPG_ROTATE_optional_config_key": "1000"},
            {},
            0,
            id="run_with_optional_env_config_key",
        ),
        pytest.param(
            [
                "--required-config-key=foo",
            ],
            {},
            {},
            0,
            id="run",
        ),
        pytest.param(
            [
                "--required-config-key=foo",
                "--optional-config-key=bar",
            ],
            {},
            {},
            0,
            id="run_with_optional_config",
        ),
    ],
)
def test_cli(
    runner: CliRunner,
    args: Optional[Union[Sequence[str], str]],
    env: Optional[Mapping[str, Optional[str]]],
    config_files: Mapping[str, Mapping[str, Union[str, int]]],
    expected_retcode: int,
) -> None:
    """Verify it runs as expected.

    Args:
        runner: The Click CLI test runner
        args: Any args to be passed to the cli runner
        env: Any env variables that should be set for the cli runner
        config_files: A dict of file path names to dicts containing configuration
            variables that would have been read from those files
        expected_retcode: The expected exit status from the invocation

    """
    # TODO: how to load data from config files here?
    for config_file, config_data in config_files.items():
        print(config_file, config_data)

    result = runner.invoke(
        cli.cli,
        args=args,
        env=env,
        catch_exceptions=bool(expected_retcode),
    )
    print(result.output)
    assert result.exit_code == expected_retcode
