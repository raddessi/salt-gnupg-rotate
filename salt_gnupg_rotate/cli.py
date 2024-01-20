# -*- coding: utf-8 -*-
#
# Why does this file exist, and why not put this in `__main__`?
#
# You might be tempted to import things from `__main__` later,
# but that will cause problems: the code will get executed twice:
#
# - When you run `python -m salt_gnupg_rotate` python will execute
#   `__main__.py` as a script. That means there won't be any
#   `salt_gnupg_rotate.__main__` in `sys.modules`.
# - When you import `__main__` it will get executed again (as a module) because
#   there's no `salt_gnupg_rotate.__main__` in `sys.modules`.

"""CLI interactions."""
import logging

# pylint: disable=import-error
import click

from salt_gnupg_rotate import __version__
from salt_gnupg_rotate.config import (
    APP_NAME,
    DEFAULTS,
)
from salt_gnupg_rotate.logger import LOGGER
from salt_gnupg_rotate.main import main
from typing import (
    Union,
)


@click.command()
@click.option(
    "--decryption-gpg-homedir",
    default=DEFAULTS["decryption_gpg_homedir"],
    required=False,
    show_default=True,
)
@click.option(
    "--encryption-gpg-homedir",
    default=DEFAULTS["encryption_gpg_homedir"],
    required=False,
    show_default=True,
)
@click.option(
    "-r",
    "--recipient",
    required=True,
    type=click.STRING,
    show_default=True,
)
@click.option(
    "--dir",
    required=True,
    type=click.STRING,
    show_default=True,
)
@click.option(
    "-l",
    "--log-level",
    default=DEFAULTS["log_level"],
    type=click.Choice(choices=DEFAULTS["log_levels"], case_sensitive=False),
    show_default=True,
)
@click.version_option(version=__version__, package_name=APP_NAME)
@click.help_option("-h", "--help")
def cli(
    dir: str,
    decryption_gpg_homedir: str,
    encryption_gpg_homedir: str,
    recipient: str,
    log_level: Union[str, int, None]
) -> int:
    """Easily rotate gnupg encryption keys.
    \f
    Args:
        required_config_key: A key that is required but has no default value
        optional_config_key: A key that is required and has a default value
        log_level: The logging level name or integer to use.

    Returns:
        int: An exit code

    """
    try:
        main(
            dirpath=dir,
            decryption_gpg_homedir=decryption_gpg_homedir,
            encryption_gpg_homedir=encryption_gpg_homedir,
            recipient=recipient,
            log_level=log_level.upper() if isinstance(log_level, str) else log_level,
        )
    except NameError as err:
        LOGGER.critical(err)
        retcode = 1
    except Exception as err:
        LOGGER.critical(err)
        retcode = 9
    else:
        retcode = 0

    exit(retcode)
