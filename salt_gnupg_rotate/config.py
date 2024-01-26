"""Configuration."""

import os
from typing import Mapping, Union, List

from rich.console import Console

from salt_gnupg_rotate.logging_mixins import logging

APP_NAME = "salt_gnupg_rotate"
ENV_APP_NAME = "SALT_GNUPG_ROTATE"
CONSOLE = Console(stderr=True)
LOG_LEVEL: str = "info"
LOG_LEVELS: List[str] = list(
    map(
        str.lower,
        [
            level_name
            for level, level_name in sorted(
                logging._levelToName.items(), reverse=True
            )
        ],
    )
)  # pylint: disable=protected-access
DECRYPTION_GPG_HOMEDIR: str = os.path.expanduser("~/.gnupg")
ENCRYPTION_GPG_HOMEDIR: str = os.path.expanduser("~/.gnupg")
