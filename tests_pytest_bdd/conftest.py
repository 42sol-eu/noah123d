"""
Pytest configuration for BDD tests.
This file provides pytest fixtures and configuration for pytest-bdd tests.
"""

import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture(scope="session")
def temp_test_dir():
    """Create a temporary directory for test files."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_stl_content():
    """Provide sample STL content for testing."""
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


@pytest.fixture
def test_stl_file(temp_test_dir, sample_stl_content):
    """Create a test STL file."""
    stl_file = temp_test_dir / "test_model.stl"
    stl_file.write_text(sample_stl_content)
    return stl_file


# Pytest-bdd configuration
def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    """Handle step errors with more context."""
    print(f"Step failed: {step}")
    print(f"Exception: {exception}")
    # You can add custom error handling here
