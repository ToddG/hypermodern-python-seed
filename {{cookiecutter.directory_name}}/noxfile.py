import nox
import tempfile

locations = "src", "tests", "noxfile.py"
nox.options.sessions = "lint", "mypy", "tests"


def install_with_constraints(session, *args, **kwargs):
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


@nox.session(python=["3.7", "3.8"])
def lint(session):
    args = session.posargs or locations
    install_with_constraints(session, "flake8", "flake8-black", "flake8-isort")
    session.run("flake8", *args)


@nox.session(python=["3.7", "3.8"])
def tests(session):
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "coverage[toml]", "pytest", "pytest-cov") 
    session.run("pytest", *args)


@nox.session(python=["3.7", "3.8"])
def format(session):
    isort(session)
    black(session)


@nox.session(python=["3.7", "3.8"])
def isort(session):
    args = session.posargs or locations
    install_with_constraints(session, "flake8-isort")
    session.run("isort", *args)


@nox.session(python=["3.7", "3.8"])
def black(session):
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python=["3.7", "3.8"])
def mypy(session):
    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)

