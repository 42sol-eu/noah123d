"""
Step definitions for CLI basic functionality tests.
"""

from behave import given, when, then
from click.testing import CliRunner
from noah123d.__main__ import main
import re


@given('the noah123d CLI is available')
def step_cli_available(context):
    """Verify that the CLI is available for testing."""
    context.runner = CliRunner()
    assert context.runner is not None


@when('I run the command with "{option}" option')
def step_run_command_with_option(context, option):
    """Run the CLI command with a specific option."""
    context.runner = CliRunner()
    context.command_result = context.runner.invoke(main, [option])
    context.command_output = context.command_result.output
    context.command_exit_code = context.command_result.exit_code


@when('I run the command with no arguments')
def step_run_command_no_args(context):
    """Run the CLI command with no arguments."""
    context.runner = CliRunner()
    context.command_result = context.runner.invoke(main, [])
    context.command_output = context.command_result.output
    context.command_exit_code = context.command_result.exit_code


@when('I run the command with model "{filename}"')
def step_run_command_with_model(context, filename):
    """Run the CLI command with a specific model file."""
    context.runner = CliRunner()
    context.command_result = context.runner.invoke(main, ['--model', filename])
    context.command_output = context.command_result.output
    context.command_exit_code = context.command_result.exit_code


@then('I should see the help text')
def step_see_help_text(context):
    """Verify that help text is displayed."""
    assert context.command_output is not None
    assert len(context.command_output.strip()) > 0


@then('the help text should contain "{text}"')
def step_help_contains_text(context, text):
    """Verify that help text contains specific content."""
    assert text in context.command_output, f"Expected '{text}' not found in output: {context.command_output}"


@then('I should see the version information')
def step_see_version_info(context):
    """Verify that version information is displayed."""
    assert "version" in context.command_output.lower()


@then('the version should match the expected format')
def step_version_format_check(context):
    """Verify that version follows expected format (YYYY.M.P)."""
    # Look for version pattern like "2025.0.1"
    version_pattern = r'\d{4}\.\d+\.\d+'
    assert re.search(version_pattern, context.command_output), f"Version format not found in: {context.command_output}"


@then('I should see a message about no models loaded')
def step_see_no_models_message(context):
    """Verify that the 'no models loaded' message is shown."""
    assert "No models loaded" in context.command_output


@then('the message should suggest using "{option}" option')
def step_message_suggests_option(context, option):
    """Verify that the message suggests using a specific option."""
    assert option in context.command_output


@then('I should see an error message about file not found')
def step_see_file_not_found_error(context):
    """Verify that file not found error is displayed."""
    # The actual error might be handled by click or by our application
    # We expect either the file doesn't exist or our app shows an error
    assert any(phrase in context.command_output.lower() for phrase in [
        "does not exist", "not found", "no such file", "error"
    ])


@then('the exit code should be {expected_code:d}')
def step_check_exit_code(context, expected_code):
    """Verify the command exit code."""
    assert context.command_exit_code == expected_code, f"Expected exit code {expected_code}, got {context.command_exit_code}"
