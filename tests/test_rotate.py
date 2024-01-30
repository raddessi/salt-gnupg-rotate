"""Tests for the `salt_gnupg_rotate.main` submodule."""


from contextlib import nullcontext
from typing import TYPE_CHECKING

import gnupg
import pytest

if TYPE_CHECKING:
    from _pytest.python_api import RaisesContext
from pytest_mock import MockerFixture

from salt_gnupg_rotate.exceptions import DecryptionError, EncryptionError
from salt_gnupg_rotate.rotate import (
    PartiallyEncryptedFile,
    collect_file_paths,
    process_directory,
)


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


def test_PartiallyEncryptedFile_find_encrypted_blocks(
    salt_pillar_fpath: str,
    pytest_gnupg_keyring_dirpath: str,
) -> None:
    """Verify that PartiallyEncryptedFile.find_encrypted_blocks runs as expected.

    Args:
        salt_pillar_fpath: pytest fixture
        pytest_gnupg_keyring_dirpath: pytest fixture

    """
    gpg = gnupg.GPG(gnupghome=pytest_gnupg_keyring_dirpath)
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.find_encrypted_blocks()
    file.find_encrypted_blocks()


def test_PartiallyEncryptedFile_decrypt(
    salt_pillar_fpath: str,
    pytest_gnupg_keyring_dirpath: str,
) -> None:
    """Verify that PartiallyEncryptedFile.decrypt runs as expected.

    Args:
        salt_pillar_fpath: pytest fixture
        pytest_gnupg_keyring_dirpath: pytest fixture

    """
    gpg = gnupg.GPG(gnupghome=pytest_gnupg_keyring_dirpath)
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.decrypt()
    file.decrypt()


