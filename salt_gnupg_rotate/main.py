"""Main code."""
from pathlib import Path

import gnupg
import rich
import rich.pretty
import rich.traceback

from salt_gnupg_rotate.config import (
    DECRYPTION_GPG_HOMEDIR,
    ENCRYPTION_GPG_HOMEDIR,
    LOG_LEVEL,
)
from salt_gnupg_rotate.exceptions import DecryptionError
from salt_gnupg_rotate.logger import LOGGER
from salt_gnupg_rotate.rotate import process_directory

rich.pretty.install()
rich.traceback.install()


def main(
    *,
    dirpath: str,
    recipient: str,
    decryption_gpg_homedir: str = DECRYPTION_GPG_HOMEDIR,
    encryption_gpg_homedir: str = ENCRYPTION_GPG_HOMEDIR,
    write: bool = False,
    log_level: str = LOG_LEVEL,
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
    dirpath = str(Path(dirpath).absolute())
    decryption_gpg_homedir = str(Path(decryption_gpg_homedir).expanduser().absolute())
    encryption_gpg_homedir = str(Path(encryption_gpg_homedir).expanduser().absolute())

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
            "Secret key for recipient '%s' found in keyring at %s :thumbs_up:",
            recipient,
            encryption_gpg_homedir,
            extra={"markup": True},
        )
    else:
        msg = (
            f"Secret key for recipient '{recipient}' not present in keyring at "
            f"{encryption_gpg_homedir}",
        )
        raise NameError(msg)

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
                "Success! Rotated encryption on blocks in %s files :rocket:",
                updated_count,
                extra={"markup": True},
            )
        else:
            LOGGER.info("Success! Pass '--write' to write out the changes")
