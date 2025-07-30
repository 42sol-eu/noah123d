#!/usr/bin/env python3
"""
3MF Text Editor - A utility to modify text strings in 3MF files

This tool allows you to modify text content in 3MF files by editing the metadata
configuration files that contain text definitions used by slicer software.

Usage:
    python text_3mf_editor.py input.3mf output.3mf "Old Text" "New Text"
    python text_3mf_editor.py input.3mf output.3mf --interactive
    python text_3mf_editor.py input.3mf --list-text

Author: Noah123d Project
License: MIT
"""

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from noah123d import Archive3mf


class Text3MFEditor:
    """Editor for modifying text content in 3MF files."""
    
    def __init__(self, verbose: bool = False):
        """Initialize the editor."""
        self.verbose = verbose
        self.config_files = [
            'Metadata/Slic3r_PE_model.config',
            'Metadata/PrusaSlicer_model.config',
            'Metadata/model.config'
        ]
    
    def log(self, message: str):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(message)
    
    def find_text_strings(self, file_path: str) -> List[Tuple[str, str]]:
        """
        Find all text strings in a 3MF file.
        
        Args:
            file_path: Path to the 3MF file
            
        Returns:
            List of tuples (config_file, text_content) containing found text
        """
        text_strings = []
        
        try:
            with Archive3mf(file_path, 'r') as archive:
                for config_file in self.config_files:
                    config_content = archive.extract_file(config_file)
                    if config_content:
                        config_str = config_content.decode('utf-8', errors='ignore')
                        
                        # Find text in name attributes
                        lines = config_str.split('\n')
                        for line_num, line in enumerate(lines, 1):
                            line = line.strip()
                            
                            # Look for name value attributes
                            if 'key="name"' in line and 'value=' in line:
                                start = line.find('value="') + 7
                                end = line.find('"', start)
                                if start > 6 and end > start:
                                    text_value = line[start:end]
                                    if text_value and not text_value.startswith('printer_kit'):
                                        text_strings.append((config_file, text_value))
                            
                            # Look for slic3rpe:text elements
                            if 'slic3rpe:text' in line and 'text=' in line:
                                start = line.find('text="') + 6
                                end = line.find('"', start)
                                if start > 5 and end > start:
                                    text_value = line[start:end]
                                    if text_value:
                                        text_strings.append((config_file, text_value))
                
        except Exception as e:
            self.log(f"Error reading file: {e}")
        
        return text_strings
    
    def list_text_content(self, file_path: str) -> bool:
        """
        List all text content found in a 3MF file.
        
        Args:
            file_path: Path to the 3MF file
            
        Returns:
            True if text was found, False otherwise
        """
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return False
        
        print(f"🔍 Searching for text content in: {file_path}")
        print("=" * 60)
        
        text_strings = self.find_text_strings(file_path)
        
        if not text_strings:
            print("❌ No modifiable text content found in this 3MF file.")
            print("\nNote: This tool looks for text in slicer metadata files.")
            print("Text that is part of the 3D mesh geometry cannot be modified.")
            return False
        
        print(f"✅ Found {len(text_strings)} text string(s):")
        print()
        
        seen_texts = set()
        for i, (config_file, text) in enumerate(text_strings, 1):
            if text not in seen_texts:
                print(f"{i:2d}. \"{text}\"")
                print(f"    Location: {config_file}")
                seen_texts.add(text)
        
        print()
        print("💡 To modify text, use:")
        print(f"   python {sys.argv[0]} \"{file_path}\" \"output.3mf\" \"Old Text\" \"New Text\"")
        
        return True
    
    def modify_text(self, input_file: str, output_file: str, 
                   text_replacements: Dict[str, str], create_backup: bool = True) -> bool:
        """
        Modify text strings in a 3MF file.
        
        Args:
            input_file: Path to input 3MF file
            output_file: Path to output 3MF file
            text_replacements: Dictionary of {old_text: new_text} replacements
            create_backup: Whether to create a backup of the input file
            
        Returns:
            True if modification was successful, False otherwise
        """
        if not os.path.exists(input_file):
            print(f"❌ Input file not found: {input_file}")
            return False
        
        # Create backup if requested
        if create_backup and input_file != output_file:
            backup_file = f"{input_file}.backup"
            if not os.path.exists(backup_file):
                try:
                    shutil.copy2(input_file, backup_file)
                    print(f"📁 Created backup: {backup_file}")
                except Exception as e:
                    print(f"⚠️  Warning: Could not create backup: {e}")
        
        try:
            modifications_made = False
            
            with Archive3mf(input_file, 'r') as source_archive:
                # Find which config files exist and contain text
                existing_configs = {}
                
                for config_file in self.config_files:
                    config_content = source_archive.extract_file(config_file)
                    if config_content:
                        existing_configs[config_file] = config_content.decode('utf-8')
                
                if not existing_configs:
                    print("❌ No slicer configuration files found in this 3MF file.")
                    print("   This file may not contain modifiable text content.")
                    return False
                
                # Apply text replacements to each config file
                modified_configs = {}
                
                for config_file, config_str in existing_configs.items():
                    original_config = config_str
                    
                    for old_text, new_text in text_replacements.items():
                        # Replace in name attributes
                        old_name_attr = f'value="{old_text}"'
                        new_name_attr = f'value="{new_text}"'
                        config_str = config_str.replace(old_name_attr, new_name_attr)
                        
                        # Replace in slic3rpe:text elements
                        old_text_attr = f'text="{old_text}"'
                        new_text_attr = f'text="{new_text}"'
                        config_str = config_str.replace(old_text_attr, new_text_attr)
                    
                    if config_str != original_config:
                        modified_configs[config_file] = config_str
                        modifications_made = True
                        self.log(f"Modified: {config_file}")
                
                if not modifications_made:
                    print("⚠️  No matching text found to replace.")
                    print("   Use --list-text to see available text content.")
                    return False
                
                # Create the output file
                with Archive3mf(output_file, 'w') as dest_archive:
                    # Copy all files from source
                    for filename in source_archive.list_contents():
                        if filename in modified_configs:
                            # Use modified version
                            dest_archive.add_file(filename, modified_configs[filename])
                        else:
                            # Copy original
                            file_content = source_archive.extract_file(filename)
                            if file_content:
                                dest_archive.add_file(filename, file_content)
                
                print(f"✅ Successfully created modified 3MF: {output_file}")
                
                # Report what was changed
                for old_text, new_text in text_replacements.items():
                    print(f"   🔄 '{old_text}' → '{new_text}'")
                
                return True
                
        except Exception as e:
            print(f"❌ Error modifying 3MF file: {e}")
            return False
    
    def interactive_mode(self, input_file: str, output_file: str) -> bool:
        """
        Interactive mode for text replacement.
        
        Args:
            input_file: Path to input 3MF file
            output_file: Path to output 3MF file
            
        Returns:
            True if modification was successful, False otherwise
        """
        print("🎯 Interactive Text Editor Mode")
        print("=" * 40)
        
        # First, list available text
        text_strings = self.find_text_strings(input_file)
        
        if not text_strings:
            print("❌ No modifiable text content found.")
            return False
        
        # Show available text
        unique_texts = list(set(text for _, text in text_strings))
        print(f"Found {len(unique_texts)} unique text string(s):")
        print()
        
        for i, text in enumerate(unique_texts, 1):
            print(f"{i:2d}. \"{text}\"")
        
        print()
        
        # Get replacements from user
        replacements = {}
        
        while True:
            print("Enter text to replace (or press Enter to finish):")
            old_text = input("> ").strip()
            
            if not old_text:
                break
            
            if old_text not in unique_texts:
                print(f"⚠️  Text '{old_text}' not found. Available texts:")
                for text in unique_texts:
                    print(f"   - \"{text}\"")
                continue
            
            print(f"Enter new text to replace '{old_text}':")
            new_text = input("> ").strip()
            
            if not new_text:
                print("❌ New text cannot be empty.")
                continue
            
            replacements[old_text] = new_text
            print(f"✅ Added replacement: '{old_text}' → '{new_text}'")
            print()
        
        if not replacements:
            print("❌ No replacements specified.")
            return False
        
        # Perform the modification
        return self.modify_text(input_file, output_file, replacements)


