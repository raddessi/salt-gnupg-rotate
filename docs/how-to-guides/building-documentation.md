# Building the documentation

Documentation is built via a nox suite that runs sphinx. You can either build
the docs one-time if you want to get a static build for deployment, or you can
start up a server to auto build the documentation when any of the source files
are modified.

```{note}
This tutorial assumes you have already followed the [](setting-up-for-development)
steps to set up for developing this project.
```

## Building static documentation

To generate a static copy of the documentation:

```bash
nox -s docs-build
```

The generated documentation will be placed in the `docs/_build` directory.

## Live-view documentation

To view the documentation live in your browser while editing it you can run:

```bash
nox -s docs
```

A browser window will be opened to the sphinx server so you can view updates
dynamically
