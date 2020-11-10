"""project_name Nox sessions."""

import tempfile
from typing import Any

import nox
from nox.sessions import Session

locations = "src", "tests", "noxfile.py"
nox.options.sessions = "lint", "mypy", "pytype", "tests"
_versions = ["3.7"]


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install application dependencies using constraints."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=_versions)
def lint(session: Session) -> None:
    """Run the code linters."""
    args = session.posargs or locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-black",
        "flake8-isort",
        "flake8-docstrings",
    )
    session.run("flake8", *args)


@nox.session(python=_versions)
def tests(session: Session) -> None:
    """Run tests."""
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "coverage[toml]", "pytest", "pytest-cov")
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
    install_with_constraints(session, "flake8-isort")
    session.run("isort", *args)


@nox.session(python=_versions)
def black(session: Session) -> None:
    """Run the code reformatter (black)."""
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python=_versions)
def mypy(session: Session) -> None:
    """Run the static type checker (mypy))."""
    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)


@nox.session(python=_versions)
def pytype(session: Session) -> None:
    """Run the static type checker (pytype)."""
    args = session.posargs or ["--disable=import-error", *locations]
    install_with_constraints(session, "pytype")
    session.run("pytype", *args)
