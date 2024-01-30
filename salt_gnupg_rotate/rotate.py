"""Rotation functions."""

import os
import re
from pathlib import Path
from textwrap import dedent, indent

from gnupg import GPG
from rich.markup import escape
from rich.progress import track

from salt_gnupg_rotate.config import CONSOLE
from salt_gnupg_rotate.exceptions import DecryptionError, EncryptionError
from salt_gnupg_rotate.logger import LOGGER
from salt_gnupg_rotate.logging_mixins import CustomLogger


class PartiallyEncryptedFile:
    """A file that is either partially or fully encrypted."""

    encrypted_blocks = None
    logger = LOGGER
    decrypted_blocks = None
    reencrypted_contents = None

    def __init__(
        self,
        path: str,
        decryption_gpg_keyring: GPG,
        encryption_gpg_keyring: GPG,
        recipient: str,
    ) -> None:
        """Constructor.

        Args:
            path: The path to the file
            decryption_gpg_keyring: The keyring that should be used to decrypt the file
            encryption_gpg_keyring: The keyring that should be used to encrypt the file
            recipient: The name of the recipient of the key in the
                encryption_gpg_keyring that the data should be re-encrypted for

        """
        self.path = path
        self.decryption_gpg_keyring = decryption_gpg_keyring
        self.encryption_gpg_keyring = encryption_gpg_keyring
        self.recipient = recipient

        self.logger.info("Loading file %s", path)
        with Path(self.path).open("r") as fdesc:
            self.contents = fdesc.read()

    def find_encrypted_blocks(self) -> None:
        """Find any encrypted blocks within the file."""
        pattern = r"\n?(\s*?-----BEGIN PGP MESSAGE-----.*?-----END PGP MESSAGE-----)"
        self.encrypted_blocks = re.findall(pattern, self.contents, re.DOTALL)

        self.logger.debug(
            "Found %s encrypted blocks in file %s",
            len(self.encrypted_blocks),
            self.path,
        )
        total_count = len(self.encrypted_blocks)
        for count, encrypted_block in enumerate(self.encrypted_blocks, start=1):
            self.logger.trace(
                "Block %s of %s in file %s before decryption:\n%s",
                count,
                total_count,
                self.path,
                escape(encrypted_block),
            )

    def decrypt(self) -> None:
        """Decrypt any encrypted blocks in the file.

        Raises:
            DecryptionError: If there was an error during decryption
            ValueError: If there was an error finding the encrypted blocks

        """
        if self.encrypted_blocks is None:
            self.find_encrypted_blocks()

        if not isinstance(self.encrypted_blocks, list):
            msg = "expected to find encrypted blocks but found none"
            raise ValueError(msg)  # noqa: TRY004

        decrypted_blocks = []
        total_count = len(self.encrypted_blocks)
        for count, encrypted_block in enumerate(self.encrypted_blocks, start=1):
            self.logger.debug(
                "Decrypting block %s of %s in file %s",
                count,
                total_count,
                self.path,
            )
            line_length_before = max(len(line) for line in encrypted_block.splitlines())
            line_length_after = max(
                len(line.lstrip()) for line in encrypted_block.splitlines()
            )
            padding_size = line_length_before - line_length_after

            encrypted_stripped_block = dedent(encrypted_block)
            decrypted_block = self.decryption_gpg_keyring.decrypt(
                encrypted_stripped_block,
                passphrase=None,
                always_trust=True,
            )

            if not decrypted_block.ok:
                msg = (
                    f"Failed to decrypt block in {self.path}: "
                    f"{decrypted_block.problems[0]['status']}"
                )
                raise DecryptionError(msg)

            self.logger.trace(
                "Block after decryption (some characters may not be printable):\n%s",
                escape(decrypted_block.data.decode()),
            )
            decrypted_blocks.append(
                (
                    encrypted_block,
                    encrypted_stripped_block,
                    decrypted_block,
                    padding_size,
                ),
            )

        self.decrypted_blocks = decrypted_blocks

    def encrypt(self) -> None:
        """Re-encrypt the decrypted blocks from the file.

        Raises:
            EncryptionError: If there was an error during encryption
            ValueError: If there was an error finding the decrypted blocks

        """
        if self.decrypted_blocks is None:
            self.decrypt()

        if not isinstance(self.decrypted_blocks, list):
            msg = "expected to find decrypted blocks but found none"
            raise ValueError(msg)  # noqa: TRY004

        new_contents = self.contents
        total_count = len(self.decrypted_blocks)
        for count, (
            encrypted_block,
            _,
            decrypted_block,
            padding_size,
        ) in enumerate(self.decrypted_blocks, start=1):
            reencrypted_data = self.encryption_gpg_keyring.encrypt(
                str(decrypted_block),
                self.recipient,
                always_trust=True,
            )

            if not reencrypted_data.ok:
                msg = (
                    f"Failed to encrypt block in {self.path}: "
                    f"{reencrypted_data.problems[0]['status']}"
                )
                raise EncryptionError(msg)

            if padding_size:
                reencrypted_padded_block = indent(
                    str(reencrypted_data),
                    " " * padding_size,
                )
            else:
                reencrypted_padded_block = str(reencrypted_data)

            self.logger.debug(
                "Re-encrypted block %s of %s in file %s",
                count,
                total_count,
                self.path,
            )
            self.logger.trace(
                "Block %s of %s in file %s after re-encryption:\n%s",
                count,
                total_count,
                self.path,
                escape(reencrypted_padded_block),
            )

            proposed_change = new_contents.replace(
                encrypted_block,
                reencrypted_padded_block,
                1,
            )
            # check if nothing was changed incorrectly
            if proposed_change == new_contents:
                msg = (
                    f"Attempt to replace block {count} of {total_count} in file "
                    f"{self.path} failed"
                )
                raise EncryptionError(msg)
            new_contents = proposed_change

        self.logger.trace(
            f"Proposed contents of file {self.path} after re-encryption:\n"
            f"{new_contents}",
        )

        self.reencrypted_contents = new_contents

    def write_reencrypted_contents(self) -> None:
        """Write the file back to disk after re-encrypting any encrypted blocks."""
        if self.reencrypted_contents is None:
            self.encrypt()

        if isinstance(self.reencrypted_contents, str):
            self.logger.debug("Writing updated file %s", self.path)
            with Path(self.path).open("w") as fdesc:
                fdesc.seek(0)
                fdesc.write(self.reencrypted_contents)
                fdesc.truncate()


