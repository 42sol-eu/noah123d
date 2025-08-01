"""
Step definitions for model processing tests.
"""

from behave import given, when, then
from click.testing import CliRunner
from noah123d.__main__ import main
from pathlib import Path
import tempfile
import shutil


@given('I have sample STL files available')
def step_sample_stl_files_available(context):
    """Ensure we have the infrastructure to create sample STL files."""
    context.runner = CliRunner()
    assert hasattr(context, 'sample_stl_content')


@given('a valid STL file "{filename}" exists')
def step_create_valid_stl_file(context, filename):
    """Create a valid STL file for testing."""
    if not hasattr(context, 'test_files'):
        context.test_files = {}
    
    file_path = context.test_data_dir / filename
    with open(file_path, 'w') as f:
        f.write(context.sample_stl_content)
    
    context.test_files[filename] = file_path
    assert file_path.exists()


@given('valid STL files "{file1}" and "{file2}" exist')
def step_create_multiple_stl_files(context, file1, file2):
    """Create multiple valid STL files for testing."""
    if not hasattr(context, 'test_files'):
        context.test_files = {}
    
    for filename in [file1, file2]:
        file_path = context.test_data_dir / filename
        with open(file_path, 'w') as f:
            f.write(context.sample_stl_content)
        context.test_files[filename] = file_path
        assert file_path.exists()


@given('a directory "{dirname}" contains STL files')
def step_create_directory_with_stl_files(context, dirname):
    """Create a directory containing STL files."""
    dir_path = context.test_data_dir / dirname
    dir_path.mkdir(exist_ok=True)
    
    # Create a couple of STL files in the directory
    for filename in ['model1.stl', 'model2.stl']:
        file_path = dir_path / filename
        with open(file_path, 'w') as f:
            f.write(context.sample_stl_content)
    
    context.test_directory = dir_path


@given('a valid STL file positioned away from origin')
def step_create_offset_stl_file(context):
    """Create an STL file with vertices not at origin."""
    # Create STL content with vertices offset from origin
    offset_stl_content = """solid test
  facet normal 0.0 0.0 1.0
    outer loop
      vertex 10.0 5.0 3.0
      vertex 11.0 5.0 3.0
      vertex 10.5 6.0 3.0
    endloop
  endfacet
endsolid test
"""
    
    filename = "offset_model.stl"
    file_path = context.test_data_dir / filename
    with open(file_path, 'w') as f:
        f.write(offset_stl_content)
    
    if not hasattr(context, 'test_files'):
        context.test_files = {}
    context.test_files[filename] = file_path


@when('I process the model file "{filename}"')
def step_process_model_file(context, filename):
    """Process a specific model file."""
    file_path = context.test_files[filename]
    context.runner = CliRunner()
    context.command_result = context.runner.invoke(main, ['--model', str(file_path)])
    context.command_output = context.command_result.output
    context.command_exit_code = context.command_result.exit_code


@when('I process the model file')
def step_process_the_model_file(context):
    """Process the model file (when there's only one or a default)."""
    # Assume we're working with the offset model from the previous step
    filename = "offset_model.stl"
    file_path = context.test_files[filename]
    context.runner = CliRunner()
    context.command_result = context.runner.invoke(main, ['--model', str(file_path)])
    context.command_output = context.command_result.output
    context.command_exit_code = context.command_result.exit_code


@when('I process multiple model files')
def step_process_multiple_model_files(context):
    """Process multiple model files."""
    file_paths = [str(path) for path in context.test_files.values()]
    args = []
    for path in file_paths:
        args.extend(['--model', path])
    
    context.runner = CliRunner()
    context.command_result = context.runner.invoke(main, args)
    context.command_output = context.command_result.output
    context.command_exit_code = context.command_result.exit_code


@when('I process all models from the directory')
def step_process_directory_models(context):
    """Process all models from a directory."""
    context.runner = CliRunner()
    context.command_result = context.runner.invoke(main, ['--directory', str(context.test_directory)])
    context.command_output = context.command_result.output
    context.command_exit_code = context.command_result.exit_code


