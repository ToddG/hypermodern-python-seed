"""{{cookiecutter.project_name}} tests."""

import click.testing
import pytest
from click.testing import CliRunner
from {{cookiecutter.project_name}} import console
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture
def runner() -> CliRunner:
    """Create a client runner fixture."""
    return click.testing.CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """Test that the client returns."""
    result = runner.invoke(console.main)
    assert result.exit_code == 0
