#!/usr/bin/env python3
"""Detailed analysis of the text strings in text.3mf."""

from noah123d import Archive3mf
import xml.etree.ElementTree as ET

def detailed_text_analysis():
    """Provide detailed analysis of text modification possibilities."""
    try:
        with Archive3mf('text.3mf', 'r') as archive:
            # Read the Slic3r_PE_model.config file which contains the text
            config_content = archive.extract_file('Metadata/Slic3r_PE_model.config')
            if config_content:
                config_str = config_content.decode('utf-8')
                
                print("=== DETAILED TEXT ANALYSIS ===")
                print(f"Text strings found in: Metadata/Slic3r_PE_model.config")
                print(f"File type: XML metadata file (Slicer configuration)")
                print()
                
                # Parse as XML to understand structure
                try:
                    root = ET.fromstring(config_str)
                    print("XML structure analysis:")
                    
                    # Find all volume elements with text names
                    for volume in root.findall('.//volume'):
                        for metadata in volume.findall('metadata'):
                            if metadata.get('key') == 'name':
                                name_value = metadata.get('value')
                                if name_value in ['Rissen Text', 'Sunken Text']:
                                    print(f"\\n📝 Text Element Found:")
                                    print(f"   Text: '{name_value}'")
                                    print(f"   Volume ID range: {volume.get('firstid')} to {volume.get('lastid')}")
                                    
                                    # Get other metadata for this volume
                                    print(f"   Volume properties:")
                                    for meta in volume.findall('metadata'):
                                        key = meta.get('key')
                                        value = meta.get('value')
                                        print(f"     {key}: {value}")
                                        
                except ET.ParseError as e:
                    print(f"XML parsing error: {e}")
                    # Fallback to text search
                    print("\\nFallback text search:")
                    lines = config_str.split('\\n')
                    for i, line in enumerate(lines):
                        if 'Rissen Text' in line or 'Sunken Text' in line:
                            print(f"Line {i+1}: {line.strip()}")
                            if i > 0:
                                print(f"Previous: {lines[i-1].strip()}")
                            if i < len(lines) - 1:
                                print(f"Next: {lines[i+1].strip()}")
                            print()
                
                print("\\n=== MODIFICATION ANALYSIS ===")
                print("✅ Text Modifiability Assessment:")
                print("1. Text Location: Metadata/Slic3r_PE_model.config (Slicer metadata)")
                print("2. Text Format: XML metadata with 'name' attribute")
                print("3. Text Purpose: Volume/object naming in slicer software")
                print("4. Modification Method: Edit XML metadata file")
                print()
                print("🔧 How to Modify:")
                print("- Extract the 3MF file (it's a ZIP archive)")
                print("- Edit Metadata/Slic3r_PE_model.config")
                print("- Find <metadata type='volume' key='name' value='...'/>")
                print("- Change the 'value' attribute")
                print("- Re-zip the contents back to .3mf")
                print()
                print("⚠️  Important Notes:")
                print("- These are slicer software metadata (PrusaSlicer/Slic3r)")
                print("- Text changes will affect how the model appears in slicer")
                print("- The actual 3D geometry remains unchanged")
                print("- Changes may not be visible in all 3D viewers")
                print("- Original text might be regenerated if model is re-sliced")
                
    except Exception as e:
        print(f"Error in detailed analysis: {e}")

if __name__ == '__main__':
    detailed_text_analysis()
