"""{{cookiecutter.project_name}} Nox sessions."""
import glob
import os
import tempfile

# from datetime import datetime
from typing import Any

import nox
from nox.sessions import Session

locations = "src", "tests", "noxfile.py", "docs/conf.py"
nox.options.sessions = "format", "lint", "mypy", "pytype", "tests", "docs", "pdf"
_versions = ["3.8"]


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


@nox.session(python=_versions)
def lint(session: Session) -> None:
    """Run the code linters."""
    args = session.posargs or locations
    install_with_constraints(
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
    """Delegate to 'tests'."""
    tests(session=session)


@nox.session(python=_versions)
def tests(session: Session) -> None:
    """Run tests."""
    args = session.posargs or ["--cov", "--xdoctest", "--cov-config=.coveragerc"]
    install_with_constraints(
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


@nox.session(python=_versions)
def docs(session: Session) -> None:
    """Build the documentation as html."""
    session = prepare_documentation(session)
    session.run("sphinx-build", "-b", "html", "docs", "docs/_build/html")


@nox.session(python=_versions)
def pdf(session: Session) -> None:
    """Build the documentation as pdf."""
    session = prepare_documentation(session)
    session.run("sphinx-build", "-b", "latex", "docs", "docs/_build/latex")
    session.cd("docs/_build/latex")
    session.run("make", external=True)


def prepare_documentation(session: Session) -> Session:
    """Prepare the session to render documentation."""
    session.install(".")
    if not os.path.exists("./node_modules/.bin/mmdc"):
        print(
            "Mermaidjs CLI 'mmdc' does not exist, attempting to " "install via 'yarn'"
        )
        session.run("yarn", external=True)
    install_with_constraints(
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
 
    for existing_file in glob.iglob(
            f"{dist_dir}/{{cookiecutter.project_name}}-*"):
        print(f"removing '{existing_file}'")
        os.remove(existing_file)
    session.run("poetry", "build", external=True)
    session.run("poetry", "version", "patch", external=True)
    for new_file in glob.iglob(f"{dist_dir}/{{cookiecutter.project_name}}-*"):
        print(f"created '{new_file}'")

