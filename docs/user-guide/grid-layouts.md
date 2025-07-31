# Grid layouts

Grid layouts are Noah123d's flagship feature, allowing you to create optimized arrangements of multiple copies for 3D printing and manufacturing workflows.

## Overview

The grid layout system automatically:

1. **Calculates object dimensions**: Analyzes STL bounding box
2. **Determines grid layout**: Optimal rows×columns for given count  
3. **Computes spacing**: Based on object size and spacing factor
4. **Positions objects**: Places copies without overlapping
5. **Centers grid**: Optional centering around origin

## Core functions

### `stl_to_3mf_grid()`

Simple function for creating grid layouts:

```python
from noah123d import stl_to_3mf_grid

success = stl_to_3mf_grid(
    stl_path="part.stl",
    output_path="grid.3mf",
    count=4,                    # Total number of copies
    grid_cols=2,               # Number of columns (optional)
    spacing_factor=1.2,        # Spacing multiplier
    center_grid=True           # Center at origin
)
```

### `STLConverter.convert_with_copies()`

Advanced method with detailed control:

```python
from noah123d import STLConverter

converter = STLConverter(include_metadata=True, validate=True)
success = converter.convert_with_copies(
    stl_path="part.stl",
    output_path="grid.3mf",
    count=9,
    grid_cols=3,
    spacing_factor=1.1,
    center_grid=True
)

# Get conversion statistics
if success:
    stats = converter.get_conversion_stats()
    print(f"Created {stats['copies']} objects")
    print(f"Grid layout: {stats['grid_layout']}")
```

## Parameters

### Core parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `count` | `int` | Required | Total number of copies to create |
| `grid_cols` | `int` | `None` | Number of columns (auto-calculated if None) |
| `spacing_factor` | `float` | `1.1` | Spacing multiplier (1.0 = touching) |
| `center_grid` | `bool` | `True` | Center the grid around origin |

### Spacing factor guide

| Factor | Spacing | Use Case |
|--------|---------|----------|
| `1.0` | 0% (touching) | Maximum density, parts touching |
| `1.1` | 10% gap | Recommended minimum for 3D printing |
| `1.2` | 20% gap | Good for most applications |
| `1.5` | 50% gap | Wide spacing for large parts |
| `2.0` | 100% gap | Maximum spacing, double width |

## Grid layout logic

### Automatic layout calculation

When `grid_cols` is not specified, Noah123d calculates the optimal layout:

```python
import math

def calculate_optimal_layout(count):
    cols = math.ceil(math.sqrt(count))
    rows = math.ceil(count / cols)
    return (rows, cols)

# Examples:
# 4 objects → 2×2 grid
# 6 objects → 3×2 grid  
# 9 objects → 3×3 grid
# 12 objects → 4×3 grid
```

### Grid position calculation

Objects are positioned using:

```python
def calculate_position(row, col, spacing_x, spacing_y, center_grid):
    x = col * spacing_x
    y = row * spacing_y
    
    if center_grid:
        # Offset to center the grid
        grid_width = (cols - 1) * spacing_x
        grid_height = (rows - 1) * spacing_y
        x -= grid_width / 2
        y -= grid_height / 2
    
    return (x, y, 0)  # Z always 0
```

## Examples

### Basic grid patterns

=== "2×2 Grid"

    ```python
    from noah123d import stl_to_3mf_grid
    
    # Create 4 copies in 2×2 arrangement
    stl_to_3mf_grid(
        stl_path="part.stl",
        output_path="grid_2x2.3mf",
        count=4,
        grid_cols=2,
        spacing_factor=1.2
    )
    ```

=== "3×3 Grid"

    ```python
    # Create 9 copies in 3×3 arrangement
    stl_to_3mf_grid(
        stl_path="part.stl",
        output_path="grid_3x3.3mf",
        count=9,
        grid_cols=3,
        spacing_factor=1.1
    )
    ```

=== "Single Row"

    ```python
    # Create 5 copies in single row
    stl_to_3mf_grid(
        stl_path="part.stl",
        output_path="row_5x1.3mf",
        count=5,
        grid_cols=5,
        spacing_factor=1.5
    )
    ```

=== "Auto Layout"

    ```python
    # Let system choose optimal layout
    stl_to_3mf_grid(
        stl_path="part.stl",
        output_path="auto_grid.3mf",
        count=6,  # Will create 3×2 grid
        spacing_factor=1.1
    )
    ```

### Advanced configurations

#### Production grid

```python
from noah123d import STLConverter

converter = STLConverter(
    include_metadata=True,
    validate=True
)

# Large production grid
success = converter.convert_with_copies(
    stl_path="production_part.stl",
    output_path="production_batch.3mf",
    count=24,
    grid_cols=6,  # 6×4 grid
    spacing_factor=1.15,
    center_grid=True
)

if success:
    stats = converter.get_conversion_stats()
    print(f"📊 Production Grid Statistics:")
    print(f"   Objects: {stats['copies']}")
    print(f"   Layout: {stats['grid_layout'][1]}×{stats['grid_layout'][0]}")
    print(f"   Triangles: {stats['triangles']:,}")
    print(f"   Time: {stats['conversion_time']:.2f}s")
```

#### Tight packing

```python
# Minimal spacing for maximum density
stl_to_3mf_grid(
    stl_path="small_part.stl",
    output_path="tight_pack.3mf",
    count=16,
    grid_cols=4,
    spacing_factor=1.05,  # Just 5% spacing
    center_grid=True
)
```

