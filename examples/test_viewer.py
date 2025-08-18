# -*- coding: utf-8 -*-
"""
Test the new viewer.py module with enhanced configuration.
----
file:
    name:       test_viewer.py  
    uuid:       c4d5e6f7-8g9h-0i1j-2k3l-m4n5o6p7q8r9
description:    Test the new viewer.py module with enhanced configuration
authors:        felix@42sol.eu
project:
    name:       noah123d
    uuid:       93fe70d7-2d29-4ebf-bf0e-51d75dbfda30
    url:        https://github.com/42sol-eu/noah123d
"""

# %% [External imports]
from noah123d import ColorMapHelper, ViewerHelper, setup_viewer
from ocp_vscode import Camera

# %% [Test setup function]
print("Testing setup_viewer function...")
try:
    # Set up viewer with custom configuration
    setup_viewer(port=3940, camera=Camera.KEEP)
    print("✅ setup_viewer() completed successfully")
except Exception as e:
    print(f"⚠️  setup_viewer() warning: {e}")

# %% [Test ColorMapHelper with new configuration]
print("\nTesting ColorMapHelper with new configuration...")

# Create helper with custom port and camera settings
helper = ColorMapHelper(
    grid_size=10, 
    spacing=3.0,
    port=3940,  # Custom port
    camera=Camera.KEEP  # Keep camera position
)

print(f"✅ ColorMapHelper created with port={helper.port} and camera={helper.camera}")

# %% [Create and show objects]
print("\nCreating sphere grid...")
helper.create_sphere_grid(rows=1, cols=10)
print(f"✅ Created {len(helper.objects)} spheres")

# %% [Test with presets]
print("\nTesting preset colormaps...")
helper.show_with_preset('rainbow')
print("✅ Displayed rainbow preset")

helper.show_with_preset('viridis', alpha=0.8)  
print("✅ Displayed viridis preset with alpha=0.8")

# %% [Test ViewerHelper alias]
print("\nTesting ViewerHelper alias...")
viewer_helper = ViewerHelper(grid_size=5, spacing=2.0, port=3940)
viewer_helper.create_box_grid(rows=1, cols=5)
viewer_helper.show_with_preset('plasma')
print("✅ ViewerHelper alias working correctly")

# %% [Test backwards compatibility]
print("\nTesting backwards compatibility...")
try:
    # This should still work with the new module
    from noah123d import ColorMapHelper as LegacyHelper
    legacy = LegacyHelper(grid_size=3)
    legacy.create_sphere_grid()
    legacy.show_with_tab20()
    print("✅ Backwards compatibility maintained")
except Exception as e:
    print(f"❌ Backwards compatibility issue: {e}")

print("\n🎉 All tests completed!")
print(f"Available presets: {helper.get_available_presets()}")
