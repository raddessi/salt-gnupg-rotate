"""Configuration."""

from __future__ import annotations

import os

from rich.console import Console
from rich.theme import Theme

from salt_gnupg_rotate.logging_mixins import logging  # type: ignore[attr-defined]

APP_NAME = "salt_gnupg_rotate"
ENV_APP_NAME = "SALT_GNUPG_ROTATE"
CONSOLE = Console(stderr=True, theme=Theme({"logging.level.trace": "hot_pink"}))
LOG_LEVEL: str = "info"
LOG_LEVELS: list[str] = [
    str(level_name).lower()
    for _, level_name in sorted(
        getattr(logging, "_levelToName", {}).items(),
        reverse=True,
    )
]
DECRYPTION_GPG_HOMEDIR: str = os.getenv("GNUPGHOME", "~/.gnupg")
ENCRYPTION_GPG_HOMEDIR: str = os.getenv("GNUPGHOME", "~/.gnupg")
