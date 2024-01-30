"""Configuration."""

import os

from rich.console import Console

from salt_gnupg_rotate.logging_mixins import logging  # type: ignore[attr-defined]

APP_NAME = "salt_gnupg_rotate"
ENV_APP_NAME = "SALT_GNUPG_ROTATE"
CONSOLE = Console(stderr=True)
LOG_LEVEL: str = "info"
LOG_LEVELS: list[str] = list(
    map(
        str.lower,
        [
            level_name
            for _, level_name in sorted(logging._levelToName.items(), reverse=True)  # noqa: SLF001
        ],
    ),
)
DECRYPTION_GPG_HOMEDIR: str = os.getenv("GNUPGHOME", "~/.gnupg")
ENCRYPTION_GPG_HOMEDIR: str = os.getenv("GNUPGHOME", "~/.gnupg")
