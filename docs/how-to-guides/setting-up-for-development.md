# Setting Up for Development

Here we will set up your system to develop this project.

## Install dependencies

You will need the following python modules installed on your system:

- `poetry`
- `nox`
- `nox-poetry`
- `pre-commit`

````{tab} pipx
```bash
pipx install poetry
pipx install pre-commit
pipx install nox
pipx inject nox nox-poetry
```
````

````{tab} pip
```bash
pip install poetry nox nox-poetry pre-commit
```
````

You will also need either `conda` or `mamba` for virtual environment management.
I am partial to miniforge myself which includes both utilities but any flavor of installer should work as long as `conda` or `mamba` are present on your system.

`````{tab} Miniforge
````{tab} Miniforge Installer
See the Miniforge [README](https://github.com/conda-forge/miniforge) and [installation instructions](https://github.com/conda-forge/miniforge#install) for your operating system
````
`````

`````{tab} Conda
````{tab} Fedora
```bash
sudo dnf install conda
```
````
`````

## Checkout the project and install git hooks

Checkout the upstream or your own fork of the project

```bash
# checkout the project locally
git checkout https://github.com/raddessi/salt-gnupg-rotate

# install commit hooks
cd salt-gnupg-rotate
pre-commit install --install-hooks
```

Now you should be set up to develop the project.

---

See [](running-tests) for how to run the test suite.
