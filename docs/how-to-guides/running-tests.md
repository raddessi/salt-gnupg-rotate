# Running Tests

Here we will run the test suite for the `salt-gnupg-rotate` project.

```{note}
This tutorial assumes you have already followed the [](setting-up-for-development)
steps to set up for developing this project.
```

## Running all the test suites

To run all of the test suites:

```bash
nox
```

## Running a specific test suite
List out the available nox test suites:

```bash
nox -s
```

Select the suite you would like to run from the list of available suites and run it with:

```bash
nox -s <suite name>
```