#### Wide spacing

```python
# Wide spacing for large parts or assembly
stl_to_3mf_grid(
    stl_path="large_part.stl",
    output_path="wide_spacing.3mf",
    count=4,
    grid_cols=2,
    spacing_factor=2.0,  # 100% spacing
    center_grid=True
)
```

## Performance

### Grid generation performance

Noah123d's grid system is highly optimized:

- **Geometry Reuse**: Original mesh data is reused for all copies
- **Memory Efficient**: Only transformation data stored per copy
- **Fast Positioning**: Vectorized position calculations
- **Parallel Processing**: Multi-threaded where possible

### Benchmark results

Based on `tile_2x2_borde.stl` (33,448 triangles):

| Grid Size | Objects | Triangles | File Size | Time | Rate |
|-----------|---------|-----------|-----------|------|------|
| 2×2 | 4 | 133,792 | 2.6 MB | 3.6s | 37K tri/s |
| 3×3 | 9 | 301,032 | 5.9 MB | 7.2s | 42K tri/s |
| 4×3 | 12 | 401,376 | 7.8 MB | 3.1s | 129K tri/s |
| 5×4 | 20 | 668,960 | 13.1 MB | 8.4s | 80K tri/s |

## Output analysis

### Grid metadata

Generated 3MF files include comprehensive metadata:

```python
from noah123d import analyze_3mf

analysis = analyze_3mf("grid_2x2.3mf")
metadata = analysis.get('metadata', {})

print(f"Grid Layout: {metadata.get('grid_layout')}")
print(f"Spacing Factor: {metadata.get('spacing_factor')}")
print(f"Objects: {analysis['summary']['object_count']}")
print(f"Total Dimensions: {analysis['summary']['overall_dimensions']}")
```

### Position verification

Verify object positions are correct:

```python
analysis = analyze_3mf("grid_2x2.3mf")

print("Object Positions:")
for i, model in enumerate(analysis['models']):
    center = model['center_of_mass']
    print(f"  Object {i+1}: ({center[0]:.1f}, {center[1]:.1f}, {center[2]:.1f})")

# Calculate spacing between adjacent objects
if len(analysis['models']) >= 2:
    pos1 = analysis['models'][0]['center_of_mass']
    pos2 = analysis['models'][1]['center_of_mass']
    spacing_x = abs(pos2[0] - pos1[0])
    print(f"X-axis spacing: {spacing_x:.1f} mm")
```

## Applications

### 3D printing

Perfect for 3D printing workflows:

```python
# Small parts production
stl_to_3mf_grid(
    stl_path="miniature.stl",
    output_path="mini_army.3mf",
    count=25,
    grid_cols=5,
    spacing_factor=1.1
)

# Prototype testing
stl_to_3mf_grid(
    stl_path="prototype.stl",
    output_path="test_variants.3mf",
    count=6,
    grid_cols=3,
    spacing_factor=1.5
)
```

### Manufacturing

Industrial applications:

```python
# Injection molding layout
stl_to_3mf_grid(
    stl_path="injection_part.stl",
    output_path="mold_layout.3mf",
    count=8,
    grid_cols=4,
    spacing_factor=1.3
)

# Assembly kit organization
stl_to_3mf_grid(
    stl_path="component.stl",
    output_path="assembly_kit.3mf",
    count=12,
    grid_cols=3,
    spacing_factor=1.2
)
```

## Troubleshooting

### Common issues

!!! warning "Overlapping Objects"
    If objects overlap, increase `spacing_factor`:
    ```python
    # Instead of 1.1, try 1.2 or higher
    spacing_factor=1.2
    ```

!!! tip "Grid Too Large"
    For large grids, consider splitting into multiple files:
    ```python
    # Split 24 objects into two 3×4 grids
    stl_to_3mf_grid("part.stl", "batch1.3mf", count=12, grid_cols=3)
    stl_to_3mf_grid("part.stl", "batch2.3mf", count=12, grid_cols=3)
    ```

!!! info "Memory Usage"
    For very large grids (100+ objects), monitor memory usage:
    ```python
    import psutil
    print(f"Memory usage: {psutil.virtual_memory().percent}%")
    ```

### Validation

Validate grid results:

```python
from noah123d import analyze_3mf

def validate_grid(file_path, expected_count, expected_spacing):
    analysis = analyze_3mf(file_path)
    
    # Check object count
    actual_count = analysis['summary']['object_count']
    assert actual_count == expected_count, f"Expected {expected_count}, got {actual_count}"
    
    # Check spacing (if multiple objects)
    if actual_count >= 2:
        pos1 = analysis['models'][0]['center_of_mass']
        pos2 = analysis['models'][1]['center_of_mass']
        actual_spacing = abs(pos2[0] - pos1[0])
        tolerance = expected_spacing * 0.01  # 1% tolerance
        assert abs(actual_spacing - expected_spacing) < tolerance
    
    print("✅ Grid validation passed!")

# Example validation
validate_grid("grid_2x2.3mf", expected_count=4, expected_spacing=55.0)
```

## Next steps

- **[3MF Analysis](3mf-analysis.md)** - Analyze your grids
- **[Batch Processing](batch-processing.md)** - Process multiple files
- **[API Reference](../reference/converters.md)** - Detailed API docs
