# Multi-STL Assembly Guide

This guide demonstrates how to create 3MF assemblies from multiple STL files with specified counts for each component using the noah123d library.

## Overview

The `multi_stl_to_3mf()` function allows you to combine multiple different STL files into a single 3MF assembly, specifying how many copies of each part should be included. This is perfect for creating assemblies, kits, or collections of related parts.

## Basic Usage

```python
from noah123d import multi_stl_to_3mf

# Define your assembly components
stl_objects = [
    {'path': 'base.stl', 'count': 1, 'name': 'Base'},
    {'path': 'screw.stl', 'count': 4, 'name': 'Screw'},
    {'path': 'washer.stl', 'count': 4, 'name': 'Washer'},
    {'path': 'nut.stl', 'count': 4}  # name is optional
]

# Create the assembly
success = multi_stl_to_3mf(stl_objects, 'assembly.3mf')
```

## STL Object Specification

Each STL object is defined by a dictionary with the following keys:

- **`path`** (required): Path to the STL file (string or Path object)
- **`count`** (optional): Number of copies to create (default: 1)
- **`name`** (optional): Custom name for the object (default: filename without extension)

## Layout Modes

### Grid Layout (Default)
Arranges objects in an optimal grid pattern:
```python
multi_stl_to_3mf(stl_objects, 'grid_assembly.3mf', layout_mode='grid')
```

### Linear Layout
Arranges all objects in a single horizontal line:
```python
multi_stl_to_3mf(stl_objects, 'linear_assembly.3mf', layout_mode='linear')
```

### Stack Layout
Stacks all objects vertically (Z-axis):
```python
multi_stl_to_3mf(stl_objects, 'stack_assembly.3mf', layout_mode='stack')
```

## Advanced Options

### Spacing Control
Control the spacing between objects:
```python
multi_stl_to_3mf(
    stl_objects,
    'spaced_assembly.3mf',
    spacing_factor=1.5,  # 50% extra space between objects
    center_layout=True   # Center the entire layout
)
```

### Using STLConverter Class
For more control and access to statistics:
```python
from noah123d import STLConverter

converter = STLConverter(include_metadata=True, validate=True)

success = converter.convert_multiple_stl_with_counts(
    stl_objects=stl_objects,
    output_path='advanced_assembly.3mf',
    layout_mode='grid',
    spacing_factor=1.2,
    center_layout=True
)

# Get conversion statistics
stats = converter.get_conversion_stats()
print(f"Total objects: {stats['advanced_assembly.3mf']['total_objects']}")
```

## Complete Example

```python
from pathlib import Path
from noah123d import multi_stl_to_3mf

def create_printer_assembly():
    """Create a 3D printer part assembly."""
    
    # Define the assembly components
    assembly_parts = [
        {'path': 'printer_frame.stl', 'count': 1, 'name': 'Frame'},
        {'path': 'corner_bracket.stl', 'count': 8, 'name': 'Corner_Bracket'},
        {'path': 'stepper_mount.stl', 'count': 4, 'name': 'Stepper_Mount'},
        {'path': 'belt_tensioner.stl', 'count': 2, 'name': 'Belt_Tensioner'},
        {'path': 'filament_guide.stl', 'count': 1, 'name': 'Filament_Guide'}
    ]
    
    # Check if all files exist
    valid_parts = []
    for part in assembly_parts:
        if Path(part['path']).exists():
            valid_parts.append(part)
            print(f\"✓ {part['name']}: {part['count']} copies\")
        else:
            print(f\"⚠ Missing: {part['path']}\")
    
    if not valid_parts:
        print(\"No STL files found!\")
        return False
    
    # Create the assembly with grid layout
    success = multi_stl_to_3mf(
        stl_objects=valid_parts,
        output_path='printer_assembly.3mf',
        layout_mode='grid',
        spacing_factor=1.3,  # 30% spacing for clear separation
        center_layout=True,
        include_metadata=True
    )
    
    if success:
        print(\"🎉 Assembly created: printer_assembly.3mf\")
        
        # Calculate total parts
        total_parts = sum(part['count'] for part in valid_parts)
        print(f\"Total parts in assembly: {total_parts}\")
        return True
    else:
        print(\"❌ Failed to create assembly\")
        return False

if __name__ == \"__main__\":
    create_printer_assembly()
```

## Error Handling

The function includes comprehensive error handling:

```python
from noah123d import multi_stl_to_3mf, STLConverter

# Example with error handling
stl_objects = [
    {'path': 'existing_file.stl', 'count': 2},
    {'path': 'missing_file.stl', 'count': 1}  # This will cause an error
]

try:
    success = multi_stl_to_3mf(stl_objects, 'test_assembly.3mf')
    if not success:
        # Check for errors
        converter = STLConverter()
        stats = converter.get_conversion_stats()
        if 'test_assembly.3mf' in stats and 'error' in stats['test_assembly.3mf']:
            print(f\"Error: {stats['test_assembly.3mf']['error']}\")
except Exception as e:
    print(f\"Conversion failed: {e}\")
```

## Metadata Generation

When `include_metadata=True` (default), the function generates detailed metadata including:

- Source file information for each STL
- Object counts and dimensions
- Conversion performance statistics
- Object placement coordinates
- Layout configuration details

The metadata is stored in the 3MF file and can be accessed by 3D printing software or other tools.

## Performance Tips

1. **File Validation**: Set `validate=False` in STLConverter for faster processing if you're confident your STL files are valid
2. **Large Assemblies**: For assemblies with many objects, consider using `layout_mode='linear'` for simpler calculations
3. **Memory Usage**: Very large STL files with high counts may require substantial memory
4. **Spacing**: Use appropriate `spacing_factor` values to prevent objects from overlapping in the final layout

## Use Cases

- **Product Assemblies**: Create kits with all required parts
- **Replacement Parts**: Group different quantities of spare parts
- **Educational Sets**: Combine learning materials with varying quantities
- **Prototyping**: Test different part combinations and layouts
- **Manufacturing**: Prepare parts for batch production

## See Also

- `stl_to_3mf_grid()` - For multiple copies of the same STL file
- `batch_stl_to_3mf()` - For converting multiple STL files to separate 3MF files
- `stl_to_3mf()` - For simple single STL to 3MF conversion
