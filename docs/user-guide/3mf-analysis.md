# 3MF Analysis

Noah123d provides comprehensive analysis tools for 3MF files, allowing you to inspect geometry, metadata, and grid layouts.

## Overview

The analysis system provides:

1. **File Structure Analysis**: Internal 3MF archive inspection
2. **Geometry Analysis**: Object dimensions, triangles, volumes
3. **Grid Analysis**: Layout verification and spacing calculations
4. **Metadata Extraction**: Custom properties and conversion statistics
5. **Validation**: File integrity and format compliance

## Core Functions

### `analyze_3mf()`

Main analysis function for comprehensive file inspection:

```python
from noah123d import analyze_3mf

# Analyze a 3MF file
analysis = analyze_3mf("grid_2x2.3mf")

# Print summary
print(f"Objects: {analysis['summary']['object_count']}")
print(f"Total Triangles: {analysis['summary']['total_triangles']:,}")
print(f"File Size: {analysis['summary']['file_size_mb']:.1f} MB")
print(f"Overall Dimensions: {analysis['summary']['overall_dimensions']}")
```

### `Analyzer3MF` Class

Advanced analysis with detailed control:

```python
from noah123d import Analyzer3MF

analyzer = Analyzer3MF()
result = analyzer.analyze_file("production_batch.3mf")

if result['success']:
    analysis = result['analysis']
    
    # Get detailed model information
    for i, model in enumerate(analysis['models']):
        print(f"Model {i+1}:")
        print(f"  Triangles: {model['triangle_count']:,}")
        print(f"  Volume: {model['volume']:.2f} mm³")
        print(f"  Center: {model['center_of_mass']}")
        print(f"  Bounds: {model['bounding_box']}")
```

## Analysis Results

### Summary Information

```python
analysis = analyze_3mf("grid_3x3.3mf")
summary = analysis['summary']

print("📊 File Summary:")
print(f"   Objects: {summary['object_count']}")
print(f"   Total Triangles: {summary['total_triangles']:,}")
print(f"   File Size: {summary['file_size_mb']:.1f} MB")
print(f"   Creation Time: {summary.get('creation_time', 'Unknown')}")
```

### Individual Model Analysis

```python
# Analyze each model individually
for i, model in enumerate(analysis['models']):
    print(f"\n🔍 Model {i+1} Analysis:")
    print(f"   Triangles: {model['triangle_count']:,}")
    print(f"   Volume: {model['volume']:.2f} mm³")
    print(f"   Surface Area: {model['surface_area']:.2f} mm²")
    print(f"   Center of Mass: {model['center_of_mass']}")
    
    # Bounding box
    bbox = model['bounding_box']
    print(f"   Dimensions: {bbox['width']:.1f} × {bbox['height']:.1f} × {bbox['depth']:.1f} mm")
```

### Metadata Analysis

```python
# Extract metadata
metadata = analysis.get('metadata', {})

if metadata:
    print("📋 Metadata:")
    print(f"   Creator: {metadata.get('creator', 'Unknown')}")
    print(f"   Creation Tool: {metadata.get('creation_tool', 'Unknown')}")
    print(f"   Grid Layout: {metadata.get('grid_layout', 'N/A')}")
    print(f"   Spacing Factor: {metadata.get('spacing_factor', 'N/A')}")
    print(f"   Original STL: {metadata.get('source_stl', 'Unknown')}")
```

## Grid Analysis

### Layout Verification

For grid-generated 3MF files, verify the layout:

