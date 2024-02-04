[![CI](https://github.com/raddessi/salt-gnupg-rotate/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/raddessi/salt-gnupg-rotate/actions/workflows/ci.yaml)
[![documentation](https://img.shields.io/badge/docs-sphinx%20furo-blue.svg?style=flat)](https://github.com/pradyunsg/furo)
[![Checked with MyPy](https://img.shields.io/badge/mypy-checked-blue.svg)](http://mypy-lang.org/)
[![Python Versions](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12-blue.svg)](#salt-gnupg-rotate)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

<!-- sphinx-include-starts-here -->

# salt-gnupg-rotate

Easily rotate gnupg encryption keys of fully or partially encrypted files. 🧂

## About

This project was created to help with the rotation of secret keys on saltstack
controllers. Like probably at least some of you I am bad at rotating encryption
keys due to the effort and time required. This tool is meant to make that task
quick and painless.

[![main-demo](https://github.com/raddessi/salt-gnupg-rotate/assets/6693022/a8546480-3437-42ba-94f0-acca215d6fcc)](https://asciinema.org/a/636043)

## Documentation

Documentation is hosted at
[raddessi.github.io/salt-gnupg-rotate/](https://raddessi.github.io/salt-gnupg-rotate/)
and prebuilt zip files of the project documentation are available for download
from the [Releases](https://github.com/raddessi/salt-gnupg-rotate/releases)
page.

## Features

- It's fast! Rotate your keys in seconds
- Encrypted blocks are updated in-place in your files, keeping surrounding
  context and current indentation
- Trace level logging using `--log-level trace` will show you the decrypted
  block contents as well as the re-encrypted blocks for you to manually validate
  the changed before applying them
- No changes to your data will be made unless the `--write` flag is given

## Discussion

- [GitHub Discussions](https://github.com/raddessi/salt-gnupg-rotate/discussions) -
  Discussion forum hosted by GitHub; ideal for Q&A and other structured
  discussions

<!-- sphinx-include-stops-here -->

## Installation

Please see [the documentation](https://raddessi.github.io/salt-gnupg-rotate/)
for instructions on installation or upgrades.

## Providing Feedback

The best platform for general feedback, assistance, and other discussion is our
[GitHub discussions](https://github.com/raddessi/salt-gnupg-rotate/discussions).
To report a bug or request a specific feature, please open a GitHub issue using
the
[appropriate template](https://github.com/raddessi/salt-gnupg-rotate/issues/new/choose).

If you are interested in contributing to the development of this project, please
read our contributing guide in the documentation prior to beginning any work.
