# CHANGELOG



## v1.0.1 (2024-01-29)

### Fix

* fix: duplicate blocks in the same file causes errors (#28)

When an encrypted block is present more than one time in a file it causes errors since the first replacement replaces both instances and the second then fails. ([`21b8543`](https://github.com/raddessi/salt-gnupg-rotate/commit/21b85430313d4e9923773d03a5f9dab0c033281a))


## v1.0.0 (2024-01-29)

### Breaking

* feat!: initial release ([`7eefa6a`](https://github.com/raddessi/salt-gnupg-rotate/commit/7eefa6a9c262bcd5e36f68af2a7bafb752cbce4e))
