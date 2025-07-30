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


