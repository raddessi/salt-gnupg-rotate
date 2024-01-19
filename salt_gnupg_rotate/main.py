"""Main code."""
from typing import Union

# pylint: disable=import-error
import rich
import rich.pretty
import rich.traceback
from rich import print  # pylint: disable=redefined-builtin

from salt_gnupg_rotate.config import CONSOLE, DEFAULTS

rich.pretty.install()
rich.traceback.install()


def main(
    required_config_key: Union[int, str, None, bool],
    optional_config_key: Union[int, str, None, bool] = DEFAULTS.get(
        "optional_config_key", None
    ),
) -> int:
    """Main entrypoint.

    Args:
        required_config_key: A key that is required but has no default value
        optional_config_key: A key that is required and has a default value

    Returns:
        int: An exit code

    """

    retcode = 0
    print("[cyan]starting up")
    # perform any required startup actions here

    print("running!")
    CONSOLE.rule("[bold cyan]doing something!")
    print(f"required_config_key: {required_config_key}")
    print(f"optional_config_key: {optional_config_key}")

    print("[bold green]exiting")

    return retcode
