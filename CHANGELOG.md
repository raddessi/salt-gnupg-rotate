# CHANGELOG



## v1.1.0 (2024-01-30)

### Chore

* chore(deps): update actions/checkout action to v4 (#25)

Co-authored-by: renovate[bot] &lt;29139614+renovate[bot]@users.noreply.github.com&gt; ([`474696d`](https://github.com/raddessi/salt-gnupg-rotate/commit/474696d13df1fb20b1ca621909a61a011a39bd28))

### Documentation

* docs: fix CI badge and link to online docs (#29) ([`3156977`](https://github.com/raddessi/salt-gnupg-rotate/commit/315697762d2178cbe523bdbfa41ad992b97de3cd))

### Feature

* feat: abort earlier on errors (#31)

This change does a few things:
  - raises exceptions immediately after an error is encountered
  - swaps out older linters for ruff
  - fixes some stability and performance issues raised from the new linter ([`68b7030`](https://github.com/raddessi/salt-gnupg-rotate/commit/68b703083257b9566744a800667d08645f7c7415))


## v1.0.1 (2024-01-29)

### Fix

* fix: duplicate blocks in the same file causes errors (#28)

When an encrypted block is present more than one time in a file it causes errors since the first replacement replaces both instances and the second then fails. ([`21b8543`](https://github.com/raddessi/salt-gnupg-rotate/commit/21b85430313d4e9923773d03a5f9dab0c033281a))


## v1.0.0 (2024-01-29)

### Breaking

* feat!: initial release ([`7eefa6a`](https://github.com/raddessi/salt-gnupg-rotate/commit/7eefa6a9c262bcd5e36f68af2a7bafb752cbce4e))
