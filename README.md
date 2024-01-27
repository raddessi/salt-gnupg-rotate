[![ci](https://github.com/raddessi/salt-gnupg-rotate/workflows/ci/badge.svg)](https://github.com/raddessi/salt-gnupg-rotate/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-sphinx%20furo-blue.svg?style=flat)](https://github.com/pradyunsg/furo)
[![Checked with MyPy](https://img.shields.io/badge/mypy-checked-blue.svg)](http://mypy-lang.org/)
[![Python Versions](https://img.shields.io/badge/python-3.10-blue.svg)](#salt-gnupg-rotate)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<!-- sphinx-include-starts-here -->

# salt-gnupg-rotate

Easily rotate gnupg encrypted data blocks in files 🧂

## About

This project was created to help with the rotation of secret keys on saltstack controllers. Like probably at least some of you I am bad at rotating encryption keys due to the effort and time required. This tool is meant to make that task quick and painless.


## Documentation

Prebuilt zip files of the
[project documentation](https://github.com/raddessi/salt-gnupg-rotate/tree/main/docs)
are available for download from the
[Releases](https://github.com/raddessi/salt-gnupg-rotate/releases) page.


## Features

* It's fast! Rotate your keys in seconds
* Encrypted blocks are updated in-place in your files, keeping surrounding context and current indentation
* `--log-level trace` level logging will show you the decrypted block contents as well as the re-encrypted blocks for you to manually validate the changed before applying them
* If the `--write` flag is not given then no changes will be made


## Discussion

- [GitHub Discussions](https://github.com/raddessi/salt-gnupg-rotate/discussions) -
  Discussion forum hosted by GitHub; ideal for Q&A and other structured
  discussions

<!-- sphinx-include-stops-here -->

## Installation

Please see
[the documentation](https://github.com/raddessi/salt-gnupg-rotate/releases) for
instructions on installation or upgrades.

## Providing Feedback

The best platform for general feedback, assistance, and other discussion is our
[GitHub discussions](https://github.com/raddessi/salt-gnupg-rotate/discussions).
To report a bug or request a specific feature, please open a GitHub issue using
the
[appropriate template](https://github.com/raddessi/salt-gnupg-rotate/issues/new/choose).

If you are interested in contributing to the development of this project, please
read our contributing guide in the documentation prior to beginning any work.
