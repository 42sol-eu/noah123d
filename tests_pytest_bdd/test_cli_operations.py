"""
pytest-bdd step definitions for CLI operations.
This demonstrates how pytest-bdd integrates with pytest fixtures and patterns.
"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from click.testing import CliRunner
from noah123d.__main__ import main
import re


# Load all scenarios from the feature file
scenarios('features/cli_operations.feature')


# Fixtures (pytest-bdd leverages pytest fixtures)
@pytest.fixture
def cli_runner():
    """Provide a Click CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def command_result():
    """Fixture to store command execution results."""
    return {}


# Step definitions
@when(parsers.parse('I run noah123d with "{option}" option'))
def run_noah123d_with_option(cli_runner, command_result, option):
    """Run noah123d command with specified option."""
    result = cli_runner.invoke(main, [option])
    command_result['result'] = result
    command_result['output'] = result.output
    command_result['exit_code'] = result.exit_code


@when('I run noah123d with no arguments')
def run_noah123d_no_args(cli_runner, command_result):
    """Run noah123d command with no arguments."""
    result = cli_runner.invoke(main, [])
    command_result['result'] = result
    command_result['output'] = result.output
    command_result['exit_code'] = result.exit_code


@then('I should see the help message')
def should_see_help_message(command_result):
    """Verify that help message is displayed."""
    assert command_result['output'] is not None
    assert len(command_result['output'].strip()) > 0
    assert command_result['exit_code'] == 0


@then(parsers.parse('the help should contain "{text}"'))
def help_should_contain_text(command_result, text):
    """Verify that help contains specific text."""
    assert text in command_result['output'], f"Expected '{text}' not found in: {command_result['output']}"


@then('I should see version information displayed')
def should_see_version_info(command_result):
    """Verify that version information is displayed."""
    assert "version" in command_result['output'].lower()
    assert command_result['exit_code'] == 0


@then('the version format should be valid')
def version_format_should_be_valid(command_result):
    """Verify that version follows expected format."""
    version_pattern = r'\d{4}\.\d+\.\d+'
    assert re.search(version_pattern, command_result['output']), \
        f"Version format not found in: {command_result['output']}"


@then(parsers.parse('I should see "{message}" message'))
def should_see_message(command_result, message):
    """Verify that specific message is displayed."""
    assert message in command_result['output'], \
        f"Expected message '{message}' not found in: {command_result['output']}"


@then(parsers.parse('I should see guidance about using "{option}" option'))
def should_see_guidance_about_option(command_result, option):
    """Verify that guidance about specific option is shown."""
    assert option in command_result['output'], \
        f"Expected guidance about '{option}' not found in: {command_result['output']}"
