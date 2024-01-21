"""Tests for the `salt_gnupg_rotate.main` submodule."""

import gnupg
import os
import logging
import shutil
from contextlib import ExitStack as does_not_raise
from typing import Any, ContextManager, Union

import pytest

from salt_gnupg_rotate.exceptions import DecryptionError
from salt_gnupg_rotate.rotate import PartiallyEncryptedFile


SALT_PILLAR_DATADIR = "./tests/data/salt_pillar"
GNUPG_HOMEDIR = "./tests/data/gnupg"


def test_PartiallyEncryptedFile_instance(mocker):
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
    ],
)
def salt_pillar_fpath(tmp_path_factory, request):
    temp_fpath = os.path.join(tmp_path_factory.mktemp("data"), request.param)
    shutil.copy(os.path.join(SALT_PILLAR_DATADIR, request.param), temp_fpath)
    return temp_fpath


@pytest.fixture(scope="session")
def new_gnupg_homedir(tmp_path_factory):
    temp_fpath = tmp_path_factory.mktemp("gnupg")
    gpg = gnupg.GPG(gnupghome=temp_fpath)
    gpg.gen_key_input(key_type="RSA", key_length=1024)
    return temp_fpath


def test_PartiallyEncryptedFile_find_encrypted_blocks(salt_pillar_fpath):
    gpg = gnupg.GPG(gnupghome=GNUPG_HOMEDIR)
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.find_encrypted_blocks()
    file.find_encrypted_blocks()


def test_PartiallyEncryptedFile_decrypt(salt_pillar_fpath):
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
    salt_pillar_fpath, new_gnupg_homedir
):
    gpg = gnupg.GPG(gnupghome=new_gnupg_homedir)
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.find_encrypted_blocks()
    with pytest.raises(ValueError):
        file.decrypt()


def test_PartiallyEncryptedFile_encrypt(salt_pillar_fpath):
    gpg = gnupg.GPG(gnupghome=GNUPG_HOMEDIR)
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.encrypt()
    file.encrypt()


def test_PartiallyEncryptedFile_encrypt_ValueError_1(mocker, salt_pillar_fpath):
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
    with pytest.raises(ValueError):
        file.encrypt()


def test_PartiallyEncryptedFile_encrypt_ValueError_2(mocker, salt_pillar_fpath):
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
    with pytest.raises(ValueError):
        file.encrypt()


def test_PartiallyEncryptedFile_write_reencrypted_contents(salt_pillar_fpath):
    gpg = gnupg.GPG(gnupghome=GNUPG_HOMEDIR)
    file = PartiallyEncryptedFile(
        path=salt_pillar_fpath,
        decryption_gpg_keyring=gpg,
        encryption_gpg_keyring=gpg,
        recipient="pytest",
    )
    file.write_reencrypted_contents()


# def test_main_return_value(mocker):
#     mocked_process_directory = mocker.patch(
#         "salt_gnupg_rotate.main.process_directory",
#         return_value=2,
#     )
#     main(
#         dirpath="./tests/data/salt_pillar",
#         recipient="pytest",
#     )
#     mocked_process_directory.assert_called()


# def test_main_return_value_on_write(mocker):
#     mocked_process_directory = mocker.patch(
#         "salt_gnupg_rotate.main.process_directory",
#         return_value=2,
#     )
#     main(
#         dirpath="./tests/data/salt_pillar",
#         recipient="pytest",
#         write=True,
#     )
#     mocked_process_directory.assert_called()


# def test_main_gpg_keyring_missing_secret_key(mocker):
#     mocked_gpg = mocker.patch("salt_gnupg_rotate.main.gnupg.GPG")
#     mocked_gpg.side_effect = [
#         mocker.Mock(),
#         mocker.Mock(list_keys=mocker.Mock(return_value=[])),
#     ]
#     with pytest.raises(NameError):
#         main(
#             dirpath="./tests/data/salt_pillar",
#             recipient="pytest",
#         )


# def test_main_decryption_error(mocker):
#     mocked_process_directory = mocker.patch(
#         "salt_gnupg_rotate.main.process_directory",
#         side_effect=DecryptionError,
#     )
#     main(
#         dirpath="./tests/data/salt_pillar",
#         recipient="pytest",
#     )
#     mocked_process_directory.assert_called()
