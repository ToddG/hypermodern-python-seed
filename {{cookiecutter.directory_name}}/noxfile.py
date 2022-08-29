"""{{cookiecutter.project_name}} Nox sessions."""
import glob
import os
import tempfile

# from datetime import datetime
from typing import Any

import nox
from nox.sessions import Session

locations = "src", "test", "noxfile.py", "docs/conf.py"
nox.options.sessions = "format", "lint", "mypy", "test", "docs",
_versions = ["3.10"]


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file.

    This function is a wrapper for nox.sessions.Session.install. It
    invokes pip to install packages inside of the session's virtualenv.
    Additionally, pip is passed a constraints file generated from
    Poetry's lock file, to ensure that the packages are pinned to the
    versions specified in poetry.lock. This allows you to manage the
    packages as Poetry development dependencies.

    Arguments:
        session: The Session object.
        args: Command-line arguments for pip.
        kwargs: Additional keyword arguments for Session.install.
    """
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


def install_without_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages w/o constraints."""
    session.install(*args, **kwargs)


@nox.session(python=_versions)
def lint(session: Session) -> None:
    """Run the code linters."""
    args = session.posargs or locations
    install_without_constraints(
        session,
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
def test(session: Session) -> None:
    """Run tests."""
    args = session.posargs or ["--cov", "--xdoctest", "--cov-config=.coveragerc"]
    install_without_constraints(
        session, "coverage[toml]", "pytest", "pytest-cov", "xdoctest", "click"
    )
    session.install(".")
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
    install_without_constraints(session, "flake8-isort")
    session.run("isort", *args)


@nox.session(python=_versions)
def black(session: Session) -> None:
    """Run the code reformatter (black)."""
    args = session.posargs or locations
    install_without_constraints(session, "black")
    session.run("black", *args)


@nox.session(python=_versions)
def mypy(session: Session) -> None:
    """Run the static type checker (mypy))."""
    args = session.posargs or locations
    install_without_constraints(session, "mypy")
    session.run("mypy", *args)


@nox.session(python=_versions)
def docs(session: Session) -> None:
    """Build the documentation as html."""
    session = prepare_documentation(session)
    session.run("sphinx-build", "-b", "html", "docs", "docs/_build/html")


def prepare_documentation(session: Session) -> Session:
    """Prepare the session to render documentation."""
    session.install(".")
    install_without_constraints(
        session,
        "six",
        "sphinx",
        "sphinx-autodoc-typehints",
        "sphinxcontrib.mermaid",
    )
    return session


@nox.session(python=_versions)
def dist(session: Session) -> None:
    """Build distribution with incremented patch version."""
    dist_dir = "dist"

    iglob = glob.iglob(f"{dist_dir}/{{cookiecutter.project_name}}-*")
    for existing_file in iglob:
        print(f"removing '{existing_file}'")
        os.remove(existing_file)
    session.run("poetry", "build", external=True)
    session.run("poetry", "version", "patch", external=True)
    for new_file in iglob:
        print(f"created '{new_file}'")
