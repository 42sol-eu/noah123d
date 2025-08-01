"""Test module for Noah123d."""

import pytest
from noah123d import main
from click.testing import CliRunner


def test_main_no_args():
    """Test main function with no arguments."""
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "No models loaded. Use --model" in result.output


def test_main_help():
    """Test main function help."""
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert "Noah123d - CLI for building assemblies from STL models" in result.output
