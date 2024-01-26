"""Nox sessions."""
import shutil
import sys
from pathlib import Path
from textwrap import dedent

import nox

try:
    from nox_poetry import Session
    from nox_poetry import session as nox_session
except ImportError:
    message = f"""\
    Nox failed to import the 'nox-poetry' package.

    Please install it using the following command:

    {sys.executable} -m pip install nox-poetry"""
    raise SystemExit(dedent(message)) from None


PACKAGE = "salt_gnupg_rotate"
PYTHON_VERSIONS = [
    "3.10",
]
nox.needs_version = ">= 2021.10.1"
nox.options.default_venv_backend = "conda"
nox.options.error_on_external_run = True
nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = (
    "safety",
    "mypy",
    "docs-build",
    "docs-spelling",
    "xdoctest",
    "tests",
)


@nox_session(python="3.10")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages.

    Args:
        session: The running nox session

    """
    requirements = session.poetry.export_requirements()
    session.install("safety")
    session.run("safety", "check", "--full-report", f"--file={requirements}")


@nox_session(python=PYTHON_VERSIONS)
def mypy(session: Session) -> None:
    """Type-check using mypy.

    Args:
        session: The running nox session

    """
    args = session.posargs or [
        "salt_gnupg_rotate/",
        "tests/",
        "docs/conf.py",
    ]
    session.install(".")
    session.install("mypy", "pytest", "pytest-mock", "nox", "nox-poetry")
    session.run("mypy", *args)
    if not session.posargs:
        session.run("mypy", "noxfile.py")


@nox_session(python=PYTHON_VERSIONS)
def tests(session: Session) -> None:
    """Run the test suite.

    Args:
        session: The running nox session

    """
    session.install(".")
    session.install(
        "coverage[toml]",
        "jinja2-time",
        "pre-commit",
        "pygments",
        "pytest",
        "pytest-mock",
        "ruamel.yaml",
        "typeguard",
    )
    try:
        session.run(
            "coverage",
            "run",
            "--parallel",
            "-m",
            "pytest",
            "--color=yes",
            f"--typeguard-packages={PACKAGE}",
            *session.posargs,
        )
    finally:
        session.notify(target="coverage", posargs=[])


@nox_session(python="3.10")
def coverage(session: Session) -> None:
    """Produce the coverage report.

    Args:
        session: The running nox session

    """
    args = session.posargs or ["report"]

    session.install("coverage[toml]")

    if not session.posargs and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")

    session.run("coverage", *args)


@nox_session(python=PYTHON_VERSIONS)
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest.

    Args:
        session: The running nox session

    """
    args = session.posargs or ["all"]
    session.install(".")
    session.install("xdoctest[colors]")
    session.run("python", "-m", "xdoctest", PACKAGE, *args)


@nox_session(name="docs-build", python="3.10")
def docs_build(session: Session) -> None:
    """Build the documentation.

    Args:
        session: The running nox session

    """
    # run with `-b dirhtml` for nicer URLS when building for publishing to a server
    args = session.posargs or ["-b", "html", "-W", "--keep-going"]
    session.install(".")
    session.install(
        "furo",
        "myst-parser",
        "sphinx",
        "sphinx-autobuild",
        "sphinx-click",
        "sphinx-copybutton",
        "sphinx-inline-tabs",
        "sphinxcontrib-mermaid",
        "sphinxcontrib-spelling",
        "sphinxemoji",
    )

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-build", "docs", "docs/_build", "--color", *args)


@nox_session(name="docs-spelling", python="3.10")
def docs_spelling(session: Session) -> None:
    """Check spelling in the documentation.

    Args:
        session: nox test session

    """
    args = session.posargs or [
        "-b",
        "spelling",
        "-W",
        "--keep-going",
        "docs",
        "docs/_spelling",
    ]
    session.install(".")
    session.conda_install("hunspell", channel="conda-forge")
    session.install(
        "furo",
        "myst-parser",
        "sphinx",
        "sphinx-autobuild",
        "sphinx-click",
        "sphinx-copybutton",
        "sphinx-inline-tabs",
        "sphinxcontrib-mermaid",
        "sphinxcontrib-spelling",
        "sphinxemoji",
    )
    # maybe use https://pyspellchecker.readthedocs.io/en/latest/index.html?
    # session.conda_install("enchant", channel="conda-forge")

    spelling_dir = Path("docs", "_spelling")
    if spelling_dir.exists():
        shutil.rmtree(spelling_dir)

    session.run("sphinx-build", *args)


@nox_session(python="3.10")
def docs(session: Session) -> None:
    """Build and serve the documentation with live reloading on file changes.

    Args:
        session: The running nox session

    """
    args = session.posargs or ["-b", "dirhtml", "--open-browser"]
    session.install(".")
    session.install(
        "furo",
        "myst-parser",
        "sphinx",
        "sphinx-autobuild",
        "sphinx-click",
        "sphinx-copybutton",
        "sphinx-inline-tabs",
        "sphinxcontrib-mermaid",
        "sphinxcontrib-spelling",
        "sphinxemoji",
    )

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-autobuild", "docs", "docs/_build", *args)
