# Contributing to Noah123d

Thank you for your interest in contributing to Noah123d! This document provides guidelines for contributing to the project.

## Getting Started

### Development Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/your-username/noah123d.git
   cd noah123d
   ```

2. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies**:
   ```bash
   poetry install --with dev,docs
   ```

4. **Activate the virtual environment**:
   ```bash
   poetry shell
   ```

5. **Run tests to verify setup**:
   ```bash
   pytest
   ```

### Development Environment

We recommend using VS Code with these extensions:
- Python
- Pylance
- Python Docstring Generator
- GitLens

## Types of Contributions

### 🐛 Bug Reports

When reporting bugs, please include:
- Noah123d version (`python -c "import noah123d; print(noah123d.__version__)"`)
- Python version
- Operating system
- Minimal code example that reproduces the issue
- Expected vs actual behavior
- Any error messages or stack traces

Use the [bug report template](https://github.com/42sol-eu/noah123d/issues/new?template=bug_report.md).

### 💡 Feature Requests

For new features:
- Check existing issues to avoid duplicates
- Describe the use case and problem it solves
- Provide examples of how the API might look
- Consider backward compatibility

Use the [feature request template](https://github.com/42sol-eu/noah123d/issues/new?template=feature_request.md).

### 📝 Documentation

Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add examples or use cases
- Improve API documentation
- Translate documentation (future)

### 🔧 Code Contributions

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

### 2. Make Changes

- Follow the [coding standards](#coding-standards)
- Add tests for new functionality
- Update documentation as needed
- Keep commits small and focused

### 3. Testing

Run the full test suite:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=noah123d

# Run specific test file
pytest tests/test_converters.py

# Run tests in verbose mode
pytest -v
```

### 4. Documentation

Build and test documentation:

```bash
# Install docs dependencies
poetry install --with docs

# Serve docs locally
mkdocs serve

# Build docs
mkdocs build
```

### 5. Submit Pull Request

1. Push your branch to your fork
2. Create a pull request with:
   - Clear title and description
   - Reference to related issues
   - Description of changes made
   - Any breaking changes noted

## Coding Standards

### Python Style

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 88 characters (Black default)
- **Quotes**: Double quotes for strings
- **Imports**: Organized with isort
- **Type hints**: Required for public APIs

### Code Formatting

We use automated formatting tools:

```bash
# Format code with Black
black noah123d/ tests/

# Sort imports with isort
isort noah123d/ tests/

# Run both together
black noah123d/ tests/ && isort noah123d/ tests/
```

### Type Hints

All public functions must have type hints:

```python
from typing import Union, Optional, Dict, List, Any
from pathlib import Path

def convert_stl(
    stl_path: Union[str, Path],
    output_path: Union[str, Path],
    validate: bool = False
) -> bool:
    """Convert STL to 3MF format."""
    pass
```

### Documentation Strings

Use Google-style docstrings:

```python
def stl_to_3mf_grid(
    stl_path: Union[str, Path],
    output_path: Union[str, Path],
    count: int,
    grid_cols: Optional[int] = None,
    spacing_factor: float = 1.1,
    center_grid: bool = True
) -> bool:
    """Create grid layouts with multiple copies.
    
    Args:
        stl_path: Path to input STL file
        output_path: Path for output 3MF file
        count: Number of copies to create
        grid_cols: Number of columns (auto-calculated if None)
        spacing_factor: Spacing multiplier (1.0 = touching)
        center_grid: Center grid at origin
        
    Returns:
        True if conversion successful, False otherwise
        
    Example:
        >>> success = stl_to_3mf_grid("part.stl", "grid.3mf", count=4)
        >>> print(f"Grid created: {success}")
        Grid created: True
    """
    pass
```

## Testing Guidelines

### Test Structure

Tests are organized by module:

```
tests/
├── test_converters.py      # STLConverter tests
├── test_archive3mf.py      # Archive3mf tests
├── test_model.py           # Model tests
├── test_analyzer.py        # Analysis3MF tests
├── test_main.py           # CLI and main function tests
└── fixtures/              # Test data files
    ├── sample.stl
    └── sample.3mf
```

### Writing Tests

Use pytest conventions:

```python
import pytest
from pathlib import Path
from noah123d import STLConverter

class TestSTLConverter:
    def test_convert_basic(self, tmp_path):
        """Test basic STL conversion."""
        converter = STLConverter()
        input_file = Path("tests/fixtures/sample.stl")
        output_file = tmp_path / "output.3mf"
        
        success = converter.convert(input_file, output_file)
        
        assert success is True
        assert output_file.exists()
        assert output_file.stat().st_size > 0
    
    def test_convert_invalid_file(self):
        """Test conversion with invalid input."""
        converter = STLConverter()
        
        success = converter.convert("nonexistent.stl", "output.3mf")
        
        assert success is False
    
    @pytest.mark.parametrize("count,expected_cols", [
        (4, 2),
        (9, 3),
        (6, 3),
    ])
    def test_grid_layouts(self, tmp_path, count, expected_cols):
        """Test various grid layouts."""
        converter = STLConverter()
        input_file = Path("tests/fixtures/sample.stl")
        output_file = tmp_path / "grid.3mf"
        
        success = converter.convert_with_copies(
            input_file, output_file, count=count
        )
        
        assert success is True
        # Add more specific assertions
```

### Test Data

- Keep test files small (< 1MB)
- Use synthetic/generated test data when possible
- Don't commit large binary files
- Document test file sources and licenses

## Documentation Guidelines

### API Documentation

- Every public function needs docstrings
- Include usage examples
- Document parameters and return values
- Note any exceptions that might be raised

### User Documentation

- Write for different skill levels
- Include practical examples
- Use consistent terminology
- Keep examples up to date

### Building Documentation

```bash
# Install documentation dependencies
poetry install --with docs

# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build

# Deploy to GitHub Pages (maintainers only)
mkdocs gh-deploy
```

## Performance Considerations

### Benchmarking

When making performance-related changes:

```python
import time
from noah123d import STLConverter

def benchmark_conversion():
    converter = STLConverter()
    start_time = time.time()
    
    # Your code here
    success = converter.convert("large_model.stl", "output.3mf")
    
    end_time = time.time()
    print(f"Conversion took {end_time - start_time:.2f} seconds")
```

### Memory Usage

Monitor memory usage for large operations:

```python
import psutil
import os

def check_memory():
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / 1024 / 1024
    print(f"Memory usage: {memory_mb:.1f} MB")
```

## Release Process

### Versioning

Noah123d uses Calendar Versioning (CalVer):
- Format: `YYYY.MINOR.PATCH`
- Example: `2025.1.0`

### Release Checklist

For maintainers:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Run full test suite
4. Build and test documentation
5. Create release tag
6. Deploy to PyPI
7. Update GitHub release

## Community Guidelines

### Code of Conduct

We follow the [Contributor Covenant](https://www.contributor-covenant.org/). Be respectful, inclusive, and professional in all interactions.

### Communication

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Pull Requests**: Code review and development discussion

### Recognition

Contributors are recognized in:
- `CONTRIBUTORS.md` file
- Release notes
- Documentation acknowledgments

## Getting Help

If you need help:

1. Check existing documentation
2. Search closed issues
3. Ask in [GitHub Discussions](https://github.com/42sol-eu/noah123d/discussions)
4. Create a new issue if needed

## License

By contributing to Noah123d, you agree that your contributions will be licensed under the same MIT License that covers the project.
