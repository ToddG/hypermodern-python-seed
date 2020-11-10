"""{{cookiecutter.project_name}} console."""

import click

from . import __version__


@click.command()
@click.version_option(version=__version__)
def main() -> None:
    """The {{cookiecutter.project_name}} console entry point."""
    click.echo("console for {{cookiecutter.project_name}} started...")
