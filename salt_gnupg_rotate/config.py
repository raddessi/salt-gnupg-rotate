# -*- coding: utf-8 -*-
"""Configuration."""

import os
from typing import (
    Mapping,
    Union,
)
from rich.console import Console


APP_NAME = "salt_gnupg_rotate"
ENV_APP_NAME = "SALT_GNUPG_ROTATE"
CONSOLE = Console(stderr=True)
DEFAULTS: Mapping[str, Union[str, int, None, bool]] = {
    "log_level": "INFO",
    "dirpath": os.getcwd(),
}
