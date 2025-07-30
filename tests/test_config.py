#!/usr/bin/env python3
"""Simple verification script to test the configuration loading."""

import toml

def test_config():
    """Test configuration loading."""
    try:
        with open("ark.toml", 'r', encoding='utf-8') as f:
            config = toml.load(f)
        
        print("Configuration loaded successfully:")
        print(f"  Output directory: {config.get('export', {}).get('output_dir', 'NOT FOUND')}")
        print(f"  Create backup: {config.get('processing', {}).get('create_backup', 'NOT FOUND')}")
        print(f"  Verbose: {config.get('logging', {}).get('verbose', 'NOT FOUND')}")
        
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

if __name__ == '__main__':
    test_config()
