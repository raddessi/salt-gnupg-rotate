# -*- coding: utf-8 -*-
"""Configuration."""

import os
import logging
from typing import (
    Mapping,
    Union,
)
from rich.console import Console

APP_NAME = "salt_gnupg_rotate"
ENV_APP_NAME = "SALT_GNUPG_ROTATE"
CONSOLE = Console(stderr=True)
DEFAULTS: Mapping[str, Union[str, int, None, bool]] = {
    "log_level": "info",
    "log_levels": list(map(str.lower, logging._nameToLevel.keys())) + ["trace"],  # pylint: disable=protected-access
    "decryption_gpg_homedir": os.path.expanduser("~/.gnupg"),
    "encryption_gpg_homedir": os.path.expanduser("~/.gnupg"),
}
