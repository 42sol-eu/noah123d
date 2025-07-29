# 3MF File Analyzer Documentation

## Overview

The Noah123D library now includes a comprehensive 3MF file analyzer that can extract detailed information about models including center of mass, dimensions, volume, surface area, and mesh quality metrics. This is perfect for inspecting 3MF files before 3D printing or for analyzing model properties.

## New Analyzer Features

### 🔍 Analysis Capabilities

- **Model Geometry**: Center of mass, dimensions, bounding box
- **Mesh Properties**: Volume, surface area, vertex/triangle counts
- **Quality Metrics**: Mesh validation, degenerate triangle detection
- **File Information**: Archive contents, file size, object count
- **Comparison Tools**: Multi-file comparison and statistics

### 📊 Output Formats

- **Rich Console**: Beautiful formatted tables and panels
- **JSON Export**: Structured data for further processing
- **Summary Statistics**: Overall and per-model metrics
- **Comparison Reports**: Side-by-side file analysis

## API Reference

### Core Classes

#### `Analysis3MF`
Main analyzer class for 3MF files:

```python
from noah123d import Analysis3MF

analyzer = Analysis3MF()
analysis = analyzer.analyze_file(Path("model.3mf"))
```

### Convenience Functions

#### `analyze_3mf(file_path)`
Complete analysis of a 3MF file:

```python
from noah123d import analyze_3mf
from pathlib import Path

analysis = analyze_3mf(Path("model.3mf"))
print(f"Objects: {analysis['summary']['object_count']}")
print(f"Total volume: {sum(m['volume'] for m in analysis['models']):.1f} mm³")
```

#### `get_model_center_of_mass(file_path, model_id=None)`
Get center of mass coordinates:

```python
from noah123d import get_model_center_of_mass

# Overall center of mass
center = get_model_center_of_mass(Path("model.3mf"))
print(f"Center: ({center[0]:.2f}, {center[1]:.2f}, {center[2]:.2f})")

# Specific model center of mass
model_center = get_model_center_of_mass(Path("model.3mf"), model_id=1)
```

#### `get_model_dimensions(file_path, model_id=None)`
Get model dimensions:

```python
from noah123d import get_model_dimensions

# Overall dimensions
dims = get_model_dimensions(Path("model.3mf"))
print(f"Size: {dims[0]:.1f} × {dims[1]:.1f} × {dims[2]:.1f} mm")

# Specific model dimensions
model_dims = get_model_dimensions(Path("model.3mf"), model_id=1)
```

## Analysis Results Structure

The analyzer returns a comprehensive dictionary with the following structure:

```python
{
    'file_path': str,           # Path to analyzed file
    'file_size': int,           # File size in bytes
    'archive_contents': [str],  # List of files in 3MF archive
    'summary': {
        'object_count': int,
        'total_vertices': int,
        'total_triangles': int,
        'overall_bounds': {
            'min': [x, y, z],
            'max': [x, y, z]
        },
        'overall_center_of_mass': [x, y, z],
        'overall_dimensions': [width, height, depth]
    },
    'models': [{
        'object_id': int,
        'object_type': str,
        'vertex_count': int,
        'triangle_count': int,
        'bounds': {'min': [x,y,z], 'max': [x,y,z]},
        'dimensions': [w, h, d],
        'center_of_mass': [x, y, z],
        'volume': float,           # mm³
        'surface_area': float      # mm²
    }]
}
```

## Usage Examples

### Example 1: Basic Analysis

```python
from noah123d import analyze_3mf
from pathlib import Path

# Analyze a 3MF file
analysis = analyze_3mf(Path("my_model.3mf"))

if 'error' not in analysis:
    print(f"File: {Path(analysis['file_path']).name}")
    print(f"Objects: {analysis['summary']['object_count']}")
    
    for model in analysis['models']:
        print(f"Model {model['object_id']}:")
        print(f"  Center: {model['center_of_mass']}")
        print(f"  Size: {model['dimensions']}")
        print(f"  Volume: {model['volume']:.1f} mm³")
```

### Example 2: Convenience Functions

```python
from noah123d import get_model_center_of_mass, get_model_dimensions
from pathlib import Path

file_path = Path("grid_model.3mf")

# Get overall properties
center = get_model_center_of_mass(file_path)
dimensions = get_model_dimensions(file_path)

print(f"Overall center of mass: {center}")
print(f"Overall dimensions: {dimensions}")

# Get individual model properties
for model_id in range(1, 5):  # Models 1-4
    model_center = get_model_center_of_mass(file_path, model_id)
    model_dims = get_model_dimensions(file_path, model_id)
    
    if model_center and model_dims:
        print(f"Model {model_id}: center={model_center}, size={model_dims}")
```

