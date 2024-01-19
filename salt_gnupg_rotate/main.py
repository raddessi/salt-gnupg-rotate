# -*- coding: utf-8 -*-
"""Main code."""
from typing import (
    Union,
)
import os

# pylint: disable=import-error
import rich
import rich.pretty
import rich.traceback

from salt_gnupg_rotate.config import (
    DEFAULTS,
)
from salt_gnupg_rotate.logger import LOGGER
from salt_gnupg_rotate.rotate import process_directory, DecryptionError

rich.pretty.install()
rich.traceback.install()



def main(
    required_config_key: Union[int, str, None, bool],
    dirpath: str,
    optional_config_key: Union[int, str, None, bool] = DEFAULTS.get(
        "optional_config_key", None
    ),
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
    logger = LOGGER
    LOGGER.setLevel(log_level)

    retcode = 0
    LOGGER.debug("starting up")
    # validation
    dirpath = os.path.realpath(dirpath)

    LOGGER.debug("required_config_key: %s", required_config_key)
    LOGGER.debug("dirpath=%s", dirpath)
    LOGGER.debug("log_level=%s", log_level)

    new_key_id = 'salt-master'
    import gnupg
    gpg = gnupg.GPG(homedir=os.path.expanduser("~/.gnupg"))
    try:
        process_directory(dirpath, gpg, new_key_id)
    except DecryptionError as err:
        LOGGER.error(err)
        retcode = 1
    else:
        LOGGER.warning("success! :rocket:", extra={"markup": True})

    return retcode
