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
    log_level: Union[int, str, None, bool] = DEFAULTS["log_level"],
) -> int:
    """Main entrypoint.

    Args:
        required_config_key: A key that is required but has no default value
        optional_config_key: A key that is required and has a default value
        log_level: The logging level name or integer to use.

    Returns:
        int: An exit code

    """
    LOGGER.setLevel(log_level)
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
        process_directory(
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
            LOGGER.info("Success! :rocket:", extra={"markup": True})
        else:
            LOGGER.info("Success! Pass '--write' to write out the changes")
