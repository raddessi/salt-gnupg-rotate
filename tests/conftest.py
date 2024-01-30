"""Configuration for the pytest test suite."""

import functools
import os
import shutil
import sys
from collections.abc import Iterator
from pathlib import Path

import gnupg
import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.tmpdir import TempPathFactory
from click.testing import CliRunner

SALT_PILLAR_DATADIR = "./tests/data/salt_pillar"


@pytest.fixture()
def runner() -> Iterator[CliRunner]:
    """Yield a click.testing.CliRunner to invoke the CLI.

    Returns:
        click.testing.CliRunner: Runner for the test suite

    """
    class_ = CliRunner

    def invoke_wrapper(func):  # noqa: ANN001, ANN202
        """Augment CliRunner.invoke to emit its output to stdout.

        This enables pytest to show the output in its logs on test
        failures.

        Args:
            func: The function to be wrapped

        Returns:
            function: The wrapped function

        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):  # noqa: ANN002, ANN003, ANN202
            echo = kwargs.pop("echo", False)
            result = func(*args, **kwargs)

            if echo is True:
                sys.stdout.write(result.output)

            return result

        return wrapper

    class_.invoke = invoke_wrapper(class_.invoke)

    return class_()


@pytest.fixture(name="pytest_gnupg_keyring_dirpath")
def gnupg_keyring_dirpath() -> str:
    """A fixture to return the path to the pytest gnupg keyring directory.

    Returns:
        str: dirpath of the keyring
    """
    return "./tests/data/gnupg"


@pytest.fixture(
    name="salt_pillar_fpath",
    scope="session",
    params=[
        "encrypted_file.gpg",
        "multiple_keys_in_yaml.sls",
        "one_key_in_yaml.sls",
        "nonconforming_file_type.txt",
        "duplicate_blocks_in_yaml.sls",
    ],
)
def salt_pillar_fpath_fixture(
    tmp_path_factory: TempPathFactory,
    request: FixtureRequest,
) -> str:
    """A fixture returning the path to a temp directory to use for pillar data.

    Args:
        tmp_path_factory: pytest-tmpdir fixture
        request: pytest request fixture

    Returns:
        str: Of the temp dir
    """
    temp_fpath = os.path.join(tmp_path_factory.mktemp("data"), request.param)
    shutil.copy(os.path.join(SALT_PILLAR_DATADIR, request.param), temp_fpath)
    return temp_fpath


@pytest.fixture(name="new_gnupg_homedir", scope="session")
def new_gnupg_homedir_fixture(tmp_path_factory: TempPathFactory) -> Path:
    """A fixture returning a temp dir path with a gnupg keyring inside.

    Args:
        tmp_path_factory: pytest-tmpdir fixture

    Returns:
        Path: Of the temp dir
    """
    temp_fpath = tmp_path_factory.mktemp("gnupg")
    gpg = gnupg.GPG(gnupghome=temp_fpath)
    gpg.gen_key_input(key_type="RSA", key_length=1024)
    return temp_fpath
