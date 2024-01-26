"""Tests for the `salt_gnupg_rotate.main` submodule."""

import logging
import os
import shutil
from contextlib import nullcontext
from typing import Any, Union
from _pytest.python_api import RaisesContext
from _pytest.tmpdir import TempPathFactory
from _pytest.fixtures import FixtureRequest
from pathlib import Path
from pytest_mock import MockerFixture

import gnupg
import pytest

from salt_gnupg_rotate.exceptions import DecryptionError
from salt_gnupg_rotate.rotate import (
    PartiallyEncryptedFile,
    collect_file_paths,
    process_directory,
)

SALT_PILLAR_DATADIR = "./tests/data/salt_pillar"
GNUPG_HOMEDIR = "./tests/data/gnupg"


def test_PartiallyEncryptedFile_instance(mocker: MockerFixture) -> None:
    PartiallyEncryptedFile(
        path="./tests/data/salt_pillar/encrypted_file.gpg",
        decryption_gpg_keyring=mocker.Mock(),
        encryption_gpg_keyring=mocker.Mock(),
        recipient="pytest",
    )


@pytest.fixture(
    scope="session",
    params=[
        "encrypted_file.gpg",
        "multiple_keys_in_yaml.sls",
        "one_key_in_yaml.sls",
        "nonconforming_file_type.txt",
    ],
)
def salt_pillar_fpath(tmp_path_factory: TempPathFactory, request: FixtureRequest) -> str:
    temp_fpath = os.path.join(tmp_path_factory.mktemp("data"), request.param)
    shutil.copy(os.path.join(SALT_PILLAR_DATADIR, request.param), temp_fpath)
    return temp_fpath


@pytest.fixture(scope="session")
def new_gnupg_homedir(tmp_path_factory: TempPathFactory) -> Path:
    temp_fpath = tmp_path_factory.mktemp("gnupg")
    gpg = gnupg.GPG(gnupghome=temp_fpath)
    gpg.gen_key_input(key_type="RSA", key_length=1024)
    return temp_fpath


def test_PartiallyEncryptedFile_find_encrypted_blocks(salt_pillar_fpath: str) -> None:
    gpg = gnupg.GPG(gnupghome=GNUPG_HOMEDIR)
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.find_encrypted_blocks()
    file.find_encrypted_blocks()


def test_PartiallyEncryptedFile_decrypt(salt_pillar_fpath: str) -> None:
    gpg = gnupg.GPG(gnupghome=GNUPG_HOMEDIR)
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.decrypt()
    file.decrypt()


def test_PartiallyEncryptedFile_decrypt_ValueError(
    salt_pillar_fpath: str, new_gnupg_homedir: str
) -> None:
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
        expectation = pytest.raises(ValueError)
    else:
        expectation = nullcontext()
    with expectation:
        file.decrypt()


def test_PartiallyEncryptedFile_encrypt(salt_pillar_fpath: str) -> None:
    gpg = gnupg.GPG(gnupghome=GNUPG_HOMEDIR)
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.encrypt()
    file.encrypt()


def test_PartiallyEncryptedFile_encrypt_ValueError_1(
    mocker: MockerFixture, salt_pillar_fpath: str
) -> None:
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
        expectation = pytest.raises(ValueError)
    else:
        expectation = nullcontext()
    with expectation:
        file.encrypt()


def test_PartiallyEncryptedFile_encrypt_ValueError_2(salt_pillar_fpath: str) -> None:
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
        expectation = pytest.raises(ValueError)
    else:
        expectation = nullcontext()
    with expectation:
        file.encrypt()


def test_PartiallyEncryptedFile_write_reencrypted_contents(
    salt_pillar_fpath: str,
) -> None:
    gpg = gnupg.GPG(gnupghome=GNUPG_HOMEDIR)
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.write_reencrypted_contents()
    file.write_reencrypted_contents()


def test_collect_file_paths(salt_pillar_fpath: str) -> None:
    collect_file_paths(salt_pillar_fpath)


def test_process_directory(mocker: MockerFixture, salt_pillar_fpath: str) -> None:
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
