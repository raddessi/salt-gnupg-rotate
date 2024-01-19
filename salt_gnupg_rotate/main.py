# -*- coding: utf-8 -*-
"""Main code."""
from typing import (
    Union,
)

# pylint: disable=import-error
import rich
import rich.pretty
import rich.traceback

from salt_gnupg_rotate.config import (
    DEFAULTS,
)
from salt_gnupg_rotate.logger import create_logger
from salt_gnupg_rotate.rotate import process_directory

rich.pretty.install()
rich.traceback.install()



def main(
    required_config_key: Union[int, str, None, bool],
    optional_config_key: Union[int, str, None, bool] = DEFAULTS.get(
        "optional_config_key", None
    ),
    dirpath: str = DEFAULTS.get("dirpath"),
    log_level: Union[int, str, None, bool] = DEFAULTS.get("log_level", None),
) -> int:
    """Main entrypoint.

    Args:
        required_config_key: A key that is required but has no default value
        optional_config_key: A key that is required and has a default value
        log_level: The logging level name or integer to use.

    Returns:
        int: An exit code

    """
    logger = create_logger(log_level=log_level)

    retcode = 0
    logger.debug("starting up")
    # perform any required startup actions here
    # directory = './pillar'
    new_key_id = 'salt-master'
    import gnupg
    import os
    gpg = gnupg.GPG(homedir=os.path.expanduser("~/.gnupg"))
    
    process_directory(dirpath, gpg, new_key_id)


    logger.debug("started OK :thumbsup:", extra={"markup": True})
    logger.debug("required_config_key: %s", required_config_key)
    logger.debug("optional_config_key: %s", optional_config_key)


    logger.debug("exiting")

    return retcode
