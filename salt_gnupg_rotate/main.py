"""Main code."""
import os
from typing import Union

# pylint: disable=import-error
import gnupg
import rich
import rich.pretty
import rich.traceback

from salt_gnupg_rotate.config import DEFAULTS
from salt_gnupg_rotate.logger import LOGGER
from salt_gnupg_rotate.rotate import DecryptionError, process_directory

rich.pretty.install()
rich.traceback.install()


def main(
    dirpath: str,
    recipient: str,
    decryption_gpg_homedir: Union[int, str, None, bool] = DEFAULTS.get(
        "decryption_gpg_homedir", None
    ),
    encryption_gpg_homedir: Union[int, str, None, bool] = DEFAULTS.get(
        "encryption_gpg_homedir", None
    ),
    write: bool = False,
    log_level: Union[int, str, bool] = DEFAULTS["log_level"],
) -> None:
    """Main entrypoint.

    Args:
        dirpath: The directory path to search for files within that should be
            re-encrypted
        recipient: The recipient name of the gpg key in the encryption keyring to use
        decryption_gpg_homedir: The directory path of the gnupg keyring to use for
            decryption
        encryption_gpg_homedir: The directory path of the gnupg keyring to use for
            encryption
        write: If True, write out the changes to disk. If False, only check that
            re-encryption succeeds in memory and make no changes to disk
        log_level: The logging level name or integer to use.

    Raises:
        NameError: If the named recipient key is not found in the encryption keyring

    """
    LOGGER.setLevel(log_level.upper())
    LOGGER.debug("Starting up")

    # validation
    dirpath = os.path.realpath(dirpath)
    decryption_gpg_homedir = os.path.realpath(decryption_gpg_homedir)
    encryption_gpg_homedir = os.path.realpath(encryption_gpg_homedir)

    LOGGER.debug("dirpath=%s", dirpath)
    LOGGER.debug("decryption_gpg_homedir=%s", decryption_gpg_homedir)
    LOGGER.debug("encryption_gpg_homedir=%s", encryption_gpg_homedir)
    LOGGER.debug("recipient=%s", recipient)
    LOGGER.debug("log_level=%s", log_level)

    decryption_gpg_keyring = gnupg.GPG(
        gnupghome=decryption_gpg_homedir,
    )

    encryption_gpg_keyring = gnupg.GPG(
        gnupghome=encryption_gpg_homedir,
    )

    # check the recipient secret key exists
    if encryption_gpg_keyring.list_keys(secret=True, keys=recipient):
        LOGGER.debug(
            f"Secret key for recipient '{recipient}' found in keyring at "
            f"{encryption_gpg_homedir} :thumbs_up:",
            extra={"markup": True},
        )
    else:
        raise NameError(
            f"Secret key for recipient '{recipient}' not present in keyring at "
            f"{encryption_gpg_homedir}"
        )

    try:
        updated_count = process_directory(
            dirpath=dirpath,
            decryption_gpg_keyring=decryption_gpg_keyring,
            encryption_gpg_keyring=encryption_gpg_keyring,
            recipient=recipient,
            write=write,
        )
    except DecryptionError as err:
        LOGGER.error(err)
    else:
        if write:
            LOGGER.info(
                f"Success! Rotated encryption on blocks in {updated_count} files "
                ":rocket:",
                extra={"markup": True},
            )
        else:
            LOGGER.info("Success! Pass '--write' to write out the changes")