def test_PartiallyEncryptedFile_decrypt_DecryptionError(
    salt_pillar_fpath: str,
    new_gnupg_homedir: str,
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
    expectation: nullcontext[None] | RaisesContext[Exception]
    if file.encrypted_blocks:
        expectation = pytest.raises(DecryptionError)
    else:
        expectation = nullcontext()
    with expectation:
        file.decrypt()


def test_PartiallyEncryptedFile_decrypt_ValueError(
    salt_pillar_fpath: str,
    new_gnupg_homedir: str,
    mocker: MockerFixture,
) -> None:
    """Verify that PartiallyEncryptedFile.decrypt raises a ValueError as expected.

    Args:
        salt_pillar_fpath: pytest fixture
        new_gnupg_homedir: pytest fixture
        mocker: pytest-mock mocker fixture

    """
    gpg = gnupg.GPG(gnupghome=new_gnupg_homedir)
    mocker.patch(
        "salt_gnupg_rotate.rotate.PartiallyEncryptedFile.find_encrypted_blocks",
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


def test_PartiallyEncryptedFile_encrypt(
    salt_pillar_fpath: str,
    pytest_gnupg_keyring_dirpath: str,
) -> None:
    """Verify that PartiallyEncryptedFile.encrypt runs as expected.

    Args:
        salt_pillar_fpath: pytest fixture
        pytest_gnupg_keyring_dirpath: pytest fixture

    """
    gpg = gnupg.GPG(gnupghome=pytest_gnupg_keyring_dirpath)
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.encrypt()
    file.encrypt()


def test_PartiallyEncryptedFile_encrypt_EncryptionError_1(
    mocker: MockerFixture,
    salt_pillar_fpath: str,
    pytest_gnupg_keyring_dirpath: str,
) -> None:
    """PartiallyEncryptedFile.encrypt raises a EncryptionError as expected.

    Args:
        mocker: pytest-mock mocker fixture
        salt_pillar_fpath: pytest fixture
        pytest_gnupg_keyring_dirpath: pytest fixture

    """
    gpg = gnupg.GPG(gnupghome=pytest_gnupg_keyring_dirpath)
    mocked_gpg = mocker.Mock(
        encrypt=mocker.Mock(
            return_value=mocker.Mock(ok=False, problems=[{"status": "foo"}]),
        ),
    )
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=mocked_gpg,
        recipient="pytest",
    )
    file.decrypt()
    expectation: nullcontext[None] | RaisesContext[Exception]
    if file.encrypted_blocks:
        expectation = pytest.raises(EncryptionError)
    else:
        expectation = nullcontext()
    with expectation:
        file.encrypt()


def test_PartiallyEncryptedFile_encrypt_EncryptionError_2(
    salt_pillar_fpath: str,
    pytest_gnupg_keyring_dirpath: str,
) -> None:
    """PartiallyEncryptedFile.encrypt raises a EncryptionError as expected.

    Args:
        salt_pillar_fpath: pytest fixture
        pytest_gnupg_keyring_dirpath: pytest fixture

    """
    gpg = gnupg.GPG(gnupghome=pytest_gnupg_keyring_dirpath)
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.decrypt()
    expectation: nullcontext[None] | RaisesContext[Exception]
    if file.decrypted_blocks:
        # corrupt the replacement source data
        file.decrypted_blocks[0] = ("asdfasdf", *file.decrypted_blocks[0][1:])
        expectation = pytest.raises(EncryptionError)
    else:
        expectation = nullcontext()
    with expectation:
        file.encrypt()


def test_PartiallyEncryptedFile_encrypt_ValueError(
    salt_pillar_fpath: str,
    new_gnupg_homedir: str,
    mocker: MockerFixture,
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


def test_PartiallyEncryptedFile_write_reencrypted_contents(
    salt_pillar_fpath: str,
    pytest_gnupg_keyring_dirpath: str,
) -> None:
    """Verify that PartiallyEncryptedFile.write runs as expected.

    Args:
        salt_pillar_fpath: pytest fixture
        pytest_gnupg_keyring_dirpath: pytest fixture

    """
    gpg = gnupg.GPG(gnupghome=pytest_gnupg_keyring_dirpath)
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.write_reencrypted_contents()
    file.write_reencrypted_contents()


def test_PartiallyEncryptedFile_write_reencrypted_contents_failure(
    salt_pillar_fpath: str,
    mocker: MockerFixture,
    pytest_gnupg_keyring_dirpath: str,
) -> None:
    """Verify that PartiallyEncryptedFile.write fails as expected.

    Args:
        salt_pillar_fpath: pytest fixture
        mocker: pytest-mock mocker fixture
        pytest_gnupg_keyring_dirpath: pytest fixture

    """
    gpg = gnupg.GPG(gnupghome=pytest_gnupg_keyring_dirpath)
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


def test_process_directory(
    mocker: MockerFixture,
    salt_pillar_fpath: str,
    pytest_gnupg_keyring_dirpath: str,
) -> None:
    """Verify that process_directory runs as expected.

    Args:
        mocker: pytest-mock mocker fixture
        salt_pillar_fpath: pytest fixture
        pytest_gnupg_keyring_dirpath: pytest fixture

    """
    mocker.patch("salt_gnupg_rotate.rotate.PartiallyEncryptedFile")
    gpg = gnupg.GPG(gnupghome=pytest_gnupg_keyring_dirpath)
    process_directory(
        salt_pillar_fpath.rsplit("/", 1)[0],
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )


def test_process_directory_decrypt_failure(
    mocker: MockerFixture,
    salt_pillar_fpath: str,
    pytest_gnupg_keyring_dirpath: str,
) -> None:
    """Verify that process_directory raises an exception as expected.

    Args:
        mocker: pytest-mock mocker fixture
        salt_pillar_fpath: pytest fixture
        pytest_gnupg_keyring_dirpath: pytest fixture

    """
    mocker.patch(
        "salt_gnupg_rotate.rotate.PartiallyEncryptedFile.decrypt",
        side_effect=Exception,
    )
    gpg = gnupg.GPG(gnupghome=pytest_gnupg_keyring_dirpath)
    expectation: nullcontext[None] | RaisesContext[Exception]
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
    mocker: MockerFixture,
    salt_pillar_fpath: str,
    pytest_gnupg_keyring_dirpath: str,
) -> None:
    """Verify that process_directory raises an exception as expected.

    Args:
        mocker: pytest-mock mocker fixture
        salt_pillar_fpath: pytest fixture
        pytest_gnupg_keyring_dirpath: pytest fixture

    """
    mocker.patch(
        "salt_gnupg_rotate.rotate.PartiallyEncryptedFile.encrypt",
        side_effect=Exception,
    )
    gpg = gnupg.GPG(gnupghome=pytest_gnupg_keyring_dirpath)
    expectation: nullcontext[None] | RaisesContext[Exception]
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


def test_process_directory_write(
    salt_pillar_fpath: str,
    pytest_gnupg_keyring_dirpath: str,
) -> None:
    """Verify that process_directory will write out updates.

    Args:
        salt_pillar_fpath: pytest fixture
        pytest_gnupg_keyring_dirpath: pytest fixture

    """
    gpg = gnupg.GPG(gnupghome=pytest_gnupg_keyring_dirpath)
    process_directory(
        salt_pillar_fpath.rsplit("/", 1)[0],
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
        write=True,
    )


def test_process_directory_write_failure(
    mocker: MockerFixture,
    salt_pillar_fpath: str,
    pytest_gnupg_keyring_dirpath: str,
) -> None:
    """Verify that process_directory raises an exception on write as expected.

    Args:
        mocker: pytest-mock mocker fixture
        salt_pillar_fpath: pytest fixture
        pytest_gnupg_keyring_dirpath: pytest fixture

    """
    mocker.patch(
        "salt_gnupg_rotate.rotate.PartiallyEncryptedFile.write_reencrypted_contents",
        side_effect=Exception,
    )
    gpg = gnupg.GPG(gnupghome=pytest_gnupg_keyring_dirpath)
    expectation: nullcontext[None] | RaisesContext[Exception]
    if salt_pillar_fpath.endswith("nonconforming_file_type.txt"):
        expectation = nullcontext()
    else:
        expectation = pytest.raises(EncryptionError)
    with expectation:
        process_directory(
            salt_pillar_fpath.rsplit("/", 1)[0],
            decryption_gpg_keyring=gpg,
            encryption_gpg_keyring=gpg,
            recipient="pytest",
            write=True,
        )
