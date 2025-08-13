#!/usr/bin/env python3
"""
Test context variable imports directly.
"""

import sys
sys.path.insert(0, 'src')

def test_imports():
    print("=== Testing Context Variable Imports ===")
    
    try:
        from noah123d.threemf.archive import current_archive
        print(f"✓ Imported current_archive: {current_archive}")
        print(f"  current_archive.get(): {current_archive.get()}")
    except Exception as e:
        print(f"✗ Failed to import current_archive: {e}")
    
    try:
        from noah123d.threemf.directory import current_directory
        print(f"✓ Imported current_directory: {current_directory}")
        print(f"  current_directory.get(): {current_directory.get()}")
    except Exception as e:
        print(f"✗ Failed to import current_directory: {e}")
        
    try:
        from noah123d.threemf.model import current_model  
        print(f"✓ Imported current_model: {current_model}")
        print(f"  current_model.get(): {current_model.get()}")
    except Exception as e:
        print(f"✗ Failed to import current_model: {e}")
    
    # Test if they're the same objects when imported from Console
    try:
        from noah123d.visual.console import current_archive as console_archive
        from noah123d.threemf.archive import current_archive as archive_archive
        print(f"\nAre they the same object? {console_archive is archive_archive}")
        print(f"Console archive: {id(console_archive)}")
        print(f"Archive archive: {id(archive_archive)}")
    except Exception as e:
        print(f"Error comparing objects: {e}")

if __name__ == "__main__":
    test_imports()
