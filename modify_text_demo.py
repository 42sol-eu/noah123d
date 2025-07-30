#!/usr/bin/env python3
"""Demonstrate how to modify text in 3MF files and export them to a configured directory."""

from noah123d import Archive3mf
import os
import shutil
import toml
import glob
import fnmatch
from pathlib import Path

def load_config(config_file: str = "ark.toml") -> dict:
    """Load configuration from TOML file."""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = toml.load(f)
        return config
    except FileNotFoundError:
        print(f"❌ Configuration file {config_file} not found. Using defaults.")
        return {
            'export': {'output_dir': 'exported_3mf'},
            'processing': {'create_backup': True, 'backup_dir': None, 'include_patterns': ['*.3mf'], 'exclude_patterns': ['*.backup', '*_temp.3mf']},
            'logging': {'verbose': True}
        }
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return {}

def find_3mf_files(config: dict) -> list:
    """Find all 3MF files based on configuration patterns."""
    include_patterns = config.get('processing', {}).get('include_patterns', ['*.3mf'])
    exclude_patterns = config.get('processing', {}).get('exclude_patterns', ['*.backup', '*_temp.3mf'])
    
    found_files = []
    for pattern in include_patterns:
        found_files.extend(glob.glob(pattern))
    
    found_files = list(set(found_files))
    
    filtered_files = []
    for file_path in found_files:
        exclude = False
        for exclude_pattern in exclude_patterns:
            if fnmatch.fnmatch(file_path, exclude_pattern):
                exclude = True
                break
        if not exclude:
            filtered_files.append(file_path)
    
    return sorted(filtered_files)

def modify_text_in_3mf(input_file: str, output_dir: str, text_replacements: dict, create_backup: bool = True, backup_dir: str = None):
    """Modify text strings in a 3MF file and save to output directory."""
    try:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        input_path = Path(input_file)
        output_file = Path(output_dir) / f"{input_path.stem}_modified{input_path.suffix}"
        
        if create_backup:
            if backup_dir:
                Path(backup_dir).mkdir(parents=True, exist_ok=True)
                backup_file = Path(backup_dir) / f"{input_path.name}.backup"
            else:
                backup_file = f"{input_file}.backup"
            
            if not os.path.exists(backup_file):
                shutil.copy2(input_file, backup_file)
                print(f"📁 Created backup: {backup_file}")
            else:
                print(f"📁 Backup already exists: {backup_file}")
        
        with Archive3mf(input_file, 'r') as source_archive:
            config_content = source_archive.extract_file('Metadata/Slic3r_PE_model.config')
            if not config_content:
                print("❌ Could not find Metadata/Slic3r_PE_model.config")
                return False
            
            config_str = config_content.decode('utf-8')
            original_config = config_str
            
            for old_text, new_text in text_replacements.items():
                old_name_attr = f'value="{old_text}"'
                new_name_attr = f'value="{new_text}"'
                config_str = config_str.replace(old_name_attr, new_name_attr)
                
                old_text_attr = f'text="{old_text}"'
                new_text_attr = f'text="{new_text}"'
                config_str = config_str.replace(old_text_attr, new_text_attr)
                
                print(f"🔄 Replaced '{old_text}' with '{new_text}'")
            
            if config_str == original_config:
                print("⚠️  No text replacements were found")
                return False
            
            with Archive3mf(output_file, 'w') as dest_archive:
                for filename in source_archive.list_contents():
                    if filename != 'Metadata/Slic3r_PE_model.config':
                        file_content = source_archive.extract_file(filename)
                        if file_content:
                            dest_archive.add_file(filename, file_content)
                
                dest_archive.add_file('Metadata/Slic3r_PE_model.config', config_str)
            
            print(f"✅ Successfully created modified 3MF: {output_file}")
            return True
            
    except Exception as e:
        print(f"❌ Error modifying 3MF file: {e}")
        return False

def demonstrate_text_modification():
    """Demonstrate text modification capabilities for all 3MF files."""
    print("=== 3MF BULK TEXT MODIFICATION & EXPORT ===\\n")
    
    config = load_config("ark.toml")
    output_dir = config.get('export', {}).get('output_dir', 'exported_3mf')
    create_backup = config.get('processing', {}).get('create_backup', True)
    backup_dir = config.get('processing', {}).get('backup_dir', None)
    verbose = config.get('logging', {}).get('verbose', True)
    
    if verbose:
        print(f"📋 Configuration loaded:")
        print(f"   • Output directory: {output_dir}")
        print(f"   • Create backups: {create_backup}")
        if backup_dir:
            print(f"   • Backup directory: {backup_dir}")
        print()
    
    found_files = find_3mf_files(config)
    
    if not found_files:
        print("❌ No 3MF files found matching the configuration patterns")
        return
    
    print(f"📂 Found {len(found_files)} 3MF files to process:")
    for file_path in found_files:
        print(f"   • {file_path}")
    print()
    
    replacements = {
        "Rissen Text": "Raised Text",
        "Sunken Text": "Engraved Text",
        "Text": "Custom Text"
    }
    
    if verbose:
        print(f"🔄 Text replacements to apply:")
        for old, new in replacements.items():
            print(f"   '{old}' → '{new}'")
        print()
    
    successful_exports = 0
    failed_exports = 0
    
    for input_file in found_files:
        print(f"🔧 Processing: {input_file}")
        
        success = modify_text_in_3mf(input_file, output_dir, replacements, create_backup, backup_dir)
        
        if success:
            successful_exports += 1
            print(f"   ✅ Successfully exported")
        else:
            failed_exports += 1
            print(f"   ❌ Export failed")
        print()
    
    print(f"🎉 BULK EXPORT COMPLETED!")
    print(f"\\n📊 Summary:")
    print(f"   • Total files processed: {len(found_files)}")
    print(f"   • Successful exports: {successful_exports}")
    print(f"   • Failed exports: {failed_exports}")
    print(f"   • Output directory: {output_dir}")
    if backup_dir and create_backup:
        print(f"   • Backup directory: {backup_dir}")
    print(f"   • Text replacements applied: {len(replacements)}")
    
    if successful_exports > 0:
        print(f"\\n📁 Check the '{output_dir}' folder for your exported files!")
    
    if backup_dir and create_backup and os.path.exists(backup_dir):
        backup_files = list(Path(backup_dir).glob("*.backup"))
        if backup_files:
            print(f"\\n💾 Backup files created in '{backup_dir}':")
            for backup_file in backup_files:
                print(f"   • {backup_file}")
    
    if os.path.exists(output_dir):
        exported_files = list(Path(output_dir).glob("*.3mf"))
        if exported_files:
            print(f"\\n📋 Exported files:")
            for exported_file in exported_files:
                print(f"   • {exported_file}")

if __name__ == '__main__':
    demonstrate_text_modification()
