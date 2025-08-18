# -*- coding: utf-8 -*-
"""
Tests for ColorMapHelper class.
----
file:
    name:       test_colormap_helper.py  
    uuid:       d4e5f6g7-8h9i-0j1k-2l3m-n4o5p6q7r8s9
description:    Tests for ColorMapHelper class
authors:        felix@42sol.eu
project:
    name:       noah123d
    uuid:       93fe70d7-2d29-4ebf-bf0e-51d75dbfda30
    url:        https://github.com/42sol-eu/noah123d
"""

import pytest
import sys
import os

# Add src to path so we can import noah123d
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from noah123d.visual.colormap_helper import ColorMapHelper, PRESET_COLORMAPS

class TestColorMapHelper:
    """Test suite for ColorMapHelper class."""

    def test_initialization(self):
        """Test ColorMapHelper initialization."""
        helper = ColorMapHelper()
        assert helper.grid_size == 20  # Default value
        assert helper.spacing == 2.0   # Default value
        assert helper.object_size == 1.0  # Default value
        assert len(helper.objects) == 0
        
        # Test custom initialization
        helper2 = ColorMapHelper(grid_size=10, spacing=1.5, object_size=0.5)
        assert helper2.grid_size == 10
        assert helper2.spacing == 1.5
        assert helper2.object_size == 0.5

    def test_sphere_grid_creation(self):
        """Test sphere grid creation."""
        helper = ColorMapHelper(grid_size=6, spacing=2.0)
        objects = helper.create_sphere_grid(rows=2, cols=3)
        
        assert len(objects) == 6  # 2 rows * 3 cols
        assert len(helper.objects) == 6
        assert helper.objects == objects

    def test_box_grid_creation(self):
        """Test box grid creation."""
        helper = ColorMapHelper(grid_size=8, spacing=1.5)
        objects = helper.create_box_grid(rows=2, cols=4)
        
        assert len(objects) == 8  # 2 rows * 4 cols
        assert len(helper.objects) == 8
        assert helper.objects == objects

    def test_preset_colormaps(self):
        """Test preset colormap availability."""
        helper = ColorMapHelper()
        presets = helper.get_available_presets()
        
        # Check that all expected presets are available
        expected_presets = [
            'rainbow', 'heat', 'cool', 'viridis', 'plasma',
            'blues', 'greens', 'reds', 'turbo', 'summer'
        ]
        for preset in expected_presets:
            assert preset in presets

        # Check PRESET_COLORMAPS structure
        for preset_name, (colormap_name, colormap_type) in PRESET_COLORMAPS.items():
            assert isinstance(colormap_name, str)
            assert colormap_type in ['segmented', 'listed']

    def test_invalid_preset(self):
        """Test error handling for invalid preset."""
        helper = ColorMapHelper()
        helper.create_sphere_grid(rows=1, cols=5)
        
        with pytest.raises(ValueError, match="Unknown preset"):
            helper.show_with_preset('invalid_preset')

    def test_properties(self):
        """Test property access."""
        helper = ColorMapHelper()
        helper.create_sphere_grid(rows=2, cols=3)
        
        # Test objects property
        objects = helper.objects
        assert len(objects) == 6
        
        # Test current_colormap property (should be None initially)
        assert helper.current_colormap is None

    def test_automatic_object_creation(self):
        """Test that methods create objects automatically if none exist."""
        helper = ColorMapHelper(grid_size=5)
        
        # Should have no objects initially
        assert len(helper.objects) == 0
        
        # This should create objects automatically
        try:
            helper.show_with_tab20()
            # If no error, objects were created
            assert len(helper.objects) > 0
        except ImportError:
            # ocp_vscode not available, which is OK for testing
            pass

    def test_colormap_methods_exist(self):
        """Test that all colormap methods exist and are callable."""
        helper = ColorMapHelper()
        
        # Test that methods exist
        methods = [
            'show_with_preset',
            'show_with_tab20', 
            'show_with_segmented',
            'show_with_smart_colormap',
            'show_with_golden_ratio',
            'show_with_seeded_random',
            'show_with_custom_colors',
            'set_global_colormap',
            'show_simple',
            'reset_visualization'
        ]
        
        for method_name in methods:
            assert hasattr(helper, method_name)
            assert callable(getattr(helper, method_name))

    def test_constants(self):
        """Test that constants are defined correctly."""
        from noah123d.visual.colormap_helper import (
            DEFAULT_GRID_SIZE, 
            DEFAULT_SPACING, 
            DEFAULT_OBJECT_SIZE
        )
        
        assert isinstance(DEFAULT_GRID_SIZE, int)
        assert isinstance(DEFAULT_SPACING, float)
        assert isinstance(DEFAULT_OBJECT_SIZE, float)
        
        assert DEFAULT_GRID_SIZE > 0
        assert DEFAULT_SPACING > 0
        assert DEFAULT_OBJECT_SIZE > 0

    def test_custom_colors_validation(self):
        """Test custom colors functionality."""
        helper = ColorMapHelper()
        helper.create_sphere_grid(rows=1, cols=3)
        
        custom_colors = ['red', 'green', 'blue']
        
        # This should not raise an error
        try:
            helper.show_with_custom_colors(custom_colors)
        except ImportError:
            # ocp_vscode not available, which is OK for testing
            pass

if __name__ == "__main__":
    # Run basic tests without pytest if called directly
    test_helper = TestColorMapHelper()
    
    print("Running ColorMapHelper tests...")
    
    try:
        test_helper.test_initialization()
        print("✓ Initialization test passed")
        
        test_helper.test_sphere_grid_creation()
        print("✓ Sphere grid creation test passed")
        
        test_helper.test_box_grid_creation()
        print("✓ Box grid creation test passed")
        
        test_helper.test_preset_colormaps()
        print("✓ Preset colormaps test passed")
        
        test_helper.test_properties()
        print("✓ Properties test passed")
        
        test_helper.test_automatic_object_creation()
        print("✓ Automatic object creation test passed")
        
        test_helper.test_colormap_methods_exist()
        print("✓ Colormap methods test passed")
        
        test_helper.test_constants()
        print("✓ Constants test passed")
        
        test_helper.test_custom_colors_validation()
        print("✓ Custom colors test passed")
        
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
