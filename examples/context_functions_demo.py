"""Example demonstrating context-aware functions for both directories and models."""

from pathlib import Path
import tempfile

from noah123d import Archive3mf
from noah123d.directories import ThreeD, add_thumbnail, create_model_file
from noah123d.model import Model, add_object, get_object_count, list_objects


def example_context_functions():
    """Example showing how to use context functions without object names."""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "example.3mf"
        
        print("Creating 3MF archive with context functions...")
        
        with Archive3mf(archive_path, 'w') as archive:
            print(f"✓ Created archive: {archive.file_path}")
            
            with ThreeD() as threed:
                print("✓ Created 3D directory")
                
                # Add thumbnail using context function (no threed.add_thumbnail needed)
                add_thumbnail("preview.png", b"fake_png_data")
                print("✓ Added thumbnail using context function")
                
                # Create model file using context function
                create_model_file("shapes.model", "<model>placeholder</model>")
                print("✓ Created model file using context function")
                
                # Work with the model using context functions
                with Model("shapes.model") as model:
                    print("✓ Created model context")
                    
                    # Add objects using context functions (no model.add_object needed)
                    vertices1 = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
                    triangles1 = [[0, 1, 2]]
                    obj1 = add_object(vertices1, triangles1, "triangle")
                    print(f"✓ Added triangle object (ID: {obj1}) using context function")
                    
                    # Add a square using context functions
                    vertices2 = [[2, 0, 0], [3, 0, 0], [3, 1, 0], [2, 1, 0]]
                    triangles2 = [[0, 1, 2], [0, 2, 3]]
                    obj2 = add_object(vertices2, triangles2, "square")
                    print(f"✓ Added square object (ID: {obj2}) using context function")
                    
                    # Check results using context functions
                    count = get_object_count()
                    objects = list_objects()
                    print(f"✓ Model contains {count} objects: {objects}")
                    
        print(f"✓ Archive saved to: {archive_path}")
        return archive_path


def example_mixed_usage():
    """Example showing mixed usage of context functions and instance methods."""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "mixed_example.3mf"
        
        print("\nCreating 3MF archive with mixed function usage...")
        
        with Archive3mf(archive_path, 'w') as archive:
            with ThreeD() as threed:
                with Model("mixed.model") as model:
                    
                    # Mix context functions and instance methods
                    vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
                    triangles = [[0, 1, 2]]
                    
                    # Add using context function
                    obj1 = add_object(vertices, triangles, "context_triangle")
                    
                    # Add using instance method
                    obj2 = model.add_object(vertices, triangles, "instance_triangle")
                    
                    # Check results with both approaches
                    context_count = get_object_count()
                    instance_count = model.get_object_count()
                    
                    context_objects = list_objects()
                    instance_objects = model.list_objects()
                    
                    print(f"✓ Context function count: {context_count}")
                    print(f"✓ Instance method count: {instance_count}")
                    print(f"✓ Both methods see the same data: {context_count == instance_count}")
                    print(f"✓ Context objects: {context_objects}")
                    print(f"✓ Instance objects: {instance_objects}")
                    
        return archive_path


if __name__ == "__main__":
    # Run examples
    print("=" * 60)
    print("Context Functions Example")
    print("=" * 60)
    
    example_archive1 = example_context_functions()
    example_archive2 = example_mixed_usage()
    
    print(f"\n✅ Examples completed!")
    print(f"Created archives:")
    print(f"  - {example_archive1}")
    print(f"  - {example_archive2}")
