"""Rotation functions."""

import os
import re
import gnupg
from textwrap import indent, dedent
from rich import print


def find_pgp_blocks(text):
    pattern = r"\n?(\s*?-----BEGIN PGP MESSAGE-----.*?-----END PGP MESSAGE-----)"
    return re.findall(pattern, text, re.DOTALL)

def process_file(file_path, gpg, new_key_id):
    print(f"file: {file_path}")

    with open(file_path, 'r+') as file:
        content = file.read()
        pgp_blocks = find_pgp_blocks(content)
        print(f"content before:\n{content}")

        for block in pgp_blocks:
            line_length_before = max((len(line) for line in block.splitlines()))
            line_length_after = max((len(line.lstrip()) for line in block.splitlines()))
            padding_size = line_length_before - line_length_after


            print(f"block before (padding size {padding_size}):\n{block}")

            block = dedent(block)
            decrypted_data = gpg.decrypt(block, passphrase=None, always_trust=True)

            if not decrypted_data.ok:
                print(f"Failed to decrypt block in {file_path}")
                continue

            encrypted_data = gpg.encrypt(str(decrypted_data), new_key_id, always_trust=True)

            if not encrypted_data.ok:
                print(f"Failed to encrypt block in {file_path}")
                continue

            if padding_size:
                encrypted_data = indent(str(encrypted_data), " " * padding_size)
            else:
                encrypted_data = str(encrypted_data)

            print(f"block after:\n{encrypted_data}")
            content = content.replace(block, encrypted_data)
            print(f"content after:\n{content}")

        # file.seek(0)
        # file.write(content)
        # file.truncate()

def process_directory(directory, gpg, new_key_id):
    print(f'[red]{{"dir": "{directory}"}}')
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.rsplit(".", 1)[-1] not in ["sls", "gpg"]:
                continue
            file_path = os.path.join(root, name)
            # if file_path != "./pillar/ssh-keys/init.sls":
            #     continue
            process_file(file_path, gpg, new_key_id)