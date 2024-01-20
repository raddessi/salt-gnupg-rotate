"""Tests for the `config` module."""


from salt_gnupg_rotate.config import DEFAULTS


def test_defaults() -> None:
    """Dummy test for the defaults, nothing to test at the moment."""
    assert isinstance(DEFAULTS, dict)
