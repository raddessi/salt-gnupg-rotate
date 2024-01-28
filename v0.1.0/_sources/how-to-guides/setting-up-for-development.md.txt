# Setting Up for Development

Here we will set up your system to develop this project.

## Install dependencies

You will need the following python modules installed on your system:

- `poetry`
- `nox`
- `nox-poetry`
- `pre-commit`

````{tab} pip
```bash
pip install poetry nox nox-poetry pre-commit
```
````

You will also need either `conda` or `mamba` for virtual environment management.
I am partial to miniforge myself but any flavor should work.

```{tab} Miniforge
See the Miniforge [README](https://github.com/conda-forge/miniforge)
```

````{tab} Fedora
```bash
sudo dnf install conda
```
````

## Checkout the project and install hooks

Checkout the upstream or your own fork of the project

```bash
# checkout
git checkout <github project url>

# install commit hooks
cd salt-gnupg-rotate
pre-commit install --install-hooks
```

Now you should be set up to develop the project.

---

See [](running-tests) for how to run the test suite.
