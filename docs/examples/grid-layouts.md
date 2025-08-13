# Grid layout feature documentation

## Overview

The Noah123d STL converter now supports creating grid layouts with multiple copies of the same object. This feature automatically calculates spacing based on the object's dimensions to prevent overlapping and creates perfectly arranged grids for 3D printing.

## New features added

### 🔲 grid layout functions

#### `stl_to_3mf_grid()`
Simple function for creating grid layouts:

```python
from noah123d import stl_to_3mf_grid

# Create a 2x2 grid with 4 copies
success = stl_to_3mf_grid(
    stl_path="part.stl",
    output_path="grid.3mf", 
    count=4,
    grid_cols=2,
    spacing_factor=1.2,  # 20% spacing between parts
    center_grid=True
)
```

#### `STLConverter.convert_with_copies()`
Advanced method for grid conversion with detailed control:

```python
from noah123d import STLConverter

converter = STLConverter(include_metadata=True)
success = converter.convert_with_copies(
    stl_path="part.stl",
    output_path="grid.3mf",
    count=9,
    grid_cols=3,
    spacing_factor=1.1,
    center_grid=True
)

# Get detailed statistics
stats = converter.get_conversion_stats()
```

## Parameters

### Core parameters
- **`count`**: Total number of copies to create
- **`grid_cols`**: Number of columns (auto-calculated if None)
- **`spacing_factor`**: Spacing multiplier (1.0 = touching, 1.1 = 10% gap)
- **`center_grid`**: Center the grid around origin (default: True)

### Spacing factor examples
- `1.0` - Objects touching (no gap)
- `1.1` - 10% spacing (recommended minimum)
- `1.2` - 20% spacing (good for most prints)
- `1.5` - 50% spacing (wide spacing)

## Grid layout logic

The system automatically:

1. **Calculates object Dimensions**: Analyzes STL bounding box
2. **Determines grid Layout**: Optimal rows×columns for given count
3. **Computes Spacing**: Based on object size and spacing factor
4. **Positions Objects**: Places copies without overlapping
5. **Centers Grid**: Optional centering around origin

### Auto-Layout examples
- 4 copies → 2×2 grid
- 6 copies → 3×2 grid  
- 9 copies → 3×3 grid
- 12 copies → 4×3 grid

## Usage examples

### Example 1: Simple 2×2 grid
```python
from noah123d import stl_to_3mf_grid

# Create 4 copies in a 2x2 grid with 20% spacing
stl_to_3mf_grid("part.stl", "quad.3mf", count=4, grid_cols=2, spacing_factor=1.2)
```

### Example 2: Single row layout
```python
# Create 5 copies in a single row
stl_to_3mf_grid("part.stl", "row.3mf", count=5, grid_cols=5, spacing_factor=1.5)
```

### Example 3: Auto-layout
```python
# Let the system choose optimal layout for 6 copies
stl_to_3mf_grid("part.stl", "auto.3mf", count=6, spacing_factor=1.1)
```

### Example 4: Advanced control
```python
from noah123d import STLConverter

converter = STLConverter(include_metadata=True, validate=True)

# Create custom grid with detailed statistics
success = converter.convert_with_copies(
    stl_path="complex_part.stl",
    output_path="production_grid.3mf",
    count=12,
    grid_cols=4,  # 4×3 grid
    spacing_factor=1.15,
    center_grid=True
)

if success:
    stats = converter.get_conversion_stats()
    print(f"Created {stats['copies']} objects")
    print(f"Grid layout: {stats['grid_layout']}")
    print(f"Total triangles: {stats['triangles']:,}")
```

## Output files

Grid conversion creates 3MF files with:

- ✅ **Multiple Objects**: Each copy as separate object
- ✅ **Proper Positioning**: No overlapping, optimal spacing  
- ✅ **Grid Metadata**: Detailed conversion report
- ✅ **Build Items**: All objects included in build plate

### Metadata information
The generated 3MF includes metadata with:
- Grid configuration (rows×columns)
- Spacing factor used
- Object positions (X, Y, Z coordinates)
- Performance statistics
- Conversion details

## Performance

Grid conversion performance:
- **~80,000 triangles/second** for grid operations
- Efficient memory usage (reuses geometry)
- Fast positioning calculations
- Scales well with object count

### Test results
Based on tile_2x2_borde.stl (33,448 triangles):

| Grid Size | Objects | Total Triangles | File Size | Time |
|-----------|---------|----------------|-----------|------|
| 2×2       | 4       | 133,792        | 2.6 MB    | 3.6s |
| 3×3       | 9       | 301,032        | 5.9 MB    | -    |
| 4×3       | 12      | 401,376        | 7.8 MB    | 3.1s |

## Applications

Perfect for:
- **3D Printing Arrays**: Multiple small parts on one print bed
- **Production Runs**: Batch manufacturing layouts
- **Assembly Kits**: Organized part arrangements
- **Prototyping**: Quick test arrays with different spacings

## File examples

Run the examples to see the grid functionality:

```bash
# Test all grid layouts
python examples/example_grid_layout.py

# Creates files like:
# - grid_2x2.3mf (2×2 grid)
# - grid_3x3.3mf (3×3 grid) 
# - grid_1x5.3mf (single row)
# - advanced_*.3mf (custom configurations)
```

## Integration

The grid feature integrates seamlessly with existing noah123d workflow:

1. **STL Analysis**: Uses existing `get_stl_info()` for dimensions
2. **3MF Creation**: Uses `Archive`, `Directory`, `model` classes
3. **Object Management**: Leverages existing object handling
4. **Metadata**: Enhanced metadata with grid information

This provides a complete solution from single STL files to production-ready grid layouts! 🎯
