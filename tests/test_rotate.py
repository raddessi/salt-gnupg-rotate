"""Tests for the `salt_gnupg_rotate.main` submodule."""

import os
import shutil
from contextlib import nullcontext
from pathlib import Path
from typing import Union

import gnupg
import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.python_api import RaisesContext
from _pytest.tmpdir import TempPathFactory
from pytest_mock import MockerFixture

from salt_gnupg_rotate.exceptions import DecryptionError, EncryptionError
from salt_gnupg_rotate.rotate import (
    PartiallyEncryptedFile,
    collect_file_paths,
    process_directory,
)

SALT_PILLAR_DATADIR = "./tests/data/salt_pillar"
GNUPG_HOMEDIR = "./tests/data/gnupg"


# pylint: disable=invalid-name
def test_PartiallyEncryptedFile_instance(mocker: MockerFixture) -> None:
    """Test that PartiallyEncryptedFile can be instantiated.

    Args:
        mocker: pytest-mock mocker fixture
    """
    PartiallyEncryptedFile(
        path="./tests/data/salt_pillar/encrypted_file.gpg",
        decryption_gpg_keyring=mocker.Mock(),
        encryption_gpg_keyring=mocker.Mock(),
        recipient="pytest",
    )


@pytest.fixture(
    name="salt_pillar_fpath",
    scope="session",
    params=[
        "encrypted_file.gpg",
        "multiple_keys_in_yaml.sls",
        "one_key_in_yaml.sls",
        "nonconforming_file_type.txt",
    ],
)
def salt_pillar_fpath_fixture(
    tmp_path_factory: TempPathFactory, request: FixtureRequest
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


# pylint: disable=invalid-name
def test_PartiallyEncryptedFile_find_encrypted_blocks(salt_pillar_fpath: str) -> None:
    """Verify that PartiallyEncryptedFile.find_encrypted_blocks runs as expected.

    Args:
        salt_pillar_fpath: pytest fixture

    """
    gpg = gnupg.GPG(gnupghome=GNUPG_HOMEDIR)
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.find_encrypted_blocks()
    file.find_encrypted_blocks()


# pylint: disable=invalid-name
def test_PartiallyEncryptedFile_decrypt(salt_pillar_fpath: str) -> None:
    """Verify that PartiallyEncryptedFile.decrypt runs as expected.

    Args:
        salt_pillar_fpath: pytest fixture

    """
    gpg = gnupg.GPG(gnupghome=GNUPG_HOMEDIR)
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.decrypt()
    file.decrypt()


# pylint: disable=invalid-name
def test_PartiallyEncryptedFile_decrypt_DecryptionError(
    salt_pillar_fpath: str, new_gnupg_homedir: str
) -> None:
    """Verify that PartiallyEncryptedFile.decrypt raises a DecryptionError as expected.

    Args:
        salt_pillar_fpath: pytest fixture
        new_gnupg_homedir: pytest fixture

    """
    gpg = gnupg.GPG(gnupghome=new_gnupg_homedir)
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.find_encrypted_blocks()
    expectation: Union[nullcontext[None], RaisesContext[Exception]]
    if file.encrypted_blocks:
        expectation = pytest.raises(DecryptionError)
    else:
        expectation = nullcontext()
    with expectation:
        file.decrypt()


# pylint: disable=invalid-name
def test_PartiallyEncryptedFile_decrypt_ValueError(
    salt_pillar_fpath: str, new_gnupg_homedir: str, mocker: MockerFixture
) -> None:
    """Verify that PartiallyEncryptedFile.decrypt raises a ValueError as expected.

    Args:
        salt_pillar_fpath: pytest fixture
        new_gnupg_homedir: pytest fixture
        mocker: pytest-mock mocker fixture

    """
    gpg = gnupg.GPG(gnupghome=new_gnupg_homedir)
    mocker.patch(
        "salt_gnupg_rotate.rotate.PartiallyEncryptedFile.find_encrypted_blocks"
    )
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.find_encrypted_blocks()
    with pytest.raises(ValueError):
        file.decrypt()


# pylint: disable=invalid-name
def test_PartiallyEncryptedFile_encrypt(salt_pillar_fpath: str) -> None:
    """Verify that PartiallyEncryptedFile.encrypt runs as expected.

    Args:
        salt_pillar_fpath: pytest fixture

    """
    gpg = gnupg.GPG(gnupghome=GNUPG_HOMEDIR)
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.encrypt()
    file.encrypt()


# pylint: disable=invalid-name
def test_PartiallyEncryptedFile_encrypt_EncryptionError_1(
    mocker: MockerFixture, salt_pillar_fpath: str
) -> None:
    """Verify that PartiallyEncryptedFile.encrypt raises a EncryptionError runs as expected.

    Args:
        mocker: pytest-mock mocker fixture
        salt_pillar_fpath: pytest fixture

    """
    gpg = gnupg.GPG(gnupghome=GNUPG_HOMEDIR)
    mocked_gpg = mocker.Mock(
        encrypt=mocker.Mock(
            return_value=mocker.Mock(ok=False, problems=[{"status": "foo"}])
        )
    )
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=mocked_gpg,
        recipient="pytest",
    )
    file.decrypt()
    expectation: Union[nullcontext[None], RaisesContext[Exception]]
    if file.encrypted_blocks:
        expectation = pytest.raises(EncryptionError)
    else:
        expectation = nullcontext()
    with expectation:
        file.encrypt()


