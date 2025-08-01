#!/usr/bin/env python3
"""Simple verification script to test the configuration loading."""

import toml

def test_config():
    """Test configuration loading."""
    # Load the configuration file
    with open("ark.toml", 'r', encoding='utf-8') as f:
        config = toml.load(f)
    
    # Assert that config was loaded and is a dictionary
    assert config is not None
    assert isinstance(config, dict)
    
    # Verify expected configuration sections exist
    assert 'export' in config
    assert 'processing' in config
    assert 'logging' in config
    
    # Verify expected keys exist with reasonable values
    export_config = config.get('export', {})
    processing_config = config.get('processing', {})
    logging_config = config.get('logging', {})
    
    # Check export configuration
    assert 'output_dir' in export_config
    assert isinstance(export_config['output_dir'], str)
    
    # Check processing configuration  
    assert 'create_backup' in processing_config
    assert isinstance(processing_config['create_backup'], bool)
    
    assert 'backup_dir' in processing_config
    assert isinstance(processing_config['backup_dir'], str)
    
    # Check logging configuration
    assert 'verbose' in logging_config
    assert isinstance(logging_config['verbose'], bool)
    
    print("Configuration loaded successfully:")
    print(f"  Output directory: {export_config['output_dir']}")
    print(f"  Create backup: {processing_config['create_backup']}")
    print(f"  Backup directory: {processing_config['backup_dir']}")
    print(f"  Verbose: {logging_config['verbose']}")

if __name__ == '__main__':
    test_config()
