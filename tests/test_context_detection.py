#!/usr/bin/env python3
"""
Test context variable detection in Console class.
"""

import sys
sys.path.insert(0, 'src')

from noah123d.threemf import Archive, Directory, Model
from noah123d.visual.console import Console

def test_context_detection():
    console = Console()
    
    print("=== Testing Context Detection ===")
    
    # Test outside any context
    print(f"Outside contexts: {console._detect_current_context()}")
    
    # Test inside Archive context
    with Archive("test.3mf", 'w') as archive:
        print(f"Inside Archive: {console._detect_current_context()}")
        
        # Test data in archive context
        test_data = ["3D/model.file", "[Content_Types].xml", "_rels/.rels"]
        console.print_content(test_data)
        
        # Test inside Directory context
        with Directory('3D') as directory:
            print(f"Inside 3D Directory: {console._detect_current_context()}")
            
            # Test inside Model context
            with Model() as model:
                print(f"Inside Model: {console._detect_current_context()}")
                
                # Test object data in model context
                object_data = [
                    {'id': 1, 'vertices': 100, 'triangles': 200},
                    {'id': 2, 'vertices': 150, 'triangles': 300}
                ]
                console.print_content(object_data)

if __name__ == "__main__":
    test_context_detection()