```python
def analyze_grid_layout(file_path):
    analysis = analyze_3mf(file_path)
    models = analysis['models']
    
    if len(models) < 2:
        print("Single object, no grid analysis possible")
        return
    
    # Calculate grid dimensions
    positions = [model['center_of_mass'] for model in models]
    x_positions = sorted(set(round(pos[0], 1) for pos in positions))
    y_positions = sorted(set(round(pos[1], 1) for pos in positions))
    
    grid_cols = len(x_positions)
    grid_rows = len(y_positions)
    
    print(f"🔢 Grid Layout Analysis:")
    print(f"   Detected Grid: {grid_rows}×{grid_cols}")
    print(f"   Total Objects: {len(models)}")
    print(f"   Expected Objects: {grid_rows * grid_cols}")
    
    # Calculate spacing
    if len(x_positions) > 1:
        x_spacing = x_positions[1] - x_positions[0]
        print(f"   X-axis Spacing: {x_spacing:.1f} mm")
    
    if len(y_positions) > 1:
        y_spacing = y_positions[1] - y_positions[0]
        print(f"   Y-axis Spacing: {y_spacing:.1f} mm")

# Example usage
analyze_grid_layout("grid_2x2.3mf")
```

### Position Analysis

```python
def analyze_object_positions(file_path):
    analysis = analyze_3mf(file_path)
    
    print("📍 Object Positions:")
    for i, model in enumerate(analysis['models']):
        pos = model['center_of_mass']
        print(f"   Object {i+1}: ({pos[0]:6.1f}, {pos[1]:6.1f}, {pos[2]:6.1f})")
    
    # Check for overlaps
    positions = [model['center_of_mass'] for model in analysis['models']]
    bboxes = [model['bounding_box'] for model in analysis['models']]
    
    overlaps = []
    for i in range(len(positions)):
        for j in range(i+1, len(positions)):
            # Simple overlap check using bounding boxes
            bbox1, bbox2 = bboxes[i], bboxes[j]
            pos1, pos2 = positions[i], positions[j]
            
            # Calculate distance between centers
            distance = ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
            min_distance = (bbox1['width'] + bbox2['width']) / 2
            
            if distance < min_distance * 0.9:  # 10% tolerance
                overlaps.append((i+1, j+1))
    
    if overlaps:
        print(f"⚠️  Potential overlaps detected: {overlaps}")
    else:
        print("✅ No overlaps detected")

# Example usage
analyze_object_positions("tight_pack.3mf")
```

## Performance Analysis

### Conversion Statistics

```python
def analyze_performance(file_path):
    analysis = analyze_3mf(file_path)
    metadata = analysis.get('metadata', {})
    
    if 'conversion_time' in metadata:
        total_triangles = analysis['summary']['total_triangles']
        conversion_time = metadata['conversion_time']
        
        print("⚡ Performance Analysis:")
        print(f"   Conversion Time: {conversion_time:.2f}s")
        print(f"   Processing Rate: {total_triangles/conversion_time:,.0f} triangles/sec")
        print(f"   File Size: {analysis['summary']['file_size_mb']:.1f} MB")
        print(f"   Size per Object: {analysis['summary']['file_size_mb']/analysis['summary']['object_count']:.2f} MB")

# Example usage
analyze_performance("production_batch.3mf")
```

### Memory Usage

```python
import psutil
import os

def analyze_memory_usage(file_path):
    file_size = os.path.getsize(file_path) / (1024**2)  # MB
    
    print("💾 Memory Analysis:")
    print(f"   File Size: {file_size:.1f} MB")
    print(f"   Current Memory Usage: {psutil.virtual_memory().percent:.1f}%")
    print(f"   Available Memory: {psutil.virtual_memory().available / (1024**3):.1f} GB")
    
    # Estimate memory requirements for loading
    estimated_memory = file_size * 3  # Rough estimate
    print(f"   Estimated Load Memory: {estimated_memory:.1f} MB")

# Example usage
analyze_memory_usage("large_grid.3mf")
```

## Validation

### File Integrity