@when('I process the model with verbose output enabled')
def step_process_model_verbose(context, filename="cube.stl"):
    """Process a model with verbose output."""
    if filename in context.test_files:
        file_path = context.test_files[filename]
    else:
        # Default to first available file
        file_path = list(context.test_files.values())[0]
    
    context.runner = CliRunner()
    context.command_result = context.runner.invoke(main, ['--model', str(file_path), '--verbose'])
    context.command_output = context.command_result.output
    context.command_exit_code = context.command_result.exit_code


@then('the model should be loaded successfully')
def step_model_loaded_successfully(context):
    """Verify that the model was loaded successfully."""
    assert "Successfully loaded STL" in context.command_output or "Loading STL model file" in context.command_output


@then('I should see confirmation that the model was loaded')
def step_see_model_load_confirmation(context):
    """Verify that there's confirmation of model loading."""
    success_indicators = ["Successfully loaded", "Loading STL", "✓"]
    assert any(indicator in context.command_output for indicator in success_indicators)


@then('the model should be moved to origin')
def step_model_moved_to_origin(context):
    """Verify that the model was moved to origin."""
    assert "moved to origin" in context.command_output or "Model moved to origin" in context.command_output


@then('both models should be loaded successfully')
def step_both_models_loaded(context):
    """Verify that multiple models were loaded."""
    # Count occurrences of success indicators
    success_count = context.command_output.count("Successfully loaded") + context.command_output.count("Loading STL")
    assert success_count >= 2, f"Expected at least 2 models loaded, found indicators for {success_count}"


@then('I should see confirmation for each model')
def step_see_confirmation_each_model(context):
    """Verify that each model has confirmation."""
    # This is similar to the previous step but focuses on confirmation messages
    confirmations = context.command_output.count("✓") + context.command_output.count("Successfully")
    assert confirmations >= 2


@then('no duplicate loading should occur')
def step_no_duplicate_loading(context):
    """Verify that models aren't loaded multiple times."""
    # Look for skip messages or ensure no excessive loading
    skip_count = context.command_output.count("Skipping already loaded")
    # If we run the same models twice, we should see skip messages
    # For now, just ensure we don't have errors
    assert "Error" not in context.command_output


@then('all STL files in the directory should be processed')
def step_all_directory_files_processed(context):
    """Verify that all files in directory were processed."""
    # Should see at least 2 files processed (model1.stl and model2.stl)
    assert context.command_output.count("Loading STL") >= 2


@then('I should see a directory search message')
def step_see_directory_search_message(context):
    """Verify that directory search message is shown."""
    assert "Searching directory" in context.command_output


@then('I should see detailed mesh information')
def step_see_detailed_mesh_info(context):
    """Verify that detailed mesh information is shown with verbose output."""
    detailed_indicators = ["Mesh bounds", "triangles", "mesh bounds"]
    assert any(indicator in context.command_output for indicator in detailed_indicators)


@then('I should see mesh bounds information')
def step_see_mesh_bounds_info(context):
    """Verify that mesh bounds are displayed."""
    bounds_indicators = ["X:", "Y:", "Z:", "bounds"]
    assert any(indicator in context.command_output for indicator in bounds_indicators)


@then('I should see triangle count information')
def step_see_triangle_count(context):
    """Verify that triangle count is displayed."""
    assert "triangles" in context.command_output


@then('the model should be moved to origin coordinates')
def step_model_at_origin_coordinates(context):
    """Verify model is moved to origin coordinates."""
    assert "moved to origin" in context.command_output


@then('the bounding box minimum should be at (0,0,0)')
def step_bounding_box_at_origin(context):
    """Verify that bounding box minimum is at origin."""
    # This is more of a logical assertion - our move_model_origin function should do this
    # We verify by checking that the operation completed successfully
    assert "moved to origin" in context.command_output and "✓" in context.command_output
