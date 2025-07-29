"""Test module for Noah123D."""

import pytest
from noah123d.main import main
from click.testing import CliRunner


def test_main_no_args():
    """Test main function with no arguments."""
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "No STL file specified" in result.output


def test_main_help():
    """Test main function help."""
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert "Noah123D - Building assemblies from STL models" in result.output
