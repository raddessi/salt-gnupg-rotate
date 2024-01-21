"""Rotation functions."""

import os
import re
from textwrap import dedent, indent

import gnupg
from rich import print
from rich.progress import track
from rich.markup import escape

from salt_gnupg_rotate.config import CONSOLE
from salt_gnupg_rotate.logger import LOGGER
from salt_gnupg_rotate.exceptions import EncryptionError, DecryptionError


class PartiallyEncryptedFile:
    encrypted_blocks = None
    logger = LOGGER
    decrypted_blocks = None

    def __init__(self, path, decryption_gpg_keyring, encryption_gpg_keyring, recipient):
        self.path = path
        self.decryption_gpg_keyring = decryption_gpg_keyring
        self.encryption_gpg_keyring = encryption_gpg_keyring
        self.recipient = recipient

        self.logger.info(f"Loading file {path}")
        with open(self.path) as self._fdesc:
            self.contents = self._fdesc.read()

    # TODO: change to getter
    def find_encrypted_blocks(self):
        if self.encrypted_blocks is not None:
            return self.encrypted_blocks

        pattern = r"\n?(\s*?-----BEGIN PGP MESSAGE-----.*?-----END PGP MESSAGE-----)"
        self.encrypted_blocks = re.findall(pattern, self.contents, re.DOTALL)

        self.logger.debug(
            f"Found {len(self.encrypted_blocks)} encrypted blocks in file {self.path}"
        )
        total_count = len(self.encrypted_blocks)
        for count, encrypted_block in enumerate(self.encrypted_blocks, start=1):
            self.logger.trace(f"Block {count} of {total_count} in file {self.path} before decryption:\n{escape(encrypted_block)}")

        return self.encrypted_blocks

    def decrypt(self):
        if self.encrypted_blocks is None:
            self.find_encrypted_blocks()

        decrypted_blocks = []
        total_count = len(self.encrypted_blocks)
        for count, encrypted_block in enumerate(self.encrypted_blocks, start=1):
            self.logger.debug(f"Decrypting block {count} of {total_count} in file {self.path}")
            line_length_before = max(len(line) for line in encrypted_block.splitlines())
            line_length_after = max(len(line.lstrip()) for line in encrypted_block.splitlines())
            padding_size = line_length_before - line_length_after

            encrypted_block = dedent(encrypted_block)
            decrypted_block = self.decryption_gpg_keyring.decrypt(
                encrypted_block, passphrase=None, always_trust=True
            )

            if not decrypted_block.ok:
                raise ValueError(f"Failed to decrypt block in {self.path}: {decrypted_block.problems[0]['status']}")

            self.logger.trace(f"Block after decryption (some characters may not be printable):\n{escape(decrypted_block.data.decode())}")
            decrypted_blocks.append((encrypted_block, decrypted_block, padding_size))
            
        self.decrypted_blocks = decrypted_blocks


    def encrypt(self):
        if self.decrypted_blocks is None:
            self.decrypt()
            
        new_contents = self.contents
        total_count = len(self.decrypted_blocks)
        for count, (encrypted_block, decrypted_block, padding_size) in enumerate(self.decrypted_blocks, start=1):
            reencrypted_data = self.encryption_gpg_keyring.encrypt(
                str(decrypted_block), self.recipient, always_trust=True
            )

            if not reencrypted_data.ok:
                self.logger.error(f"Failed to encrypt block in {self.path}")
                return False

            if padding_size:
                reencrypted_data = indent(str(reencrypted_data), " " * padding_size)
            else:
                reencrypted_data = str(reencrypted_data)

            self.logger.trace(f"Block {count} of {total_count} in file {self.path} after decryption:\n{escape(reencrypted_data)}")
            new_contents = new_contents.replace(encrypted_block, reencrypted_data)
        
        self.logger.trace(f"Proposed contents of file {self.path} after re-encryption:\n{new_contents}")

        # file.seek(0)
        # file.write(content)
        # file.truncate()


def collect_file_paths(dirpath):
    fpaths = []
    for root, dirs, files in os.walk(dirpath):
        for name in files:
            if name.rsplit(".", 1)[-1] not in ["sls", "gpg"]:
                continue
            file_path = os.path.join(root, name)
            fpaths.append(file_path)

    return fpaths


def process_directory(
    dirpath,
    decryption_gpg_keyring,
    encryption_gpg_keyring,
    recipient,
    write=False,
    logger=LOGGER,
):
    files = []
    fpaths = collect_file_paths(dirpath=dirpath)

    logger.info(f"Opening files in directory {dirpath} ...")
    for fpath in track(fpaths, description="Opening files...", console=CONSOLE):
        file = PartiallyEncryptedFile(
            path=fpath,
            decryption_gpg_keyring=decryption_gpg_keyring,
            encryption_gpg_keyring=encryption_gpg_keyring,
            recipient=recipient,
        )
        file.find_encrypted_blocks()
        files.append(file)

    decryption_success = True
    logger.info("Decrypting blocks in the loaded files ...")
    for file in track(files, description="Decrypting...", console=CONSOLE):
        try:
            file.decrypt()
        except Exception as err:
            logger.error(err)
            decryption_success = False
    if not decryption_success:
        raise DecryptionError("Bailing due to decryption errors")
    
    reencryption_success = True
    logger.info("Re-encrypting blocks in the loaded files ...")
    for file in track(files, description="Re-encrypting...", console=CONSOLE):
        try:
            file.encrypt()
        except Exception as err:
            logger.error(err)
            reencryption_success = False
    if not reencryption_success:
        raise EncryptionError("Bailing due to re-encryption errors")

    if write:
        logger.info("Writing out changes ...")
    else:
        logger.info("Skipping writing out changes")
    

