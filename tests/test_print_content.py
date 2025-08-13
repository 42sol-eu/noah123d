#!/usr/bin/env python3
"""
Quick test to demonstrate the context-aware print_content method.
"""

import sys
sys.path.insert(0, 'src')

from noah123d.visual.console import Console

def test_print_content():
    console = Console()
    
    # Test 1: Archive contents (list of file paths)
    print("\n=== Test 1: Archive Contents ===")
    archive_files = [
        "3D/3dmodel.model",
        "[Content_Types].xml", 
        "_rels/.rels",
        "Metadata/conversion_info.txt"
    ]
    console.print_content(archive_files, 'archive')
    
    # Test 2: Metadata files (filtered list)  
    print("\n=== Test 2: Metadata Files ===")
    metadata_files = [f for f in archive_files if 'Metadata' in f]
    console.print_content(metadata_files, 'metadata')
    
    # Test 3: Object details (list of dicts)
    print("\n=== Test 3: Object Details ===")
    object_details = [
        {'id': 1, 'vertices': 1000, 'triangles': 2000, 'type': 'mesh'},
        {'id': 2, 'vertices': 1500, 'triangles': 3000, 'type': 'mesh'},
    ]
    console.print_content(object_details, 'objects')
    
    # Test 4: Auto-detection without context hint
    print("\n=== Test 4: Auto-detection (no context hint) ===")
    console.print_content(archive_files)  # Should detect as file paths
    
    # Test 5: Dictionary content
    print("\n=== Test 5: Dictionary Content ===")
    config_data = {
        'version': '1.0',
        'objects': 5,
        'metadata': ['conversion_info.txt'],
        'settings': {'quality': 'high', 'compression': True}
    }
    console.print_content(config_data, 'configuration')
    
    # Test 6: Empty data
    print("\n=== Test 6: Empty Data ===")
    console.print_content([], 'empty_test')

if __name__ == "__main__":
    test_print_content()
