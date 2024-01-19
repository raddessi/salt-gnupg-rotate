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

from typing import Union

# pylint: disable=import-error
import click

from salt_gnupg_rotate import __version__
from salt_gnupg_rotate.config import APP_NAME
from salt_gnupg_rotate.main import main


@click.command()
@click.option(
    "--required-config-key",
    required=True,
    show_default=True,
)
@click.option(
    "--optional-config-key",
    default="foo",
    required=False,
    show_default=True,
)
@click.version_option(version=__version__, package_name=APP_NAME)
@click.help_option("-h", "--help")
def cli(
    required_config_key: Union[str, int, bool, None],
    optional_config_key: Union[str, int, bool, None],
) -> int:
    """Easily rotate gnupg encryption keys.
    \f
    Args:
        required_config_key: A key that is required but has no default value
        optional_config_key: A key that is required and has a default value

    Returns:
        int: An exit code

    """
    main(
        required_config_key=required_config_key,
        optional_config_key=optional_config_key,
    )

    return 0