# pylint: disable=invalid-name
def test_PartiallyEncryptedFile_encrypt_EncryptionError_2(
    salt_pillar_fpath: str,
) -> None:
    """Verify that PartiallyEncryptedFile.encrypt raises a EncryptionError runs as expected.

    Args:
        salt_pillar_fpath: pytest fixture

    """
    gpg = gnupg.GPG(gnupghome=GNUPG_HOMEDIR)
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.decrypt()
    expectation: Union[nullcontext[None], RaisesContext[Exception]]
    if file.decrypted_blocks:
        # corrupt the replacement source data
        file.decrypted_blocks[0] = ("asdfasdf", *file.decrypted_blocks[0][1:])
        expectation = pytest.raises(EncryptionError)
    else:
        expectation = nullcontext()
    with expectation:
        file.encrypt()


# pylint: disable=invalid-name
def test_PartiallyEncryptedFile_encrypt_ValueError(
    salt_pillar_fpath: str, new_gnupg_homedir: str, mocker: MockerFixture
) -> None:
    """Verify that PartiallyEncryptedFile.encrypt raises a ValueError as expected.

    Args:
        salt_pillar_fpath: pytest fixture
        new_gnupg_homedir: pytest fixture
        mocker: pytest-mock mocker fixture

    """
    gpg = gnupg.GPG(gnupghome=new_gnupg_homedir)
    mocker.patch("salt_gnupg_rotate.rotate.PartiallyEncryptedFile.decrypt")
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.find_encrypted_blocks()
    with pytest.raises(ValueError):
        file.encrypt()


# pylint: disable=invalid-name
def test_PartiallyEncryptedFile_write_reencrypted_contents(
    salt_pillar_fpath: str,
) -> None:
    """Verify that PartiallyEncryptedFile.write runs as expected.

    Args:
        salt_pillar_fpath: pytest fixture

    """
    gpg = gnupg.GPG(gnupghome=GNUPG_HOMEDIR)
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.write_reencrypted_contents()
    file.write_reencrypted_contents()


# pylint: disable=invalid-name
def test_PartiallyEncryptedFile_write_reencrypted_contents_failure(
    salt_pillar_fpath: str, mocker: MockerFixture
) -> None:
    """Verify that PartiallyEncryptedFile.write fails as expected.

    Args:
        salt_pillar_fpath: pytest fixture
        mocker: pytest-mock mocker fixture

    """
    gpg = gnupg.GPG(gnupghome=GNUPG_HOMEDIR)
    mocker.patch("salt_gnupg_rotate.rotate.PartiallyEncryptedFile.encrypt")
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.write_reencrypted_contents()


