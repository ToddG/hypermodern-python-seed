import click

from . import __version__


@click.command()
@click.version_option(version=__version__)
def main():
    """The {{cookiecutter.project_name}} console."""
    click.echo("console for {{cookiecutter.project_name}} started...")
