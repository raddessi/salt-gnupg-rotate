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


class PartiallyEncryptedFile(object):
    encrypted_blocks = None
    logger = LOGGER

    def __init__(self, path):
        self.path = path

        self.logger.debug(f"opening file {path}")
        with open(self.path, 'r') as self._fdesc:
            self.contents = self._fdesc.read()

    # TODO: change to getter
    def find_encrypted_blocks(self):
        if self.encrypted_blocks is not None:
            return self.encrypted_blocks

        pattern = r"\n?(\s*?-----BEGIN PGP MESSAGE-----.*?-----END PGP MESSAGE-----)"
        self.encrypted_blocks = re.findall(pattern, self.contents, re.DOTALL)

        return self.encrypted_blocks

    def decrypt(self, new_key_id, gpg):
        for block in self.find_encrypted_blocks():
            line_length_before = max((len(line) for line in block.splitlines()))
            line_length_after = max((len(line.lstrip()) for line in block.splitlines()))
            padding_size = line_length_before - line_length_after


            self.logger.debug(f"block before (padding size {padding_size}):\n{block}")

            block = dedent(block)
            decrypted_data = gpg.decrypt(block, passphrase=None, always_trust=True)

            if not decrypted_data.ok:
                self.logger.error(f"Failed to decrypt block in {self.path}")
                continue

            encrypted_data = gpg.encrypt(str(decrypted_data), new_key_id, always_trust=True)

            if not encrypted_data.ok:
                self.logger.error(f"Failed to encrypt block in {self.path}")
                continue

            if padding_size:
                encrypted_data = indent(str(encrypted_data), " " * padding_size)
            else:
                encrypted_data = str(encrypted_data)

            self.logger.debug(f"block after:\n{encrypted_data}")
            content = content.replace(block, encrypted_data)
            # print(f"content after:\n{content}")

        # file.seek(0)
        # file.write(content)
        # file.truncate()

    def find_pgp_blocks(text):
        pattern = r"\n?(\s*?-----BEGIN PGP MESSAGE-----.*?-----END PGP MESSAGE-----)"
        return re.findall(pattern, text, re.DOTALL)


def process_file(file_path, gpg, new_key_id, logger=LOGGER):

    file = PartiallyEncryptedFile(path=file_path)
    file.decrypt(new_key_id=new_key_id, gpg=gpg)

    # logger.debug(f"file: {file_path}")

    # with open(file_path, 'r+') as file:
    #     content = file.read()
    #     pgp_blocks = find_pgp_blocks(content)
    #     # print(f"content before:\n{content}")

    #     # for block in pgp_blocks:
    #     #     line_length_before = max((len(line) for line in block.splitlines()))
    #     #     line_length_after = max((len(line.lstrip()) for line in block.splitlines()))
    #     #     padding_size = line_length_before - line_length_after


    #     #     logger.debug(f"block before (padding size {padding_size}):\n{block}")

    #     #     block = dedent(block)
    #     #     decrypted_data = gpg.decrypt(block, passphrase=None, always_trust=True)

    #     #     if not decrypted_data.ok:
    #     #         logger.error(f"Failed to decrypt block in {file_path}")
    #     #         continue

    #     #     encrypted_data = gpg.encrypt(str(decrypted_data), new_key_id, always_trust=True)

    #     #     if not encrypted_data.ok:
    #     #         logger.error(f"Failed to encrypt block in {file_path}")
    #     #         continue

    #     #     if padding_size:
    #     #         encrypted_data = indent(str(encrypted_data), " " * padding_size)
    #     #     else:
    #     #         encrypted_data = str(encrypted_data)

    #     #     logger.debug(f"block after:\n{encrypted_data}")
    #     #     content = content.replace(block, encrypted_data)
    #     #     # print(f"content after:\n{content}")

    #     # # file.seek(0)
    #     # # file.write(content)
    #     # # file.truncate()
            
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
    logger.debug(f'{{"dir": "{directory}"}}')

    fpaths = collect_file_paths(directory=directory)
    for fpath in track(fpaths, description="Processing...", console=CONSOLE):
        process_file(fpath, gpg, new_key_id, logger=logger)
