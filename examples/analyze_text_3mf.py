#!/usr/bin/env python3
"""Analyze text.3mf file to check for modifiable text content."""

from noah123d import Archive3mf, Directory, Model
import json

def analyze_text_3mf():
    """Analyze the text.3mf file structure and content."""
    try:
        # Analyze text.3mf file
        with Archive3mf('text.3mf', 'r') as archive:
            print('Archive contents:')
            contents = archive.list_contents()
            for content in contents:
                print(f'  {content}')
            
            # Check for metadata that might contain text strings
            print('\nLooking for metadata files...')
            metadata_files = [c for c in contents if 'Metadata' in c or 'metadata' in c.lower()]
            print(f'Metadata files found: {metadata_files}')
            
            # Check if there are any text files in the archive
            text_files = [c for c in contents if c.endswith('.txt') or c.endswith('.json') or c.endswith('.xml')]
            print(f'Text files found: {text_files}')
            
            # Try to read the main 3D model file
            model_files = [c for c in contents if '3D/' in c and c.endswith('.model')]
            print(f'Model files found: {model_files}')
            
            # Try to read raw content of model files to look for text
            for model_file in model_files:
                print(f'\nReading raw content of {model_file}...')
                try:
                    raw_content = archive.extract_file(model_file)
                    if raw_content:
                        content_str = raw_content.decode('utf-8', errors='ignore')
                        
                        # Look for the specific text strings
                        if 'Rissen Text' in content_str:
                            print(f'✅ Found "Rissen Text" in {model_file}')
                            # Find surrounding context
                            start = content_str.find('Rissen Text')
                            context = content_str[max(0, start-100):start+200]
                            print(f'Context: ...{context}...')
                            
                        if 'Sunken Text' in content_str:
                            print(f'✅ Found "Sunken Text" in {model_file}')
                            # Find surrounding context
                            start = content_str.find('Sunken Text')
                            context = content_str[max(0, start-100):start+200]
                            print(f'Context: ...{context}...')
                            
                        # Look for any text-related tags or attributes
                        text_indicators = ['text', 'name', 'displayname', 'title', 'label']
                        for indicator in text_indicators:
                            if indicator in content_str.lower():
                                print(f'Found potential text indicator: {indicator}')
                    else:
                        print(f'Could not extract content from {model_file}')
                            
                except Exception as e:
                    print(f'Error reading {model_file}: {e}')
                    
            # Also check metadata files for text content
            print('\nChecking metadata files for text content...')
            for meta_file in metadata_files:
                if meta_file.endswith('.xml') or meta_file.endswith('.config'):
                    print(f'\nReading {meta_file}...')
                    try:
                        raw_content = archive.extract_file(meta_file)
                        if raw_content:
                            content_str = raw_content.decode('utf-8', errors='ignore')
                            
                            # Look for the specific text strings
                            if 'Rissen Text' in content_str:
                                print(f'✅ Found "Rissen Text" in {meta_file}')
                                start = content_str.find('Rissen Text')
                                context = content_str[max(0, start-100):start+200]
                                print(f'Context: ...{context}...')
                                
                            if 'Sunken Text' in content_str:
                                print(f'✅ Found "Sunken Text" in {meta_file}')
                                start = content_str.find('Sunken Text')
                                context = content_str[max(0, start-100):start+200]
                                print(f'Context: ...{context}...')
                                
                    except Exception as e:
                        print(f'Error reading {meta_file}: {e}')
            
            # Try to read model data using the model API
            print('\nAnalyzing using Model API...')
            try:
                with Directory('3D') as models_dir:
                    with Model() as model:
                        object_count = model.get_object_count()
                        print(f'Found {object_count} objects in the model')
                        
                        for obj_id in model.list_objects():
                            obj = model.get_object(obj_id)
                            if obj:
                                print(f'Object {obj_id}:')
                                print(f'  Type: {obj.get("type", "unknown")}')
                                print(f'  Properties: {list(obj.keys())}')
                                
                                # Check if there are any string properties
                                for key, value in obj.items():
                                    if isinstance(value, str):
                                        if any(text in value.lower() for text in ['text', 'rissen', 'sunken']):
                                            print(f'  Found text in {key}: {value}')
                                            
                                # Check for name or displayname properties specifically
                                if 'name' in obj:
                                    print(f'  Object name: {obj["name"]}')
                                if 'displayname' in obj:
                                    print(f'  Object display name: {obj["displayname"]}')
                                    
            except Exception as e:
                print(f'Error reading model using API: {e}')
                
    except FileNotFoundError:
        print('text.3mf file not found in current directory')
    except Exception as e:
        print(f'Error analyzing text.3mf: {e}')

if __name__ == '__main__':
    analyze_text_3mf()
