"""
Environment setup for behave BDD tests.
This file is automatically loaded by behave and provides hooks for setup and teardown.
"""

import tempfile
import shutil
from pathlib import Path
import os
import sys

# Add the project root to Python path so we can import noah123d
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def before_all(context):
    """Set up test environment before all tests."""
    # Create a temporary directory for test files
    context.temp_dir = Path(tempfile.mkdtemp())
    context.test_data_dir = context.temp_dir / "test_data"
    context.test_data_dir.mkdir()
    
    # Store original working directory
    context.original_cwd = os.getcwd()
    
    # Create some sample STL content (minimal valid STL)
    context.sample_stl_content = create_sample_stl_content()


def after_all(context):
    """Clean up after all tests."""
    # Clean up temporary directory
    if hasattr(context, 'temp_dir') and context.temp_dir.exists():
        shutil.rmtree(context.temp_dir)
    
    # Restore original working directory
    if hasattr(context, 'original_cwd'):
        os.chdir(context.original_cwd)


def before_scenario(context, scenario):
    """Set up before each scenario."""
    # Reset any global state if needed
    context.command_result = None
    context.command_output = None
    context.command_exit_code = None


def create_sample_stl_content():
    """Create minimal valid STL file content for testing."""
    return """solid test
  facet normal 0.0 0.0 1.0
    outer loop
      vertex 0.0 0.0 0.0
      vertex 1.0 0.0 0.0
      vertex 0.5 1.0 0.0
    endloop
  endfacet
endsolid test
"""
