# Quick start

Get up and running with Noah123d in minutes! This guide will walk you through your first STL to 3MF conversion and grid layout creation.

## Prerequisites

Make sure you have Noah123d installed:

```bash
python3 -m pip install noah123d
```

> [!Note]
> Instead of `python3` you need to put your python executable.
> When using a `poetry` managed project use `poetry add noah123d` to add the package to your project.

## Your first conversion

### 1. simple STL to 3MF

Let's start with a basic conversion:

```python
from noah123d import stl_to_3mf

# Convert a single STL file to 3MF
success = stl_to_3mf(
    stl_path="your_model.stl",
    output_path="converted_model.3mf"
)

if success:
    print("✅ Conversion successful!")
else:
    print("❌ Conversion failed")
```

### 2. using the CLI

You can also use the command line interface:

```bash
# Basic conversion
noah convert input.stl output.3mf

# With validation
noah convert input.stl output.3mf --validate

# Show help
noah --help
```

## Grid layouts

### Create your first grid

Create a 2×2 grid with 4 copies:

```python
from noah123d import stl_to_3mf_grid

success = stl_to_3mf_grid(
    stl_path="part.stl",
    output_path="grid_2x2.3mf",
    count=4,                    # Number of copies
    grid_cols=2,               # 2 columns = 2×2 grid
    spacing_factor=1.2,        # 20% spacing between parts
    center_grid=True           # Center the grid at origin
)

print(f"Grid created: {success}")
```

### Different grid patterns

=== "Square Grid (3×3)"

    ```python
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
    stl_to_3mf_grid(
        stl_path="part.stl",
        output_path="row_layout.3mf",
        count=5,
        grid_cols=5,
        spacing_factor=1.5
    )
    ```

=== "Auto Layout"

    ```python
    # Let Noah123d choose optimal layout
    stl_to_3mf_grid(
        stl_path="part.stl",
        output_path="auto_grid.3mf",
        count=6,  # Will create 3×2 grid
        spacing_factor=1.1
    )
    ```

## Analyzing 3MF files

### Basic analysis

Analyze any 3MF file to get detailed information:

```python
from noah123d import analyze_3mf

# Analyze a 3MF file
analysis = analyze_3mf("model.3mf")

# Print summary
summary = analysis['summary']
print(f"Objects: {summary['object_count']}")
print(f"Dimensions: {summary['overall_dimensions']}")
print(f"Center of mass: {summary['overall_center_of_mass']}")

# Print individual objects
for i, model in enumerate(analysis['models']):
    print(f"Object {i+1}: {model['dimensions']}")
```

### Rich console output

For beautiful formatted output:

```python
from noah123d import analyze_3mf_rich

# Analyze and display with rich formatting
analyze_3mf_rich("grid_2x2.3mf")
```

## Complete example

Here's a complete workflow from STL to analysis:

```python
from noah123d import stl_to_3mf_grid, analyze_3mf, STLConverter

# 1. create a grid layout
print("📐 Creating grid layout...")
success = stl_to_3mf_grid(
    stl_path="input.stl",
    output_path="production_grid.3mf",
    count=12,
    grid_cols=4,  # 4×3 grid
    spacing_factor=1.15,
    center_grid=True
)

if success:
    print("✅ Grid created successfully!")
    
    # 2. analyze the result
    print("\n🔍 Analyzing the grid...")
    analysis = analyze_3mf("production_grid.3mf")
    
    # 3. print results
    summary = analysis['summary']
    print(f"📊 Created {summary['object_count']} objects")
    print(f"📏 Total dimensions: {summary['overall_dimensions']}")
    print(f"📦 File size: {analysis['file_size']:,} bytes")
    
    # 4. get detailed statistics
    converter = STLConverter(include_metadata=True)
    stats = converter.get_conversion_stats()
    if stats:
        print(f"🚀 Triangles: {stats.get('triangles', 'N/A'):,}")
        print(f"⏱️  Time: {stats.get('conversion_time', 'N/A'):.2f}s")

else:
    print("❌ Grid creation failed")
```

## CLI examples

### Basic commands

```bash
# Convert single file
noah convert model.stl output.3mf

# Create grid layout
noah grid model.stl grid.3mf --count 4 --cols 2 --spacing 1.2

# Analyze 3MF file
noah analyze model.3mf

# Batch convert directory
noah batch-convert *.stl --output-dir converted/
```

### Advanced CLI usage

```bash
# Grid with custom settings
noah grid part.stl production.3mf \
    --count 12 \
    --cols 4 \
    --spacing 1.15 \
    --center \
    --validate

# Analyze with rich output
noah analyze grid.3mf --rich --export analysis.json

# Convert with metadata
noah convert model.stl output.3mf --metadata --validate
```

## Next steps

Now that you've completed your first conversions:

### Learn more

1. **[Basic usage](basic-usage.md)** - understand core concepts
2. **[Grid layouts](../user-guide/grid-layouts.md)** - master grid configuration
3. **[3MF analysis](../user-guide/3mf-analysis.md)** - deep dive into analysis features
4. **[API reference](../reference/index.md)** - complete function documentation

### Try examples

Explore the example files:

```bash
# Run the example scripts
cd examples/
python example_3mf.py
python example_grid_layout.py
python example_advanced_usage.py
```

### Join the community

- **Issues**: [Report problems](https://github.com/42sol-eu/noah123d/issues)
- **Discussions**: [Ask questions](https://github.com/42sol-eu/noah123d/discussions)
- **Contributing**: [Contribute code](../development/contributing.md)

## Troubleshooting

### Common first-time issues

!!! warning "File Not Found"
    Make sure your STL file path is correct:
    ```python
    from pathlib import Path
    stl_file = Path("your_model.stl")
    if not stl_file.exists():
        print(f"File not found: {stl_file}")
    ```

!!! tip "Large Files"
    For large STL files, consider using validation:
    ```python
    from noah123d import STLConverter
    converter = STLConverter(validate=True)
    converter.convert("large_model.stl", "output.3mf")
    ```

!!! info "Grid Spacing"
    Start with `spacing_factor=1.1` (10% gap) for most applications. Increase for more spacing, decrease for tighter packing.

Happy converting! 🚀
