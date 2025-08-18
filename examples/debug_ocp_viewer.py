# -*- coding: utf-8 -*-
"""
Debug OCP viewer connectivity and display.
----
file:
    name:       debug_ocp_viewer.py  
    uuid:       e5f6g7h8-9i0j-1k2l-3m4n-o5p6q7r8s9t0
description:    Debug OCP viewer connectivity and display
authors:        felix@42sol.eu
project:
    name:       noah123d
    uuid:       93fe70d7-2d29-4ebf-bf0e-51d75dbfda30
    url:        https://github.com/42sol-eu/noah123d
"""

# %% [External imports]
from build123d import Box, Sphere
from ocp_vscode import show, set_port, show_object, reset_show
import time

print("=== OCP Viewer Debug Script ===")
print()

# %% Test 1: Simple object display
print("Test 1: Creating and showing a simple box...")
try:
    # Reset first
    reset_show()
    
    # Create a simple box
    box = Box(10, 10, 10)
    print(f"Box created: {type(box)}")
    
    # Show it
    show(box)
    print("✅ Box sent to viewer")
    
    # Wait a moment
    time.sleep(2)
    
except Exception as e:
    print(f"❌ Error in Test 1: {e}")

print()

# %% Test 2: Multiple objects
print("Test 2: Creating and showing multiple objects...")
try:
    # Reset first
    reset_show()
    
    # Create multiple objects
    sphere = Sphere(5)
    box = Box(5, 5, 5).translate((15, 0, 0))
    
    print(f"Created sphere: {type(sphere)}")
    print(f"Created box: {type(box)}")
    
    # Show them
    show(sphere, box)
    print("✅ Multiple objects sent to viewer")
    
    time.sleep(2)
    
except Exception as e:
    print(f"❌ Error in Test 2: {e}")

print()

# %% Test 3: Individual object showing
print("Test 3: Using show_object for individual display...")
try:
    # Reset first
    reset_show()
    
    # Create and show individual objects
    obj1 = Sphere(3).translate((-10, 0, 0))
    obj2 = Box(3, 3, 3).translate((0, 0, 0))
    obj3 = Sphere(2).translate((10, 0, 0))
    
    show_object(obj1, options={"color": "red", "alpha": 0.8})
    show_object(obj2, options={"color": "green", "alpha": 0.8})
    show_object(obj3, options={"color": "blue", "alpha": 0.8})
    
    print("✅ Individual objects sent to viewer")
    
    time.sleep(2)
    
except Exception as e:
    print(f"❌ Error in Test 3: {e}")

print()

# %% Test 4: Check port and connectivity
print("Test 4: Port and connectivity information...")
try:
    import websockets
    import asyncio
    
    async def check_port():
        try:
            # Try to connect to the viewer
            uri = "ws://127.0.0.1:3939"
            async with websockets.connect(uri, timeout=5) as websocket:
                print(f"✅ Successfully connected to OCP viewer at {uri}")
                return True
        except Exception as e:
            print(f"❌ Could not connect to OCP viewer: {e}")
            return False
    
    # Run the async check
    connected = asyncio.run(check_port())
    
except ImportError:
    print("⚠️  websockets not available for direct testing")
except Exception as e:
    print(f"❌ Error checking connectivity: {e}")

print()

# %% Test 5: ColorMapHelper basic test
print("Test 5: Testing ColorMapHelper...")
try:
    from noah123d import ColorMapHelper
    
    # Reset first
    reset_show()
    
    helper = ColorMapHelper(grid_size=5, spacing=3.0)
    helper.create_sphere_grid(rows=1, cols=5)
    
    print(f"Created {len(helper.objects)} objects")
    
    # Try simple display first
    show(*helper.objects)
    print("✅ ColorMapHelper objects sent to viewer")
    
    time.sleep(2)
    
except Exception as e:
    print(f"❌ Error in Test 5: {e}")

print()
print("=== Debug Summary ===")
print("1. Check if OCP viewer extension is installed and active in VS Code")
print("2. Make sure you have the OCP viewer panel open in VS Code")
print("3. Try refreshing the OCP viewer panel")
print("4. Check if other examples work (like the original example_ocp_colormap.py)")
print("5. If objects are being sent but not displayed, try:")
print("   - Zooming out in the viewer (mouse wheel)")
print("   - Resetting the camera view (look for reset/home button)")
print("   - Checking if objects are very small or very large")
print()
print("The debug output shows data IS being sent to the viewer (large binary payloads).")
print("If you still can't see anything, the issue is likely with the viewer display,")
print("not with the data being sent.")
