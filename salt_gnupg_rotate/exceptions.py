"""Custom exception classes."""


class DecryptionError(ValueError):
    """Error while trying to decrypt an encoded block of text."""


class EncryptionError(ValueError):
    """Error whilte trying to encrypt a block of text."""
