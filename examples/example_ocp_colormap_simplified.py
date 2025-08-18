# -*- coding: utf-8 -*-
"""
Simplified colormap example using noah123d ColorMapHelper.
----
file:
    name:       example_ocp_colormap_simplified.py  
    uuid:       c3d4e5f6-7g8h-9i0j-1k2l-m3n4o5p6q7r8
description:    Simplified colormap example using noah123d ColorMapHelper
authors:        felix@42sol.eu
project:
    name:       noah123d
    uuid:       93fe70d7-2d29-4ebf-bf0e-51d75dbfda30
    url:        https://github.com/42sol-eu/noah123d
"""

# %% [External imports]
from noah123d import ColorMapHelper
from ocp_vscode import set_port

# %% [Setup]
# Fix OCP viewer port detection issue
set_port(3940)

# %% [Main]

# Create the helper - much simpler than the original example
helper = ColorMapHelper(grid_size=20, spacing=2.0)

# Create objects in one line instead of manual grid creation and copying
helper.create_sphere_grid(rows=1, cols=20)

# %% All the functionality from the original example, but much simpler:

# Original: show(*spheres, colors=ColorMap.tab20(alpha=0.8))
helper.show_with_tab20(alpha=0.8)

# %% Original: show(*spheres, colors=ColorMap.tab20(reverse=True))
helper.show_with_tab20(reverse=True)

# %% Original: show(*spheres, colors=ColorMap.segmented(20, "mpl:Greens", alpha=0.8))
helper.show_with_segmented(20, "mpl:Greens", alpha=0.8)

# %% Original: show(*spheres, colors=ColorMap.segmented(10, "mpl:Greens", alpha=0.8))
helper.show_with_segmented(10, "mpl:Greens", alpha=0.8)

# %% Original: show(*spheres, colors=ColorMap.golden_ratio("mpl:Greens", alpha=0.8))
helper.show_with_golden_ratio("mpl:Greens", alpha=0.8)

# %% Original: show(*spheres, colors=ColorMap.golden_ratio("mpl:Greens", reverse=True))
helper.show_with_golden_ratio("mpl:Greens", reverse=True)

# %% Original: show(*spheres, colors=ColorMap.segmented(10, "mpl:summer", reverse=True))
helper.show_with_segmented(10, "mpl:summer", reverse=True)

# %% Original: show(*spheres, colors=ColorMap.seeded(42, "mpl:summer"))
helper.show_with_seeded_random(42, "mpl:summer")

# %% Original: show(*spheres, colors=ColorMap.seeded(4242, "mpl:summer"))
helper.show_with_seeded_random(4242, "mpl:summer")

# %% Original: show(*spheres, colors=ColorMap.segmented(20, "hsv", reverse=False))
helper.show_with_segmented(20, "hsv", reverse=False)

# %% Original: show(*spheres, colors=ColorMap.segmented(10, "hsv", reverse=False))
helper.show_with_segmented(10, "hsv", reverse=False)

# %% Original: show(*spheres, colors=ColorMap.golden_ratio("hsv", alpha=0.8))
helper.show_with_golden_ratio("hsv", alpha=0.8)

# %% Original: show(*spheres, colors=ColorMap.seeded(42, "hsv"))
helper.show_with_seeded_random(42, "hsv")

# %% Original: show(*spheres, colors=ColorMap.seeded(59798267586177, "rgb", lower=10, upper=100, brightness=2.2))
helper.show_with_seeded_random(59798267586177, "rgb", lower=10, upper=100, brightness=2.2)

# %% Global colormap examples - Original: set_colormap(ColorMap.golden_ratio("mpl:Blues", alpha=0.8))
helper.set_global_colormap('golden_ratio', "mpl:Blues", alpha=0.8)
helper.show_simple()  # Original: show(*spheres)

# %% Show subset - Original: show(*spheres[:10])
# With helper, you can create a new smaller grid or work with the objects directly
subset_helper = ColorMapHelper(grid_size=10, spacing=2.0)
subset_helper.create_sphere_grid(rows=1, cols=10)
subset_helper.show_simple()

# %% Original: set_colormap(ColorMap.tab20(alpha=0.8))
helper.set_global_colormap('tab20', alpha=0.8)
helper.show_simple()

# %% Original: set_colormap(ColorMap.seeded(42, "hsv", alpha=0.8))
helper.set_global_colormap('seeded', "hsv", alpha=0.8, seed=42)
helper.show_simple()

# %% Reset - Original: reset_show()
helper.reset_visualization()

# Individual object showing would still need to be done manually 
# as it's a specific use case, but the helper provides access to objects
from ocp_vscode import show_object
objects = helper.objects
if objects:
    show_object(objects[0])
    show_object(objects[1])
    show_object(objects[2])
    show_object(objects[3], options={"color": "black", "alpha": 1.0})

# %% Custom colors - Original: ColorMap.listed(["red", "green", "blue"])
helper.show_with_custom_colors(["red", "green", "blue"])

# %% Boxes example - much simpler than original
box_helper = ColorMapHelper(grid_size=20, spacing=2.0)
box_helper.create_box_grid(rows=1, cols=20)

# %% Even simpler with presets instead of remembering colormap names
helper.show_with_preset('heat')  # Instead of "mpl:hot"
helper.show_with_preset('rainbow')  # Instead of "hsv"

# %% Show all available presets
print("Available presets:", helper.get_available_presets())
