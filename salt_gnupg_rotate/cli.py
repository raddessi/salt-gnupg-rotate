#
# Why does this file exist, and why not put this in `__main__`?
#
# You might be tempted to import things from `__main__` later,
# but that will cause problems: the code will get executed twice:
#
# - When you run `python -m salt_gnupg_rotate` python will execute
#   `__main__.py` as a script. That means there won't be any
#   `salt_gnupg_rotate.__main__` in `sys.modules`.
# - When you import `__main__` it will get executed again (as a module) because
#   there's no `salt_gnupg_rotate.__main__` in `sys.modules`.

"""CLI interactions."""
import sys

import click

from salt_gnupg_rotate import __version__
from salt_gnupg_rotate.config import (
    APP_NAME,
    DECRYPTION_GPG_HOMEDIR,
    ENCRYPTION_GPG_HOMEDIR,
    LOG_LEVEL,
    LOG_LEVELS,
)
from salt_gnupg_rotate.exceptions import DecryptionError, EncryptionError
from salt_gnupg_rotate.logger import LOGGER
from salt_gnupg_rotate.main import main


@click.command(
    help="Easily rotate gnupg encryption keys of fully or partially encrypted files.",
)
@click.option(
    "-d",
    "--dir",
    "--directory",
    "directory",
    required=True,
    type=click.STRING,
    show_default=True,
    help=(
        "The directory of encrypted data to recursively re-encrypt encrypted blocks "
        "within."
    ),
)
@click.option(
    "--decryption-gpg-homedir",
    default=DECRYPTION_GPG_HOMEDIR,
    required=False,
    show_default=True,
    help=(
        "The path of the directory of the gnupg keyring that should be used for "
        "decryption."
    ),
)
@click.option(
    "--encryption-gpg-homedir",
    default=ENCRYPTION_GPG_HOMEDIR,
    required=False,
    show_default=True,
    help=(
        "The path of the directory of the gnupg keyring that should be used for "
        "encryption."
    ),
)
@click.option(
    "-r",
    "--recipient",
    required=True,
    type=click.STRING,
    show_default=True,
    help="The name of the recipient key to use in the encryption keyring.",
)
@click.option(
    "--write",
    is_flag=True,
    default=False,
    required=False,
    show_default=True,
    help=(
        "Write the re-encrypted data back out to disk. If not passed then no changes "
        "will be made."
    ),
)
@click.option(
    "-l",
    "--log",
    "--log-level",
    "log_level",
    default=LOG_LEVEL,
    type=click.Choice(choices=LOG_LEVELS, case_sensitive=False),
    show_default=True,
    help="The logging verbosity level to use",
)
@click.version_option(version=__version__, package_name=APP_NAME)
@click.help_option("-h", "--help")
def cli(
    directory: str,
    decryption_gpg_homedir: str,
    encryption_gpg_homedir: str,
    recipient: str,
    log_level: str,
    *,
    write: bool,
) -> int:
    r"""Easily rotate gnupg encryption keys of fully or partially encrypted files.

    \f

    Args:
        directory: The directory path to search for files within that should be
            re-encrypted
        recipient: The recipient name of the gpg key in the encryption keyring to use
        decryption_gpg_homedir: The directory path of the gnupg keyring to use for
            decryption
        encryption_gpg_homedir: The directory path of the gnupg keyring to use for
            encryption
        recipient: The recipient name of the gpg key in the encryption keyring to use
        log_level: The logging level name or integer to use.
        write: If True, write out the changes to disk. If False, only check that
            re-encryption succeeds in memory and make no changes to disk

    """
    try:
        main(
            dirpath=directory,
            decryption_gpg_homedir=decryption_gpg_homedir,
            encryption_gpg_homedir=encryption_gpg_homedir,
            recipient=recipient,
            write=write,
            log_level=log_level.upper(),
        )

    except NameError as err:
        LOGGER.critical(err)
        retcode = 1

    except DecryptionError as err:
        LOGGER.critical(err)
        retcode = 2

    except EncryptionError as err:
        LOGGER.critical(err)
        retcode = 3

    except Exception as err:  # noqa: BLE001
        LOGGER.exception(err)
        retcode = 9

    else:
        retcode = 0

    sys.exit(retcode)
