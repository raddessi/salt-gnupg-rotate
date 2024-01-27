# Setting Up for Development

Here we will set up your system to develop this project.

## Install dependencies

You will need the following python modules installed on your system:

- `poetry`
- `nox`
- `nox-poetry`

````{tab} pip
```bash
pip install poetry nox nox-poetry
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

Once these are installed you should be good to go.

---

See [](running-tests) for how to run the test suite. nox nox-poetry
