# API reference

Complete API documentation for Noah123d classes and functions.

## Overview

Noah123d provides a clean, modular API for STL to 3MF conversion, grid layouts, and 3MF analysis.

## Core modules

### Main functions

High-level convenience functions for common tasks:

- **[`stl_to_3mf()`](#stl_to_3mf)** - Simple STL to 3MF conversion
- **[`stl_to_3mf_grid()`](#stl_to_3mf_grid)** - Grid layout creation
- **[`analyze_3mf()`](#analyze_3mf)** - 3MF file analysis
- **[`get_stl_info()`](#get_stl_info)** - STL file information

### Core classes

Low-level classes for advanced control:

- **[`STLConverter`](converters.md)** - STL conversion engine
- **[`Archive`](Archive.md)** - 3MF archive management
- **[`Model`](model.md)** - 3D model handling
- **[`Directory`](directory.md)** - 3MF directory structure
- **[`Analysis3MF`](analyzer.md)** - 3MF analysis engine

## Quick reference

### Import statements

```python
# High-level functions
from noah123d import (
    stl_to_3mf,
    stl_to_3mf_grid,
    analyze_3mf,
    get_stl_info
)

# Core classes
from noah123d import (
    STLConverter,
    Archive,
    Model,
    Directory,
    Analysis3MF
)

# Rich output functions
from noah123d import (
    analyze_3mf_rich,
    analyze_3mf_json
)
```

## Main functions

### `stl_to_3mf()`

::: noah123d.stl_to_3mf
    options:
        show_source: false
        show_signature_annotations: true

Simple STL to 3MF conversion function.

**Parameters:**

- **stl_path** (`str | Path`) - Path to input STL file
- **output_path** (`str | Path`) - Path for output 3MF file  
- **validate** (`bool`) - Whether to validate STL file (default: `False`)
- **include_metadata** (`bool`) - Include conversion metadata (default: `True`)

**Returns:**

- **bool** - `True` if conversion successful, `False` otherwise

**Example:**

```python
from noah123d import stl_to_3mf

success = stl_to_3mf("model.stl", "output.3mf", validate=True)
if success:
    print("Conversion successful!")
```

### `stl_to_3mf_grid()`

::: noah123d.stl_to_3mf_grid
    options:
        show_source: false
        show_signature_annotations: true

Create grid layouts with multiple copies.

**Parameters:**

- **stl_path** (`str | Path`) - Path to input STL file
- **output_path** (`str | Path`) - Path for output 3MF file
- **count** (`int`) - Number of copies to create
- **grid_cols** (`int | None`) - Number of columns (auto-calculated if `None`)
- **spacing_factor** (`float`) - Spacing multiplier (default: `1.1`)
- **center_grid** (`bool`) - Center grid at origin (default: `True`)

**Returns:**

- **bool** - `True` if conversion successful, `False` otherwise

**Example:**

```python
from noah123d import stl_to_3mf_grid

# Create 2×2 grid
success = stl_to_3mf_grid(
    stl_path="part.stl",
    output_path="grid.3mf",
    count=4,
    grid_cols=2,
    spacing_factor=1.2
)
```

### `analyze_3mf()`

::: noah123d.analyze_3mf
    options:
        show_source: false
        show_signature_annotations: true

Analyze 3MF files and extract model information.

**Parameters:**

- **file_path** (`str | Path`) - Path to 3MF file

**Returns:**

- **Dict[str, Any]** - Analysis results with model information

**Example:**

```python
from noah123d import analyze_3mf

analysis = analyze_3mf("model.3mf")
print(f"Objects: {analysis['summary']['object_count']}")
print(f"Dimensions: {analysis['summary']['overall_dimensions']}")
```

### `get_stl_info()`

::: noah123d.get_stl_info
    options:
        show_source: false
        show_signature_annotations: true

Get detailed information about STL files.

**Parameters:**

- **stl_path** (`str | Path`) - Path to STL file

**Returns:**

- **Dict[str, Any] | None** - STL information or `None` if error

**Example:**

```python
from noah123d import get_stl_info

info = get_stl_info("model.stl")
if info:
    print(f"Triangles: {info['triangle_count']:,}")
    print(f"Vertices: {info['vertex_count']:,}")
    print(f"Dimensions: {info['dimensions']}")
```

## Rich output functions

### `analyze_3mf_rich()`

Beautiful console output with Rich formatting:

```python
from noah123d import analyze_3mf_rich

# Display analysis with rich formatting
analyze_3mf_rich("grid.3mf")
```

### `analyze_3mf_json()`

Export analysis results to JSON:

```python
from noah123d import analyze_3mf_json

# Export to JSON file
analyze_3mf_json("model.3mf", "analysis.json")
```

## Type hints

Noah123d uses comprehensive type hints for better IDE support:

```python
from typing import Union, Optional, Dict, List, Any
from pathlib import Path

# Path types
PathLike = Union[str, Path]

# Analysis result type
AnalysisResult = Dict[str, Any]

# STL info type
STLInfo = Optional[Dict[str, Any]]
```

## Error handling

All functions use consistent error handling patterns:

```python
from noah123d import stl_to_3mf, analyze_3mf

# Conversion with error handling
try:
    success = stl_to_3mf("input.stl", "output.3mf")
    if not success:
        print("Conversion failed - check file paths and format")
except FileNotFoundError:
    print("Input file not found")
except Exception as e:
    print(f"Unexpected error: {e}")

# Analysis with error handling
analysis = analyze_3mf("model.3mf")
if 'error' in analysis:
    print(f"Analysis failed: {analysis['error']}")
else:
    print("Analysis successful")
```

## Performance tips

### Memory management

For large files or grids:

```python
from noah123d import STLConverter

# Use context manager for automatic cleanup
converter = STLConverter()
try:
    success = converter.convert_with_copies(
        "large_model.stl", "output.3mf", count=100
    )
finally:
    # Explicit cleanup if needed
    del converter
```

### Batch processing

Process multiple files efficiently:

```python
from noah123d import STLConverter

converter = STLConverter()
files = ["model1.stl", "model2.stl", "model3.stl"]

for stl_file in files:
    output_file = stl_file.replace(".stl", ".3mf")
    converter.convert(stl_file, output_file)
```

## Constants and enums

### Default values

```python
# Default spacing factor for grids
DEFAULT_SPACING_FACTOR = 1.1

# Default grid centering
DEFAULT_CENTER_GRID = True

# Default metadata inclusion
DEFAULT_INCLUDE_METADATA = True

# Default validation
DEFAULT_VALIDATE = False
```

## Next steps

Explore the detailed documentation for each module:

- **[STLConverter](converters.md)** - Core conversion functionality
- **[Archive](Archive.md)** - 3MF file format handling
- **[Model](model.md)** - 3D model operations
- **[Analysis3MF](analyzer.md)** - Analysis and statistics
