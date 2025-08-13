"""Example showing the new specialized directory classes."""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from noah123d import Archive, ThreeD, Metadata, Textures, Model

def demonstrate_specialized_directories():
    """Demonstrate the new specialized directory classes."""
    
    output_path = Path("example_specialized.3mf")
    
    with Archive(output_path, 'w') as archive:
        print(f"✓ Created 3MF archive: {archive.file_path}")
        
        # Using the specialized ThreeD directory
        with ThreeD() as models_dir:
            print("✓ Created 3D models directory using ThreeD class")
            
            # Create a simple model using the Model class
            with Model("test.model") as model:
                # Add a simple cube
                vertices = [
                    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # bottom
                    [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1],  # top
                ]
                triangles = [
                    [0, 1, 2], [0, 2, 3],  # bottom
                    [4, 5, 6], [4, 6, 7],  # top
                    [0, 1, 5], [0, 5, 4],  # front
                    [1, 2, 6], [1, 6, 5],  # right
                    [2, 3, 7], [2, 7, 6],  # back
                    [3, 0, 4], [3, 4, 7],  # left
                ]
                model.add_object(vertices, triangles)
                print("✓ Added cube model")
            
            # List model files using the specialized method
            model_files = models_dir.list_model_files()
            print(f"✓ Found model files: {model_files}")
        
        # Using the specialized Metadata directory
        with Metadata() as meta_dir:
            print("✓ Created Metadata directory using Metadata class")
            
            # Add conversion information using the specialized method
            meta_dir.add_conversion_info(
                source_file="cube.stl",
                converter="noah123d",
                objects_count=1,
                additional_info={
                    "author": "Demo User",
                    "purpose": "Demonstration"
                }
            )
            print("✓ Added conversion information")
            
            # Add properties using the specialized method
            meta_dir.add_properties({
                "material": "PLA",
                "color": "red",
                "infill": "20%"
            })
            print("✓ Added properties metadata")
            
            # Add custom metadata
            meta_dir.add_custom_metadata(
                "custom_info.json", 
                '{"version": "1.0", "type": "demo"}',
                "Custom JSON metadata for demo purposes"
            )
            print("✓ Added custom metadata")
        
        # Using the specialized Textures directory (optional)
        with Textures() as textures_dir:
            print("✓ Created Textures directory using Textures class")
            
            # Simulate adding a texture (in real use, you'd have actual image data)
            fake_image_data = b"fake_png_data_here"
            textures_dir.add_texture("red_texture.png", fake_image_data, "color")
            print("✓ Added texture file")
            
            # List texture files
            texture_files = textures_dir.list_texture_files()
            print(f"✓ Found texture files: {texture_files}")
    
    print(f"\n🎉 Successfully created {output_path} using specialized directory classes!")
    return output_path

def compare_old_vs_new_syntax():
    """Show the difference between old and new syntax."""
    print("\n" + "="*60)
    print("COMPARISON: Old vs New Syntax")
    print("="*60)
    
    print("\nOLD SYNTAX (still supported):")
    print("```python")
    print("with Directory('3D') as models_dir:")
    print("    models_dir.create_file('3dmodel.model', xml_content)")
    print("with Directory('Metadata') as meta_dir:")
    print("    meta_dir.create_file('conversion_info.txt', info)")
    print("```")
    
    print("\nNEW SYNTAX (recommended):")
    print("```python")
    print("with ThreeD() as models_dir:")
    print("    models_dir.create_model_file('3dmodel.model', xml_content)")
    print("with Metadata() as meta_dir:")
    print("    meta_dir.add_conversion_info(source_file, converter, count)")
    print("```")
    
    print("\nBENEFITS OF NEW SYNTAX:")
    print("✓ Type safety - each directory has specific methods")
    print("✓ Better validation - model files must end with .model")
    print("✓ Convenience methods - add_conversion_info() vs manual file creation")
    print("✓ Self-documenting - ThreeD() clearly indicates 3D directory")
    print("✓ IDE support - better autocomplete and method discovery")

if __name__ == "__main__":
    demonstrate_specialized_directories()
    compare_old_vs_new_syntax()