```python
def validate_3mf_file(file_path):
    """Comprehensive 3MF file validation"""
    
    try:
        analysis = analyze_3mf(file_path)
        
        # Basic validation
        checks = {
            "File exists": os.path.exists(file_path),
            "Has objects": analysis['summary']['object_count'] > 0,
            "Has triangles": analysis['summary']['total_triangles'] > 0,
            "Valid dimensions": all(d > 0 for d in analysis['summary']['overall_dimensions']),
            "No zero volumes": all(model['volume'] > 0 for model in analysis['models'])
        }
        
        print("🔍 File Validation:")
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check}")
        
        # Overall result
        all_passed = all(checks.values())
        print(f"\n{'✅ File is valid' if all_passed else '❌ File has issues'}")
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False

# Example usage
validate_3mf_file("grid_2x2.3mf")
```

### Grid Validation

```python
def validate_grid(file_path, expected_count=None, expected_spacing=None):
    """Validate grid layout parameters"""
    
    analysis = analyze_3mf(file_path)
    models = analysis['models']
    
    print("🔢 Grid Validation:")
    
    # Count validation
    if expected_count:
        count_valid = len(models) == expected_count
        status = "✅" if count_valid else "❌"
        print(f"   {status} Object count: {len(models)} (expected: {expected_count})")
    
    # Spacing validation
    if expected_spacing and len(models) >= 2:
        positions = [model['center_of_mass'] for model in models]
        actual_spacing = abs(positions[1][0] - positions[0][0])
        tolerance = expected_spacing * 0.05  # 5% tolerance
        spacing_valid = abs(actual_spacing - expected_spacing) < tolerance
        
        status = "✅" if spacing_valid else "❌"
        print(f"   {status} Spacing: {actual_spacing:.1f}mm (expected: {expected_spacing:.1f}mm)")
    
    # Alignment validation
    if len(models) >= 4:  # At least 2x2 grid
        x_coords = [model['center_of_mass'][0] for model in models]
        y_coords = [model['center_of_mass'][1] for model in models]
        
        x_unique = len(set(round(x, 1) for x in x_coords))
        y_unique = len(set(round(y, 1) for y in y_coords))
        
        print(f"   📐 Grid structure: {y_unique}×{x_unique}")

# Example usage
validate_grid("grid_2x2.3mf", expected_count=4, expected_spacing=55.0)
```

## Comparison Tools

### Compare Multiple Files

```python
def compare_3mf_files(file_paths):
    """Compare multiple 3MF files"""
    
    print("📊 File Comparison:")
    print(f"{'File':<20} {'Objects':<8} {'Triangles':<12} {'Size (MB)':<10}")
    print("-" * 55)
    
    for file_path in file_paths:
        analysis = analyze_3mf(file_path)
        filename = os.path.basename(file_path)
        
        print(f"{filename:<20} "
              f"{analysis['summary']['object_count']:<8} "
              f"{analysis['summary']['total_triangles']:<12,} "
              f"{analysis['summary']['file_size_mb']:<10.1f}")

# Example usage
compare_3mf_files([
    "grid_2x2.3mf",
    "grid_3x3.3mf", 
    "production_batch.3mf"
])
```

## Export Analysis

### Generate Reports

```python
import json
from datetime import datetime

def generate_analysis_report(file_path, output_path=None):
    """Generate detailed analysis report"""
    
    analysis = analyze_3mf(file_path)
    
    # Create comprehensive report
    report = {
        "analysis_timestamp": datetime.now().isoformat(),
        "file_path": file_path,
        "summary": analysis['summary'],
        "models": analysis['models'],
        "metadata": analysis.get('metadata', {}),
        "validation": validate_3mf_file(file_path)
    }
    
    # Save report
    if not output_path:
        output_path = file_path.replace('.3mf', '.analysis.json')
    
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"📄 Analysis report saved: {output_path}")
    return report

# Example usage
generate_analysis_report("grid_2x2.3mf")
```

## Next Steps

- **[Grid Layouts](grid-layouts.md)** - Create optimized grids
- **[Batch Processing](batch-processing.md)** - Process multiple files
- **[API Reference](../reference/analyzer.md)** - Detailed analysis API