### Example 3: File Comparison

```python
from noah123d import Analysis3MF
from pathlib import Path

analyzer = Analysis3MF()
files = [Path("model1.3mf"), Path("model2.3mf"), Path("model3.3mf")]

for file_path in files:
    analysis = analyzer.analyze_file(file_path)
    if 'error' not in analysis:
        summary = analysis['summary']
        total_volume = sum(m['volume'] for m in analysis['models'])
        
        print(f"{file_path.name}:")
        print(f"  Objects: {summary['object_count']}")
        print(f"  Volume: {total_volume:.1f} mm³")
        print(f"  Dimensions: {summary['overall_dimensions']}")
```

### Example 4: Quality Analysis

```python
from noah123d import Analysis3MF

analyzer = Analysis3MF()
analysis = analyzer.analyze_file(Path("complex_model.3mf"))

if 'error' not in analysis:
    for model in analysis['models']:
        print(f"Model {model['object_id']} Quality:")
        print(f"  Vertices: {model['vertex_count']:,}")
        print(f"  Triangles: {model['triangle_count']:,}")
        print(f"  Surface Area: {model['surface_area']:.1f} mm²")
        print(f"  Volume: {model['volume']:.1f} mm³")
        
        # Calculate density (if known material)
        if model['volume'] > 0:
            density = model['surface_area'] / model['volume']
            print(f"  Surface/Volume Ratio: {density:.2f}")
```

## Advanced Features

### Rich Console Output

The analyzer includes beautiful console output using the Rich library:

```python
from noah123d.examples.analyzer_3mf import Model3MFAnalyzer

analyzer = Model3MFAnalyzer()
analysis = analyzer.analyze_3mf_file(Path("model.3mf"))
analyzer.print_analysis(analysis, detailed=True)
```

This creates formatted tables showing:
- File information panel
- Summary statistics
- Individual model details table
- Mesh quality analysis table

### JSON Export

Export analysis results for further processing:

```python
import json
from noah123d import analyze_3mf

analysis = analyze_3mf(Path("model.3mf"))
with open("analysis_report.json", "w") as f:
    json.dump(analysis, f, indent=2)
```

### Batch Analysis

Analyze multiple files efficiently:

```python
from noah123d import Analysis3MF
from pathlib import Path

analyzer = Analysis3MF()
results = {}

for mf_file in Path(".").glob("*.3mf"):
    analysis = analyzer.analyze_file(mf_file)
    if 'error' not in analysis:
        results[mf_file.name] = {
            'objects': analysis['summary']['object_count'],
            'volume': sum(m['volume'] for m in analysis['models']),
            'center': analysis['summary']['overall_center_of_mass']
        }

# Compare results
for filename, data in results.items():
    print(f"{filename}: {data['objects']} objects, {data['volume']:.1f} mm³")
```

## Integration with Grid Layouts

The analyzer works seamlessly with grid-generated 3MF files:

```python
from noah123d import stl_to_3mf_grid, analyze_3mf

# Create a grid layout
stl_to_3mf_grid("part.stl", "grid.3mf", count=9, grid_cols=3)

# Analyze the result
analysis = analyze_3mf(Path("grid.3mf"))
print(f"Created {analysis['summary']['object_count']} objects")

# Check individual object positions
for model in analysis['models']:
    center = model['center_of_mass']
    print(f"Object {model['object_id']} at ({center[0]:.1f}, {center[1]:.1f})")
```

## Performance

The analyzer is optimized for large 3MF files:

- **Fast Processing**: Analyzes complex models in seconds
- **Memory Efficient**: Streams data without loading entire models
- **Scalable**: Handles files with hundreds of objects
- **Accurate Calculations**: Precise volume and surface area computations

## Applications

Perfect for:

- **Pre-Print Inspection**: Verify model integrity before 3D printing
- **Quality Control**: Check mesh quality and detect issues
- **Production Planning**: Calculate material usage and print time estimates
- **Model Optimization**: Identify oversized or problematic models
- **Assembly Analysis**: Understand part positioning and relationships

## Examples Available

Run these examples to see the analyzer in action:

```bash
# Comprehensive analyzer demo
python examples/analyzer_3mf.py

# Basic analysis functions
python examples/example_3mf_analysis.py

# Grid layout with analysis
python examples/example_grid_layout.py
```

The analyzer provides everything you need to understand and validate your 3MF files before manufacturing! 🎯
