"""
Step definitions for error handling tests.
"""

from behave import given, when, then
from click.testing import CliRunner
from noah123d.__main__ import main
from pathlib import Path
import os


@given('an invalid file "{filename}"')
def step_invalid_file(context, filename):
    """Set up an invalid file scenario."""
    context.invalid_filename = filename
    
    if filename == "empty.stl":
        # Create an empty file
        file_path = context.test_data_dir / filename
        file_path.touch()
        context.invalid_file_path = file_path
    elif filename == "corrupt.stl":
        # Create a file with invalid STL content
        file_path = context.test_data_dir / filename
        with open(file_path, 'w') as f:
            f.write("This is not a valid STL file content")
        context.invalid_file_path = file_path
    else:
        # For nonexistent.stl, we just use the name without creating the file
        context.invalid_file_path = context.test_data_dir / filename


@given('a directory that does not exist')
def step_nonexistent_directory(context):
    """Set up a non-existent directory scenario."""
    context.nonexistent_dir = context.test_data_dir / "this_directory_does_not_exist"
    # Ensure it doesn't exist
    assert not context.nonexistent_dir.exists()


@given('a file that cannot be read due to permissions')
def step_permission_denied_file(context):
    """Set up a file with permission issues."""
    # Create a file and try to make it unreadable
    # Note: This might not work on all systems, especially Windows
    file_path = context.test_data_dir / "protected.stl"
    with open(file_path, 'w') as f:
        f.write(context.sample_stl_content)
    
    try:
        # Try to remove read permissions (Unix-like systems)
        os.chmod(file_path, 0o000)
        context.protected_file_path = file_path
    except (OSError, NotImplementedError):
        # If we can't change permissions, skip this test
        context.protected_file_path = None


@given('a file with invalid mesh data')
def step_invalid_mesh_data_file(context):
    """Create a file that looks like STL but has invalid mesh data."""
    invalid_stl_content = """solid test
  facet normal invalid_normal_data
    outer loop
      vertex not_a_number 0.0 0.0
      vertex 1.0 invalid_coordinate 0.0
      vertex 0.5 1.0 not_a_number
    endloop
  endfacet
endsolid test
"""
    
    file_path = context.test_data_dir / "invalid_mesh.stl"
    with open(file_path, 'w') as f:
        f.write(invalid_stl_content)
    context.invalid_mesh_file = file_path


@when('I try to process the file')
def step_try_process_file(context):
    """Try to process the invalid file."""
    context.runner = CliRunner()
    
    if hasattr(context, 'invalid_file_path'):
        file_path = context.invalid_file_path
    elif hasattr(context, 'protected_file_path') and context.protected_file_path:
        file_path = context.protected_file_path
    elif hasattr(context, 'invalid_mesh_file'):
        file_path = context.invalid_mesh_file
    else:
        file_path = context.invalid_filename
    
    context.command_result = context.runner.invoke(main, ['--model', str(file_path)])
    context.command_output = context.command_result.output
    context.command_exit_code = context.command_result.exit_code


@when('I try to process models from the directory')
def step_try_process_from_directory(context):
    """Try to process models from a non-existent directory."""
    context.runner = CliRunner()
    context.command_result = context.runner.invoke(main, ['--directory', str(context.nonexistent_dir)])
    context.command_output = context.command_result.output
    context.command_exit_code = context.command_result.exit_code


@then('I should see an appropriate error message')
def step_see_appropriate_error_message(context):
    """Verify that an appropriate error message is shown."""
    error_indicators = [
        "Error", "error", "not found", "invalid", "failed", 
        "cannot", "unable", "✗", "does not exist"
    ]
    assert any(indicator in context.command_output for indicator in error_indicators), \
        f"No error message found in output: {context.command_output}"


@then('the application should continue running')
def step_application_continues_running(context):
    """Verify that the application doesn't crash and continues."""
    # The application should exit normally (exit code 0) even with errors
    # because Click handles many errors gracefully
    assert context.command_exit_code in [0, 2], \
        f"Unexpected exit code: {context.command_exit_code}"


@then('I should see a directory not found error')
def step_see_directory_not_found_error(context):
    """Verify directory not found error."""
    error_indicators = ["does not exist", "not found", "No such file or directory"]
    assert any(indicator in context.command_output for indicator in error_indicators), \
        f"Directory not found error not detected in: {context.command_output}"


@then('the application should handle it gracefully')
def step_application_handles_gracefully(context):
    """Verify the application handles errors gracefully."""
    # Should not crash (exit code should be reasonable)
    assert context.command_exit_code in [0, 1, 2]
    # Should not have Python tracebacks in user output
    assert "Traceback" not in context.command_output


@then('I should see a permission error message')
def step_see_permission_error(context):
    """Verify permission error message."""
    if context.protected_file_path is None:
        # Skip this check if we couldn't set up the permission test
        context.scenario.skip("Permission test not supported on this system")
        return
    
    permission_indicators = ["Permission denied", "permission", "access denied", "cannot read"]
    assert any(indicator.lower() in context.command_output.lower() for indicator in permission_indicators)


@then('I should see a mesh loading error')
def step_see_mesh_loading_error(context):
    """Verify mesh loading error."""
    mesh_error_indicators = ["Error loading STL", "invalid", "failed", "✗"]
    assert any(indicator in context.command_output for indicator in mesh_error_indicators)


@then('the error should be descriptive')
def step_error_is_descriptive(context):
    """Verify that the error message is descriptive."""
    # Error message should be more than just a generic "Error"
    assert len(context.command_output.strip()) > 10
    # Should contain some context about what went wrong
    descriptive_words = ["file", "model", "STL", "loading", "processing"]
    assert any(word in context.command_output for word in descriptive_words)


@then('the application should continue')
def step_application_should_continue(context):
    """Verify that the application continues after error."""
    # Application should not crash with unhandled exceptions
    assert context.command_exit_code in [0, 1, 2]
    # Should not show Python tracebacks
    assert "Traceback" not in context.command_output
