"""{{cookiecutter.project_name}} Nox sessions."""

import nox
from nox.sessions import Session

locations = "src", "tests", "noxfile.py", "docs/conf.py"
nox.options.sessions = "lint", "mypy", "pytype", "tests", "docs"
_versions = ["3.7", "3.8"]


@nox.session(python=_versions)
def lint(session: Session) -> None:
    """Run the code linters."""
    args = session.posargs or locations
    session.install(
        "darglint",
        "flake8",
        "flake8-annotations",
        "flake8-black",
        "flake8-docstrings",
        "flake8-isort",
        "flake8-rst-docstrings",
        "flake8_sphinx_links",
    )
    session.run("flake8", *args)


@nox.session(python=_versions)
def tests(session: Session) -> None:
    """Run tests."""
    args = session.posargs or ["--cov", "--xdoctest"]
    session.run("poetry", "install", "--no-dev", external=True)
    session.install("coverage[toml]", "pytest", "pytest-cov", "xdoctest")
    session.run("pytest", *args)


@nox.session(python=_versions)
def format(session: Session) -> None:
    """Format the code using black and isort."""
    isort(session)
    black(session)


@nox.session(python=_versions)
def isort(session: Session) -> None:
    """Run the import re-orderer (isort)."""
    args = session.posargs or locations
    session.install("flake8-isort")
    session.run("isort", *args)


@nox.session(python=_versions)
def black(session: Session) -> None:
    """Run the code reformatter (black)."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session(python=_versions)
def mypy(session: Session) -> None:
    """Run the static type checker (mypy))."""
    args = session.posargs or locations
    session.install("mypy")
    session.run("mypy", *args)


@nox.session(python=_versions)
def pytype(session: Session) -> None:
    """Run the static type checker (pytype)."""
    args = session.posargs or ["--disable=import-error", *locations]
    session.install("pytype")
    session.run("pytype", *args)


@nox.session(python=_versions)
def docs(session: Session) -> None:
    """Build the documentation."""
    session.run("poetry", "install", "--no-dev", external=True)
    session.install(
        "six",
        "sphinx",
        "sphinx-autodoc-typehints",
        "sphinxcontrib.mermaid",
    )
    session.run("sphinx-build", "docs", "docs/_build")
