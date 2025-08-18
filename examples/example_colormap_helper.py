# -*- coding: utf-8 -*-
"""
Example usage of the ColorMapHelper class from noah123d.
----
file:
    name:       example_colormap_helper.py  
    uuid:       b2c3d4e5-6f7g-8h9i-0j1k-l2m3n4o5p6q7
description:    Example usage of the ColorMapHelper class from noah123d
authors:        felix@42sol.eu
project:
    name:       noah123d
    uuid:       93fe70d7-2d29-4ebf-bf0e-51d75dbfda30
    url:        https://github.com/42sol-eu/noah123d
"""

# %% [External imports]
from noah123d import (
    ColorMapHelper,
    PRESET_COLORMAPS
)

# %% [Main]
if __name__ == "__main__":
    print("Noah123D ColorMap Helper Demo")
    print("=" * 40)
    
    # Create a helper instance
    helper = ColorMapHelper(grid_size=20, spacing=2.0)
    
    print("Available colormap presets:")
    for preset in helper.get_available_presets():
        print(f"  - {preset}")
    print()
    
    # Create a grid of spheres
    print("Creating sphere grid...")
    helper.create_sphere_grid(rows=4, cols=5)
    
    # %% Demo 1: Show with preset colormap
    print("Demo 1: Showing with 'heat' preset")
    helper.show_with_preset('heat', alpha=0.8)
    
    # %% Demo 2: Show with tab20
    print("Demo 2: Showing with tab20 colormap")
    helper.show_with_tab20(alpha=0.8, reverse=False)
    
    # %% Demo 3: Show with segmented colormap
    print("Demo 3: Showing with smart colormap (auto-detects segmented vs listed)")
    helper.show_with_smart_colormap(10, 'mpl:viridis', alpha=0.9)
    
    # %% Demo 4: Show with golden ratio distribution
    print("Demo 4: Showing with golden ratio distribution")
    helper.show_with_golden_ratio('hsv', alpha=0.8)
    
    # %% Demo 5: Show with seeded random colors
    print("Demo 5: Showing with seeded random colors")
    helper.show_with_seeded_random(42, 'mpl:turbo', alpha=0.8)
    
    # %% Demo 6: Show with custom colors
    print("Demo 6: Showing with custom colors")
    custom_colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
    helper.show_with_custom_colors(custom_colors)
    
    # %% Demo 7: Set global colormap and show multiple grids
    print("Demo 7: Setting global colormap")
    helper.set_global_colormap('golden_ratio', 'mpl:Blues', alpha=0.8)
    
    # Create different object types
    helper.create_box_grid(rows=2, cols=10)
    helper.show_simple()
    
    # %% Demo 8: Reset and create a different configuration
    print("Demo 8: Creating different grid configuration")
    helper.reset_visualization()
    
    # Create a larger helper for more objects
    large_helper = ColorMapHelper(grid_size=25, spacing=1.5, object_size=0.8)
    large_helper.create_sphere_grid(rows=5, cols=5)
    large_helper.show_with_preset('rainbow', alpha=0.7, reverse=True)
    
    print("Demo completed! Check the 3D viewer for results.")

# %% Additional examples for specific use cases

def demo_comparison():
    """Demonstrate side-by-side comparison of different colormaps."""
    print("\nComparison Demo: Different colormaps on same objects")
    
    helper1 = ColorMapHelper(grid_size=10, spacing=3.0)
    helper1.create_sphere_grid(rows=2, cols=5)
    
    # Move objects to different positions for comparison
    import copy
    from build123d import Pos
    
    objects_set1 = helper1.objects
    objects_set2 = [copy.copy(obj).move(Pos(0, 10, 0)) for obj in objects_set1]
    objects_set3 = [copy.copy(obj).move(Pos(0, 20, 0)) for obj in objects_set1]
    
    # Show different colormaps
    from ocp_vscode import show, ColorMap
    
    show(*objects_set1, colors=ColorMap.golden_ratio('mpl:viridis', alpha=0.8))
    show(*objects_set2, colors=ColorMap.segmented(10, 'mpl:plasma', alpha=0.8))
    show(*objects_set3, colors=ColorMap.tab20(alpha=0.8))
    
    print("Comparison complete - check viewer for three different colormap styles")

def demo_data_visualization():
    """Demonstrate using colormaps for data visualization."""
    print("\nData Visualization Demo")
    
    # Simulate some data values
    import random
    random.seed(42)
    data_values = [random.uniform(0, 100) for _ in range(20)]
    
    helper = ColorMapHelper(grid_size=20, spacing=2.0)
    helper.create_sphere_grid(rows=4, cols=5)
    
    # Use colors to represent data values
    # For real data visualization, you would map your data to color indices
    print(f"Data values range: {min(data_values):.1f} to {max(data_values):.1f}")
    
    # Use a heat colormap to show the "temperature" of data
    helper.show_with_preset('heat', alpha=0.9)
    print("Using heat colormap to visualize data intensity")

if __name__ == "__main__":
    # Run additional demos if ocp_vscode is available
    try:
        demo_comparison()
        demo_data_visualization()
    except ImportError:
        print("ocp_vscode not available - skipping advanced demos")