def main():
    """Main command-line interface."""
    parser = argparse.ArgumentParser(
        description="Modify text content in 3MF files",
        epilog="""
Examples:
  %(prog)s input.3mf output.3mf "Old Text" "New Text"
  %(prog)s input.3mf output.3mf --interactive
  %(prog)s input.3mf --list-text
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('input_file', help='Input 3MF file')
    parser.add_argument('output_file', nargs='?', help='Output 3MF file')
    parser.add_argument('old_text', nargs='?', help='Text to replace')
    parser.add_argument('new_text', nargs='?', help='New text')
    
    parser.add_argument('--list-text', action='store_true',
                       help='List all text content in the file')
    parser.add_argument('--interactive', action='store_true',
                       help='Interactive mode for multiple replacements')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    parser.add_argument('--no-backup', action='store_true',
                       help='Do not create backup file')
    
    args = parser.parse_args()
    
    # Initialize editor
    editor = Text3MFEditor(verbose=args.verbose)
    
    # Handle list-text mode
    if args.list_text:
        return editor.list_text_content(args.input_file)
    
    # Validate arguments for modification modes
    if not args.output_file:
        print("❌ Output file is required for modification modes.")
        parser.print_help()
        return False
    
    # Handle interactive mode
    if args.interactive:
        return editor.interactive_mode(args.input_file, args.output_file)
    
    # Handle single replacement mode
    if not args.old_text or not args.new_text:
        print("❌ Both old_text and new_text are required for single replacement mode.")
        parser.print_help()
        return False
    
    replacements = {args.old_text: args.new_text}
    return editor.modify_text(args.input_file, args.output_file, replacements, 
                             create_backup=not args.no_backup)


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
