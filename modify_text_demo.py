#!/usr/bin/env python3
"""Demonstrate how to modify text in text.3mf file."""

from noah123d import Archive3mf
import os
import shutil
from pathlib import Path

def modify_text_in_3mf(input_file: str, output_file: str, text_replacements: dict):
    """
    Modify text strings in a 3MF file.
    
    Args:
        input_file: Path to input 3MF file
        output_file: Path to output 3MF file
        text_replacements: Dict of {'old_text': 'new_text'} pairs
    """
    try:
        # Create a backup
        backup_file = f"{input_file}.backup"
        if not os.path.exists(backup_file):
            shutil.copy2(input_file, backup_file)
            print(f"📁 Created backup: {backup_file}")
        
        # Read the original file
        with Archive3mf(input_file, 'r') as source_archive:
            # Extract the metadata config file
            config_content = source_archive.extract_file('Metadata/Slic3r_PE_model.config')
            if not config_content:
                print("❌ Could not find Metadata/Slic3r_PE_model.config")
                return False
            
            # Convert to string and apply replacements
            config_str = config_content.decode('utf-8')
            original_config = config_str
            
            # Apply text replacements
            for old_text, new_text in text_replacements.items():
                # Replace in name attributes
                old_name_attr = f'value="{old_text}"'
                new_name_attr = f'value="{new_text}"'
                config_str = config_str.replace(old_name_attr, new_name_attr)
                
                # Replace in slic3rpe:text elements
                old_text_attr = f'text="{old_text}"'
                new_text_attr = f'text="{new_text}"'
                config_str = config_str.replace(old_text_attr, new_text_attr)
                
                print(f"🔄 Replaced '{old_text}' with '{new_text}'")
            
            # Check if any changes were made
            if config_str == original_config:
                print("⚠️  No text replacements were found")
                return False
            
            # Create new 3MF file with modified content
            with Archive3mf(output_file, 'w') as dest_archive:
                # Copy all files from source except the config file
                for filename in source_archive.list_contents():
                    if filename != 'Metadata/Slic3r_PE_model.config':
                        file_content = source_archive.extract_file(filename)
                        if file_content:
                            dest_archive.add_file(filename, file_content)
                
                # Add the modified config file
                dest_archive.add_file('Metadata/Slic3r_PE_model.config', config_str)
            
            print(f"✅ Successfully created modified 3MF: {output_file}")
            return True
            
    except Exception as e:
        print(f"❌ Error modifying 3MF file: {e}")
        return False

def demonstrate_text_modification():
    """Demonstrate text modification capabilities."""
    print("=== 3MF TEXT MODIFICATION DEMONSTRATION ===\\n")
    
    input_file = "text.3mf"
    output_file = "text_modified.3mf"
    
    if not os.path.exists(input_file):
        print(f"❌ Input file {input_file} not found")
        return
    
    # Define text replacements
    replacements = {
        "Rissen Text": "Raised Text",
        "Sunken Text": "Engraved Text"
    }
    
    print(f"📂 Input file: {input_file}")
    print(f"📂 Output file: {output_file}")
    print(f"🔄 Text replacements:")
    for old, new in replacements.items():
        print(f"   '{old}' → '{new}'")
    print()
    
    # Perform the modification
    success = modify_text_in_3mf(input_file, output_file, replacements)
    
    if success:
        print(f"\\n🎉 Text modification completed!")
        print(f"\\n📋 Summary:")
        print(f"   • Original file: {input_file}")
        print(f"   • Modified file: {output_file}")
        print(f"   • Backup created: {input_file}.backup")
        print(f"   • Text changes: {len(replacements)} replacements")
        
        # Verify the changes
        print(f"\\n🔍 Verifying changes...")
        with Archive3mf(output_file, 'r') as verify_archive:
            config_content = verify_archive.extract_file('Metadata/Slic3r_PE_model.config')
            if config_content:
                config_str = config_content.decode('utf-8')
                for old_text, new_text in replacements.items():
                    if new_text in config_str:
                        print(f"   ✅ Found '{new_text}' in modified file")
                    else:
                        print(f"   ❌ Could not find '{new_text}' in modified file")
    else:
        print(f"\\n❌ Text modification failed!")

if __name__ == '__main__':
    demonstrate_text_modification()
