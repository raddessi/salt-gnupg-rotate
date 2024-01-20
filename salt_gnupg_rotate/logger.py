"""Logging setup."""

from salt_gnupg_rotate.config import APP_NAME, CONSOLE, DEFAULTS
from salt_gnupg_rotate.logging_mixins import create_logger

LOGGER = create_logger(
    app_name=APP_NAME,
    log_level=DEFAULTS["log_level"],
    console=CONSOLE,
)
