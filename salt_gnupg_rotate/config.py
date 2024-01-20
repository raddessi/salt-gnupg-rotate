"""Configuration."""

import os
from typing import Mapping, Union

from rich.console import Console

from salt_gnupg_rotate.logging_mixins import logging

APP_NAME = "salt_gnupg_rotate"
ENV_APP_NAME = "SALT_GNUPG_ROTATE"
CONSOLE = Console(stderr=True)
DEFAULTS: Mapping[str, Union[str, int, None, bool]] = {
    "log_level": "info",
    "log_levels": list(
        map(
            str.lower,
            [
                level_name
                for level, level_name in sorted(
                    logging._levelToName.items(), reverse=True
                )
            ],
        )
    ),  # pylint: disable=protected-access
    "decryption_gpg_homedir": os.path.expanduser("~/.gnupg"),
    "encryption_gpg_homedir": os.path.expanduser("~/.gnupg"),
}
