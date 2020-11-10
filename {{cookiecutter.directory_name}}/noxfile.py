import nox

locations = "src", "tests", "noxfile.py"
nox.options.sessions = "lint", "tests"


@nox.session(python=["3.7", "3.8"])
def lint(session):
    args = session.posargs or locations
    session.install("flake8", "flake8-black", "flake8-isort")
    session.run("flake8", *args)


@nox.session(python=["3.7", "3.8"])
def tests(session):
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session(python=["3.7", "3.8"])
def format(session):
    isort(session)
    black(session)


@nox.session(python=["3.7", "3.8"])
def isort(session):
    args = session.posargs or locations
    session.install("flake8-isort")
    session.run("isort", *args)


@nox.session(python=["3.7", "3.8"])
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)
