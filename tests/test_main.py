"""Tests for the `salt_gnupg_rotate.main` submodule."""

import pytest
from pytest_mock import MockerFixture

from salt_gnupg_rotate.exceptions import DecryptionError
from salt_gnupg_rotate.main import main


def test_main_return_value(mocker: MockerFixture) -> None:
    """Verify that main returns as expected.

    Args:
        mocker: pytest-mock mocker fixture
    """
    mocked_process_directory = mocker.patch(
        "salt_gnupg_rotate.main.process_directory",
        return_value=2,
    )
    main(
        dirpath="./tests/data/salt_pillar",
        recipient="pytest",
    )
    mocked_process_directory.assert_called()


def test_main_return_value_on_write(mocker: MockerFixture) -> None:
    """Verify that main returns as expected when write=True.

    Args:
        mocker: pytest-mock mocker fixture
    """
    mocked_process_directory = mocker.patch(
        "salt_gnupg_rotate.main.process_directory",
        return_value=2,
    )
    main(
        dirpath="./tests/data/salt_pillar",
        recipient="pytest",
        write=True,
    )
    mocked_process_directory.assert_called()


def test_main_gpg_keyring_missing_secret_key(mocker: MockerFixture) -> None:
    """Verify that main raises as expected when a secret key is missing.

    Args:
        mocker: pytest-mock mocker fixture
    """
    mocked_gpg = mocker.patch("salt_gnupg_rotate.main.gnupg.GPG")
    mocked_gpg.side_effect = [
        mocker.Mock(),
        mocker.Mock(list_keys=mocker.Mock(return_value=[])),
    ]
    with pytest.raises(NameError):
        main(
            dirpath="./tests/data/salt_pillar",
            recipient="pytest",
        )


def test_main_decryption_error(mocker: MockerFixture) -> None:
    """Verify that main raises as expected on a decryption error.

    Args:
        mocker: pytest-mock mocker fixture
    """
    mocked_process_directory = mocker.patch(
        "salt_gnupg_rotate.main.process_directory",
        side_effect=DecryptionError,
    )
    main(
        dirpath="./tests/data/salt_pillar",
        recipient="pytest",
    )
    mocked_process_directory.assert_called()