def collect_file_paths(dirpath: str) -> list[str]:
    """Find any supported files that we should search for encrypted blocks in.

    Args:
        dirpath: The directory path to search for files within

    Returns:
        list: Of str file paths
    """
    fpaths = []
    for root, _, files in os.walk(dirpath):
        for name in files:
            if name.rsplit(".", 1)[-1] not in ["sls", "gpg"]:
                continue
            file_path = Path(root) / name
            fpaths.append(str(file_path))

    return fpaths


def process_directory(
    *,
    dirpath: str,
    decryption_gpg_keyring: GPG,
    encryption_gpg_keyring: GPG,
    recipient: str,
    write: bool = False,
    logger: CustomLogger = LOGGER,
) -> int:
    """Recursively search for and re-encrypt encrypted blocks in files.

    Args:
        dirpath: The directory path to search for files within that should be
            re-encrypted
        decryption_gpg_keyring: The gnupg keyring to use for decryption
        encryption_gpg_keyring: The gnupg keyring to use for encryption
        recipient: The recipient name of the gpg key in the encryption keyring to use
        write: If True, write out the changes to disk. If False, only check that
            re-encryption succeeds in memory and make no changes to disk
        logger: The logger instance to use

    Returns:
        int: The number of files that were or would have been updated

    Raises:
        DecryptionError: If there was an error decrypting data
        EncryptionError: If there was an error encrypting data
    """
    files = []
    fpaths = collect_file_paths(dirpath=dirpath)

    logger.info("Loading files in directory %s ...", dirpath)
    for fpath in track(fpaths, description="Loading files...", console=CONSOLE):
        file = PartiallyEncryptedFile(
            path=fpath,
            decryption_gpg_keyring=decryption_gpg_keyring,
            encryption_gpg_keyring=encryption_gpg_keyring,
            recipient=recipient,
        )
        file.find_encrypted_blocks()
        files.append(file)

    logger.info("Decrypting blocks in the loaded files ...")
    try:
        for file in track(files, description="Decrypting...", console=CONSOLE):
            file.decrypt()
    except Exception as err:
        logger.exception("Error during decryption")
        msg = "Bailing due to an error during decryption"
        raise DecryptionError(msg) from err

    logger.info("Re-encrypting blocks in the loaded files ...")
    try:
        for file in track(files, description="Re-encrypting...", console=CONSOLE):
            file.encrypt()
    except Exception as err:
        logger.exception("Error while re-encrypting blocks")
        msg = "Bailing due to an error during re-encryption"
        raise EncryptionError(msg) from err

    if write:
        logger.info("Writing out changes ...")
        try:
            for file in track(files, description="Writing...", console=CONSOLE):
                file.write_reencrypted_contents()
        except Exception as err:
            logger.exception("Error while writing updated contents")
            msg = "Bailing due to an error while writing the updated contents"
            raise EncryptionError(msg) from err
    else:
        logger.info("Skipping writing out changes")

    return len(files)
