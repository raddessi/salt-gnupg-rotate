# Building the documentation

Documentation is built via a nox suite that runs sphinx. You can either build
the docs one-time if you want to get a static build for deployment, or you can
start up a server to auto build the documentation when any of the source files
are modified.

## Building documentation

To only generate the documentation:

```bash
nox -s docs-build
```

## Serving documentation

To build and serve the documentation via `sphinx-autobuild` while rebuilding any
modified documents dynamically:

```bash
nox -s docs
```

A browser window will be opened to the sphinx server so you can view changes
live :)
