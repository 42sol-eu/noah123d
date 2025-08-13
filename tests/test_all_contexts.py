#!/usr/bin/env python3
"""
Comprehensive test of context awareness for all context managers.
"""

import sys
sys.path.insert(0, 'src')

from noah123d.threemf import Archive, Directory, Model
from noah123d.threemf.metadata import Metadata
from noah123d.threemf.textures import Textures  
from noah123d.threemf.three_d import ThreeD
from noah123d.visual.console import Console

def test_all_contexts():
    console = Console()
    
    print("=== Testing All Context Manager Types ===")
    
    # Test outside any context
    print(f"1. Outside contexts: {console._detect_current_context()}")
    console.print_content(["file1.txt", "file2.txt"], None)
    
    # Test Archive context
    print(f"\n2. Testing Archive context...")
    with Archive("test.3mf", 'w') as archive:
        print(f"   Archive context: {console._detect_current_context()}")
        archive_files = ["3D/3dmodel.model", "[Content_Types].xml", "_rels/.rels", "Metadata/info.txt"]
        console.print_content(archive_files)
        
        # Test basic Directory context
        print(f"\n3. Testing basic Directory context...")
        with Directory('CustomDir') as directory:
            print(f"   Directory context: {console._detect_current_context()}")
            dir_files = ["custom1.txt", "custom2.dat"]
            console.print_content(dir_files)
        
        # Test ThreeD (3D) context
        print(f"\n4. Testing ThreeD context...")
        with ThreeD() as three_d:
            print(f"   ThreeD context: {console._detect_current_context()}")
            model_files = ["3dmodel.model", "thumbnail.png"]
            console.print_content(model_files)
            
            # Test Model context within ThreeD
            print(f"\n5. Testing Model context (within ThreeD)...")
            with Model() as model:
                print(f"   Model context: {console._detect_current_context()}")
                object_data = [
                    {'id': 1, 'vertices': 1000, 'triangles': 2000, 'type': 'mesh'},
                    {'id': 2, 'vertices': 1500, 'triangles': 3000, 'type': 'solid'}
                ]
                console.print_content(object_data)
        
        # Test Metadata context
        print(f"\n6. Testing Metadata context...")
        with Metadata() as metadata:
            print(f"   Metadata context: {console._detect_current_context()}")
            metadata_files = ["conversion_info.txt", "properties.xml", "description.md"]
            console.print_content(metadata_files)
        
        # Test Textures context
        print(f"\n7. Testing Textures context...")
        with Textures() as textures:
            print(f"   Textures context: {console._detect_current_context()}")
            texture_files = ["wood_diffuse.png", "metal_normal.jpg", "fabric_roughness.tiff"]
            console.print_content(texture_files)
    
    print(f"\n8. Back outside contexts: {console._detect_current_context()}")

if __name__ == "__main__":
    test_all_contexts()
