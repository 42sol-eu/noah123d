# ColorMapHelper Usage Guide

The `ColorMapHelper` class in noah123d makes it easy to create and visualize objects with beautiful colormaps using build123d and ocp_vscode.

## Quick Start

```python
from noah123d import ColorMapHelper

# Create a helper instance
helper = ColorMapHelper(grid_size=20, spacing=2.0)

# Create a grid of spheres
helper.create_sphere_grid(rows=4, cols=5)

# Show with different colormap styles
helper.show_with_preset('heat')                    # Use preset colormap
helper.show_with_tab20()                          # Use tab20 colormap
helper.show_with_golden_ratio('hsv')              # Golden ratio distribution
helper.show_with_seeded_random(42, 'mpl:plasma')  # Reproducible random colors
```

## Available Preset Colormaps

The helper includes these preset colormaps:

- `rainbow` - Classic rainbow colors (HSV)
- `heat` - Heat map colors (red to yellow)
- `cool` - Cool colors (cyan to magenta)  
- `viridis` - Perceptually uniform colormap
- `plasma` - High-contrast plasma colormap
- `blues` - Blue color gradients
- `greens` - Green color gradients
- `reds` - Red color gradients
- `turbo` - Google's Turbo colormap
- `summer` - Summer color scheme

## Main Methods

### Object Creation

```python
helper = ColorMapHelper(grid_size=20, spacing=2.0, object_size=1.0)

# Create different object types
helper.create_sphere_grid(rows=4, cols=5)  # Grid of spheres
helper.create_box_grid(rows=2, cols=10)    # Grid of boxes
```

### Colormap Methods

#### Preset Colormaps
```python
# Use named presets with automatic colormap type detection
helper.show_with_preset('viridis', alpha=0.8, reverse=False, segments=10)
```

#### Tab20 Colormap
```python
# Discrete 20-color palette, great for categorical data
helper.show_with_tab20(alpha=0.8, reverse=False)
```

#### Smart Colormap (Recommended)
```python
# Automatically chooses between segmented and listed colormaps
helper.show_with_smart_colormap(10, 'mpl:viridis', alpha=0.9)
```

#### Golden Ratio Distribution
```python
# Uses golden ratio for aesthetically pleasing color distribution
helper.show_with_golden_ratio('hsv', alpha=0.8, reverse=False)
```

#### Seeded Random Colors
```python
# Reproducible random colors with seed
helper.show_with_seeded_random(
    seed=42, 
    colormap_name='mpl:turbo', 
    alpha=0.8,
    lower=10,    # Lower bound for color range
    upper=100,   # Upper bound for color range  
    brightness=1.2
)
```

#### Custom Colors
```python
# Use your own list of colors
custom_colors = ['red', 'green', 'blue', 'yellow', 'purple']
helper.show_with_custom_colors(custom_colors)
```

### Global Colormap Settings

```python
# Set a global colormap that affects all subsequent show operations
helper.set_global_colormap(
    colormap_type='golden_ratio',  # 'golden_ratio', 'segmented', 'tab20', 'seeded'
    colormap_name='mpl:Blues',
    alpha=0.8,
    reverse=False
)

# Now all objects use the global colormap
helper.show_simple()
```

### Utility Methods

```python
# Get available presets
presets = helper.get_available_presets()
print("Available presets:", presets)

# Reset visualization
helper.reset_visualization()

# Access objects directly if needed
objects = helper.objects
current_colormap = helper.current_colormap

# Demo all presets (interactive)
helper.demo_all_presets()  # Press Enter between each demo
```

## Comparison with Original ColorMap Usage

### Before (Original ocp_vscode)
```python
import copy
from build123d import *
from ocp_vscode import *

def reference(obj, loc):
    return copy.copy(obj).move(loc)

sphere = Sphere(1)
spheres = [reference(sphere, loc) for loc in GridLocations(1, 2, 1, 20)]

# Multiple lines of setup for each visualization
show(*spheres, colors=ColorMap.tab20(alpha=0.8))
show(*spheres, colors=ColorMap.segmented(20, "mpl:Greens", alpha=0.8)) 
show(*spheres, colors=ColorMap.golden_ratio("hsv", alpha=0.8))
```

### After (With ColorMapHelper)
```python
from noah123d import ColorMapHelper

# One line of setup
helper = ColorMapHelper(grid_size=20, spacing=2.0)
helper.create_sphere_grid(rows=1, cols=20)

# Simple method calls
helper.show_with_tab20(alpha=0.8)
helper.show_with_preset('greens', alpha=0.8, segments=20)  
helper.show_with_golden_ratio('hsv', alpha=0.8)
```

## Advanced Usage

### Data Visualization Example
```python
import random
from noah123d import ColorMapHelper

# Simulate data with different "temperatures"
random.seed(42)
data_values = [random.uniform(0, 100) for _ in range(25)]

helper = ColorMapHelper(grid_size=25, spacing=1.5)
helper.create_sphere_grid(rows=5, cols=5)

# Use heat colormap to represent data intensity
helper.show_with_preset('heat', alpha=0.9)
print(f"Data range: {min(data_values):.1f} to {max(data_values):.1f}")
```

### Multiple Object Types
```python
helper1 = ColorMapHelper(grid_size=10, spacing=3.0)
helper2 = ColorMapHelper(grid_size=15, spacing=2.0)

# Create different layouts
helper1.create_sphere_grid(rows=2, cols=5)  # Spheres
helper2.create_box_grid(rows=3, cols=5)     # Boxes

# Apply different colormaps
helper1.show_with_preset('plasma')
helper2.show_with_preset('viridis')
```

## Error Handling

The helper automatically handles colormap compatibility issues:

- Tries `segmented` first, falls back to `listed` if needed
- Provides clear error messages for unknown presets
- Gracefully handles missing ocp_vscode dependency

## Requirements

- `build123d` - For 3D object creation
- `ocp_vscode` - For visualization and colormaps
- `noah123d` - This package

The helper will raise an `ImportError` if `ocp_vscode` is not available.

## Tips

1. **Use presets** for quick results: `helper.show_with_preset('viridis')`
2. **Use smart colormap** when unsure about colormap types: `helper.show_with_smart_colormap()`  
3. **Set global colormaps** for consistent styling across multiple visualizations
4. **Use seeded random** for reproducible but varied color schemes
5. **Adjust alpha** for transparency effects: `alpha=0.7`
6. **Use reverse=True** to flip colormaps: `reverse=True`
