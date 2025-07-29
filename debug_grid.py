#!/usr/bin/env python3
"""Debug script to analyze grid placement issues."""

from noah123d import analyze_3mf, get_stl_info
from pathlib import Path

def analyze_grid_placement():
    """Analyze grid placement issues."""
    print("=== Grid Placement Analysis ===\n")
    
    # First, let's look at the original STL info
    stl_file = Path("_models/multiverse/tile_2x2_borde.stl")
    if stl_file.exists():
        stl_info = get_stl_info(stl_file)
        print("Original STL Info:")
        print(f"  Bounding box: min={stl_info['bounding_box']['min']}, max={stl_info['bounding_box']['max']}")
        print(f"  Dimensions: {stl_info['dimensions']}")
        print(f"  Center of gravity: {stl_info['center_of_gravity']}")
        print()
    
    # Analyze different grid files
    grid_files = ["grid_2x2.3mf", "grid_1x5.3mf", "advanced_tight_2x2.3mf"]
    
    for grid_file in grid_files:
        file_path = Path(grid_file)
        if not file_path.exists():
            print(f"File {grid_file} not found, skipping...")
            continue
            
        print(f"=== Analysis of {grid_file} ===")
        analysis = analyze_3mf(file_path)
        
        if 'error' in analysis:
            print(f"Error: {analysis['error']}")
            continue
            
        print(f"Objects: {analysis['summary']['object_count']}")
        print(f"Overall dimensions: {analysis['summary']['overall_dimensions']}")
        print(f"Overall center: {analysis['summary']['overall_center_of_mass']}")
        print()
        
        # Show individual object positions
        print("Individual object positions:")
        for i, model in enumerate(analysis['models']):
            center = model['center_of_mass']
            print(f"  Object {model['object_id']} (#{i+1}): Center = ({center[0]:.1f}, {center[1]:.1f}, {center[2]:.1f})")
        
        # Calculate expected vs actual spacing
        if len(analysis['models']) >= 2:
            first_center = analysis['models'][0]['center_of_mass']
            second_center = analysis['models'][1]['center_of_mass']
            spacing_x = abs(second_center[0] - first_center[0])
            spacing_y = abs(second_center[1] - first_center[1])
            print(f"  Spacing between first two objects: X={spacing_x:.1f}, Y={spacing_y:.1f}")
        
        print("-" * 50)

if __name__ == "__main__":
    analyze_grid_placement()
