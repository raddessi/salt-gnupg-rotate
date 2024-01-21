"""Tests for the `salt_gnupg_rotate.main` submodule."""

import logging
from contextlib import ExitStack as does_not_raise
from typing import Any, ContextManager, Union

import pytest
# import rich.console

from salt_gnupg_rotate.main import main
from salt_gnupg_rotate.exceptions import DecryptionError



def test_main_return_value(mocker):
    mocked_process_directory = mocker.patch(
        "salt_gnupg_rotate.main.process_directory",
        return_value=2,
    )
    main(
        dirpath="./tests/data/salt_pillar",
        recipient="pytest",
    )
    mocked_process_directory.assert_called()


def test_main_return_value_on_write(mocker):
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

def test_main_gpg_keyring_missing_secret_key(mocker):
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

def test_main_decryption_error(mocker):
    mocked_process_directory = mocker.patch(
        "salt_gnupg_rotate.main.process_directory",
        side_effect=DecryptionError,
    )
    main(
        dirpath="./tests/data/salt_pillar",
        recipient="pytest",
    )
    mocked_process_directory.assert_called()

# @pytest.mark.parametrize(
#     "app_name,log_level,expectation,expected_log_level",
#     [
#         # pytest.param(
#         #     "mylogger",
#         #     None,
#         #     does_not_raise(),
#         #     "NOTSET",
#         #     id="defaults",
#         # ),
#         # pytest.param(
#         #     "mylogger",
#         #     "debug",
#         #     does_not_raise(),
#         #     "DEBUG",
#         #     id="log_level_debug_lowercase",
#         # ),
#         # pytest.param(
#         #     "mylogger",
#         #     "TRACE",
#         #     does_not_raise(),
#         #     "TRACE",
#         #     id="log_level_trace",
#         # ),
#         # pytest.param(
#         #     "mylogger",
#         #     "FOO",
#         #     pytest.raises(ValueError),
#         #     None,
#         #     id="invalid_log_level",
#         # ),
#     ],
# )
# def test_main(
#     mocker,
#     app_name: str,
#     log_level: Union[int, str],
#     expectation: ContextManager[Any],
#     expected_log_level: str,
# ) -> None:
#     """Verify that creating a logger works as expected.

#     Args:
#         child_name: The name of the child logger to set up, if a child is desired
#         reset_handlers: True if the existing handlers should be reset
#         log_level: The logging level to use
#         expectation: The context manager for the expected exception raising condition of
#             this test

#     """
#     mocked_process_directory = mocker.patch(
#         "salt_gnupg_rotate.cli.main",
#         return_value=2,
#         side_effect=exception,
#     )


#     # console = rich.console.Console(stderr=True)
#     with expectation:
#         main(
#             dirpath=dirpath,
#             recipient=recipient,
#             decryption_gpg_homedir=decryption_gpg_homedir,
#             encryption_gpg_homedir=encryption_gpg_homedir,
#             write=write,
#             log_level=log_level,
#         )

#         # assert isinstance(logger, logging.Logger)
#         # logger.trace("verify trace level logging works")
