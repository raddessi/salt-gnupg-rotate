# CHANGELOG



## v1.3.0 (2024-02-03)

### Feature

* feat: consistent coloring in trace level output (#45) ([`f9f3d89`](https://github.com/raddessi/salt-gnupg-rotate/commit/f9f3d896490d335534234018be88f6a5fea7939d))


## v1.2.1 (2024-02-03)

### Documentation

* docs: update asciinema link (#44) ([`1512e9f`](https://github.com/raddessi/salt-gnupg-rotate/commit/1512e9f4abc07b145c94d8a4b0949bde211f5011))

* docs: add asciinema demos (#42) ([`f7e65e6`](https://github.com/raddessi/salt-gnupg-rotate/commit/f7e65e6e62d9d93a8aec19c21646ef9c018a800f))

### Fix

* fix: readme code style badge (#43) ([`2ac513f`](https://github.com/raddessi/salt-gnupg-rotate/commit/2ac513f0bd285d4abc5e366ff1d3b3b5ef47e60a))


## v1.2.0 (2024-02-03)

### Chore

* chore(deps): update actions/upload-artifact action to v4 (#40)

Co-authored-by: renovate[bot] &lt;29139614+renovate[bot]@users.noreply.github.com&gt; ([`051a51a`](https://github.com/raddessi/salt-gnupg-rotate/commit/051a51acb3d45b80091a7c07de9f2c1b010bc392))

* chore(deps): update dependency typeguard to v4 (#27)

Co-authored-by: renovate[bot] &lt;29139614+renovate[bot]@users.noreply.github.com&gt;
Co-authored-by: Ryan Addessi &lt;raddessi@users.noreply.github.com&gt; ([`a57ebd9`](https://github.com/raddessi/salt-gnupg-rotate/commit/a57ebd9b09110789248cd54d06b05162a13b9e84))

* chore(deps): update actions/upload-artifact action to v4 (#38)

Co-authored-by: renovate[bot] &lt;29139614+renovate[bot]@users.noreply.github.com&gt; ([`4db1054`](https://github.com/raddessi/salt-gnupg-rotate/commit/4db105437758cd1e8a3accc97eabd02ae288babf))

* chore(deps): update codecov/codecov-action action to v4 (#35)

Co-authored-by: renovate[bot] &lt;29139614+renovate[bot]@users.noreply.github.com&gt; ([`77212dc`](https://github.com/raddessi/salt-gnupg-rotate/commit/77212dc122fb6926083c050a7e754e5ff2646c28))

* chore(deps): update dependency ipython to v8.21.0 (#34)

Co-authored-by: renovate[bot] &lt;29139614+renovate[bot]@users.noreply.github.com&gt; ([`2cde203`](https://github.com/raddessi/salt-gnupg-rotate/commit/2cde203db72b71418c5d93fbabbb16e635aebae2))

* chore(deps): update dependency xdoctest to v1.1.3 (#33)

Co-authored-by: renovate[bot] &lt;29139614+renovate[bot]@users.noreply.github.com&gt; ([`2af8bc2`](https://github.com/raddessi/salt-gnupg-rotate/commit/2af8bc2f29cb28e1edcc92ec4c54cfc157e658f8))

* chore(deps): update actions/setup-python action to v5 (#26)

Co-authored-by: renovate[bot] &lt;29139614+renovate[bot]@users.noreply.github.com&gt; ([`906b892`](https://github.com/raddessi/salt-gnupg-rotate/commit/906b8927533cc546901205f93ea73e1a2ce37908))

* chore(deps): update dependency furo to v2024 (#30)

Co-authored-by: renovate[bot] &lt;29139614+renovate[bot]@users.noreply.github.com&gt; ([`03fdf33`](https://github.com/raddessi/salt-gnupg-rotate/commit/03fdf339b68d6b31b734c5805cbbd7065c6b7ea6))

### Ci

* ci: always upload artifacts (#39) ([`d813e14`](https://github.com/raddessi/salt-gnupg-rotate/commit/d813e1431c8f127a91b4ed261111c94348fc7b36))

* ci: upload coverage artifacts (#37) ([`ba015b0`](https://github.com/raddessi/salt-gnupg-rotate/commit/ba015b013f80c67b6710575596ebcab1d0321c42))

* ci: ignore mixed line endings on the CHANGELOG (#32) ([`3a86244`](https://github.com/raddessi/salt-gnupg-rotate/commit/3a86244ac7bec7969f044e0b42014ad4687415f5))

### Feature

* feat: print relative file paths (#41) ([`586fbaf`](https://github.com/raddessi/salt-gnupg-rotate/commit/586fbafcf0bae2dbb3378f061c85c5f81d86a081))

### Test

* test: test against all current python versions (#36) ([`ff29e82`](https://github.com/raddessi/salt-gnupg-rotate/commit/ff29e82c597638fee0eaa529dbedffc86657d551))


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