def test_collect_file_paths(salt_pillar_fpath: str) -> None:
    """Verify that collect_file_paths runs as expected.

    Args:
        salt_pillar_fpath: pytest fixture

    """
    collect_file_paths(salt_pillar_fpath)


def test_process_directory(mocker: MockerFixture, salt_pillar_fpath: str) -> None:
    """Verify that process_directory runs as expected.

    Args:
        mocker: pytest-mock mocker fixture
        salt_pillar_fpath: pytest fixture

    """
    mocker.patch("salt_gnupg_rotate.rotate.PartiallyEncryptedFile")
    gpg = gnupg.GPG(gnupghome=GNUPG_HOMEDIR)
    process_directory(
        salt_pillar_fpath.rsplit("/", 1)[0],
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )


def test_process_directory_decrypt_failure(
    mocker: MockerFixture, salt_pillar_fpath: str
) -> None:
    """Verify that process_directory raises an exception as expected.

    Args:
        mocker: pytest-mock mocker fixture
        salt_pillar_fpath: pytest fixture

    """
    mocker.patch(
        "salt_gnupg_rotate.rotate.PartiallyEncryptedFile.decrypt",
        side_effect=Exception,
    )
    gpg = gnupg.GPG(gnupghome=GNUPG_HOMEDIR)
    expectation: Union[nullcontext[None], RaisesContext[Exception]]
    if salt_pillar_fpath.endswith("nonconforming_file_type.txt"):
        expectation = nullcontext()
    else:
        expectation = pytest.raises(ValueError)
    with expectation:
        process_directory(
            salt_pillar_fpath.rsplit("/", 1)[0],
            decryption_gpg_keyring=gpg,
            encryption_gpg_keyring=gpg,
            recipient="pytest",
        )


def test_process_directory_encrypt_failure(
    mocker: MockerFixture, salt_pillar_fpath: str
) -> None:
    """Verify that process_directory raises an exception as expected.

    Args:
        mocker: pytest-mock mocker fixture
        salt_pillar_fpath: pytest fixture

    """
    mocker.patch(
        "salt_gnupg_rotate.rotate.PartiallyEncryptedFile.encrypt",
        side_effect=Exception,
    )
    gpg = gnupg.GPG(gnupghome=GNUPG_HOMEDIR)
    expectation: Union[nullcontext[None], RaisesContext[Exception]]
    if salt_pillar_fpath.endswith("nonconforming_file_type.txt"):
        expectation = nullcontext()
    else:
        expectation = pytest.raises(ValueError)
    with expectation:
        process_directory(
            salt_pillar_fpath.rsplit("/", 1)[0],
            decryption_gpg_keyring=gpg,
            encryption_gpg_keyring=gpg,
            recipient="pytest",
        )


def test_process_directory_write(salt_pillar_fpath: str) -> None:
    """Verify that process_directory will write out updates.

    Args:
        salt_pillar_fpath: pytest fixture

    """
    gpg = gnupg.GPG(gnupghome=GNUPG_HOMEDIR)
    process_directory(
        salt_pillar_fpath.rsplit("/", 1)[0],
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
        write=True,
    )


def test_process_directory_write_failure(
    mocker: MockerFixture, salt_pillar_fpath: str
) -> None:
    """Verify that process_directory raises an exception on write as expected.

    Args:
        mocker: pytest-mock mocker fixture
        salt_pillar_fpath: pytest fixture

    """
    mocker.patch(
        "salt_gnupg_rotate.rotate.PartiallyEncryptedFile.write_reencrypted_contents",
        side_effect=Exception,
    )
    gpg = gnupg.GPG(gnupghome=GNUPG_HOMEDIR)
    expectation: Union[nullcontext[None], RaisesContext[Exception]]
    if salt_pillar_fpath.endswith("nonconforming_file_type.txt"):
        expectation = nullcontext()
    else:
        expectation = pytest.raises(Exception)
    with expectation:
        process_directory(
            salt_pillar_fpath.rsplit("/", 1)[0],
            decryption_gpg_keyring=gpg,
            encryption_gpg_keyring=gpg,
            recipient="pytest",
            write=True,
        )
