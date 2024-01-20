# -*- coding: utf-8 -*-
"""Rotation functions."""

import os
import re

import gnupg
from textwrap import indent, dedent
from rich import print
from rich.progress import track

from salt_gnupg_rotate.logger import LOGGER
from salt_gnupg_rotate.config import CONSOLE


def find_pgp_blocks(text):
    pattern = r"\n?(\s*?-----BEGIN PGP MESSAGE-----.*?-----END PGP MESSAGE-----)"
    return re.findall(pattern, text, re.DOTALL)

class DecryptionError(ValueError):
    pass


class PartiallyEncryptedFile(object):
    encrypted_blocks = None
    logger = LOGGER

    def __init__(self, path):
        self.path = path

        self.logger.info(f"Loading file {path}")
        with open(self.path, 'r') as self._fdesc:
            self.contents = self._fdesc.read()

    # TODO: change to getter
    def find_encrypted_blocks(self):
        if self.encrypted_blocks is not None:
            return self.encrypted_blocks

        pattern = r"\n?(\s*?-----BEGIN PGP MESSAGE-----.*?-----END PGP MESSAGE-----)"
        self.encrypted_blocks = re.findall(pattern, self.contents, re.DOTALL)

        self.logger.debug(f"Found {len(self.encrypted_blocks)} encrypted blocks in file {self.path}")

        return self.encrypted_blocks

    def decrypt(self, new_key_id, gpg):

        success = True
        for block in self.find_encrypted_blocks():
            line_length_before = max((len(line) for line in block.splitlines()))
            line_length_after = max((len(line.lstrip()) for line in block.splitlines()))
            padding_size = line_length_before - line_length_after


            self.logger.trace(f"block before (padding size {padding_size}):\n{block}")

            block = dedent(block)
            decrypted_data = gpg.decrypt(block, passphrase=None, always_trust=True)
            # print(decrypted_data.__dict__)

            if not decrypted_data.ok:
                self.logger.error(f"Failed to decrypt block in {self.path}")
                return False

            encrypted_data = gpg.encrypt(str(decrypted_data), new_key_id, always_trust=True)

            if not encrypted_data.ok:
                self.logger.error(f"Failed to encrypt block in {self.path}")
                return False

            if padding_size:
                encrypted_data = indent(str(encrypted_data), " " * padding_size)
            else:
                encrypted_data = str(encrypted_data)

            self.logger.trace(f"block after:\n{encrypted_data}")
            content = self.contents.replace(block, encrypted_data)
            # print(f"content after:\n{content}")

        # file.seek(0)
        # file.write(content)
        # file.truncate()
        return success

    def find_pgp_blocks(text):
        pattern = r"\n?(\s*?-----BEGIN PGP MESSAGE-----.*?-----END PGP MESSAGE-----)"
        return re.findall(pattern, text, re.DOTALL)

def collect_file_paths(directory):
    fpaths = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.rsplit(".", 1)[-1] not in ["sls", "gpg"]:
                continue
            file_path = os.path.join(root, name)
            fpaths.append(file_path)
    
    return fpaths

def process_directory(directory, gpg, new_key_id, logger=LOGGER):
    files = []
    fpaths = collect_file_paths(directory=directory)

    logger.debug(f"Opening files in directory {directory} ...")
    for fpath in track(fpaths, description="Opening files...", console=CONSOLE):
        file = PartiallyEncryptedFile(path=fpath)
        files.append(file)

    decryption_success = True
    logger.debug("Decrypting the loaded files ...")
    for file in track(files, description="Decrypting...", console=CONSOLE):
        success = file.decrypt(new_key_id=new_key_id, gpg=gpg)
        if not success:
            decryption_success = False
    if not decryption_success:
        raise DecryptionError("Not continuing due to decryption errors")
