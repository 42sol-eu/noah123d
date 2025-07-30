#!/usr/bin/env python3
"""Test the fixed grid placement."""

from noah123d import analyze_3mf

def test_fixed_grid():
    """Test the fixed grid placement."""
    print("=== FIXED GRID ANALYSIS ===")
    
    result = analyze_3mf('test_fixed_grid_2x2.3mf')
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        return
        
    print(f"Objects: {result['summary']['object_count']}")
    print(f"Overall dimensions: {result['summary']['overall_dimensions']}")
    print("Individual object positions:")
    
    centers = []
    for i, model in enumerate(result['models']):
        center = model['center_of_mass']
        centers.append(center)
        print(f"  Object {model['object_id']} (#{i+1}): Center = ({center[0]:.1f}, {center[1]:.1f}, {center[2]:.1f})")
    
    if len(centers) >= 2:
        x_spacing = abs(centers[1][0] - centers[0][0])
        print(f"X spacing between objects 1 and 2: {x_spacing:.1f}")
        
    if len(centers) >= 3:
        y_spacing = abs(centers[2][1] - centers[0][1])
        print(f"Y spacing between objects 1 and 3: {y_spacing:.1f}")
        
    # Check if grid is properly centered and spaced
    expected_spacing = 50.0 * 1.1  # 55.0
    print(f"Expected spacing: {expected_spacing:.1f}")
    
    # Check grid regularity
    if len(centers) == 4:
        print("\nGrid regularity check:")
        print(f"  Top-left: ({centers[0][0]:.1f}, {centers[0][1]:.1f})")
        print(f"  Top-right: ({centers[1][0]:.1f}, {centers[1][1]:.1f})")
        print(f"  Bottom-left: ({centers[2][0]:.1f}, {centers[2][1]:.1f})")
        print(f"  Bottom-right: ({centers[3][0]:.1f}, {centers[3][1]:.1f})")

if __name__ == "__main__":
    test_fixed_grid()
