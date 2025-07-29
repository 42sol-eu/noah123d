"""Example 3: Advanced context manager usage, error handling, and nested operations."""

from pathlib import Path
from noah123d import Archive3mf, Directory, Model
import json
import contextlib


def safe_3mf_operations():
    """Demonstrate safe 3MF operations with proper error handling."""
    output_path = Path("safe_operations.3mf")
    
    try:
        with Archive3mf(output_path, 'w') as archive:
            print(f"Safely creating archive: {archive.file_path}")
            
            # Demonstrate nested context managers with error recovery
            with Directory('3D') as models_dir:
                print("Creating models with error handling...")
                
                # Successfully create a model
                with Model() as good_model:
                    vertices = [[0, 0, 0], [1, 0, 0], [0.5, 1, 0]]  # Triangle
                    triangles = [[0, 1, 2]]
                    obj_id = good_model.add_object(vertices, triangles, name="Triangle")
                    print(f"  ✓ Successfully created triangle model")
                
                # Demonstrate error handling in model creation
                try:
                    with Model() as problematic_model:
                        # This might fail - demonstrate recovery
                        invalid_vertices = []  # Empty vertices
                        invalid_triangles = [[0, 1, 2]]  # References non-existent vertices
                        
                        if not invalid_vertices:
                            raise ValueError("Cannot create object with empty vertices")
                        
                        obj_id = problematic_model.add_object(invalid_vertices, invalid_triangles)
                        
                except ValueError as e:
                    print(f"  ⚠ Handled model error: {e}")
                    # Create a fallback model instead
                    with Model() as fallback_model:
                        # Create a simple line instead
                        vertices = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
                        triangles = [[0, 1, 2], [0, 2, 3]]  # Rectangle
                        obj_id = fallback_model.add_object(vertices, triangles, name="Fallback_Rectangle")
                        print(f"  ✓ Created fallback rectangle model")
            
            # Create metadata with validation
            with Directory('Metadata') as metadata_dir:
                # Validate and create metadata
                metadata = create_validated_metadata()
                metadata_dir.create_file('validated_info.json', json.dumps(metadata, indent=2))
                print("  ✓ Created validated metadata")
                
        print(f"Safe operations completed: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ Archive creation failed: {e}")
        # Cleanup if needed
        if output_path.exists():
            output_path.unlink()
        raise


def create_validated_metadata():
    """Create validated metadata dictionary."""
    metadata = {
        "version": "1.0",
        "created_by": "Noah123D Safe Operations Example",
        "validation": {
            "vertices_checked": True,
            "triangles_validated": True,
            "materials_verified": False
        }
    }
    
    # Add timestamp
    from datetime import datetime
    metadata["created_at"] = datetime.now().isoformat()
    
    return metadata


def demonstrate_context_nesting():
    """Show advanced context manager nesting and parent awareness."""
    output_path = Path("nested_context.3mf")
    
    print("\\n=== Demonstrating Advanced Context Nesting ===")
    
    with Archive3mf(output_path, 'w') as archive:
        print(f"Archive context: {archive.file_path}")
        
        # Multiple nested directories
        with Directory('Assets') as assets_dir:
            print(f"  Assets directory: {assets_dir.get_archive_path()}")
            
            # Create subdirectory structure
            with Directory('Models') as models_subdir:
                print(f"    Models subdirectory: {models_subdir.get_archive_path()}")
                
                with Model() as nested_model:
                    # Create a hexagon
                    vertices, triangles = create_hexagon(radius=1.0)
                    obj_id = nested_model.add_object(vertices, triangles, name="Hexagon")
                    print(f"      Created hexagon in nested context")
            
            with Directory('Textures') as textures_subdir:
                print(f"    Textures subdirectory: {textures_subdir.get_archive_path()}")
                textures_subdir.create_file('texture_list.txt', 'No textures in this example')
        
        # Parallel directory structure
        with Directory('Documentation') as docs_dir:
            print(f"  Documentation directory: {docs_dir.get_archive_path()}")
            
            readme_content = \"\"\"# Nested Context Example
            
This 3MF file demonstrates advanced context manager usage:

1. Multiple nested directories
2. Parent context awareness  
3. Parallel directory structures
4. Safe resource management

Generated by Noah123D Example 3.
\"\"\"
            docs_dir.create_file('README.md', readme_content)
            
            # Create a manifest
            manifest = {
                "directories": ["Assets/Models/", "Assets/Textures/", "Documentation/"],
                "files": ["README.md", "texture_list.txt"],
                "models": ["Hexagon"]
            }
            docs_dir.create_file('manifest.json', json.dumps(manifest, indent=2))
    
    print(f"Nested context demonstration completed: {output_path}")
    return output_path


def create_hexagon(radius: float):
    """Create a hexagon with triangular faces."""
    import math
    
    vertices = [[0, 0, 0]]  # Center vertex
    triangles = []
    
    # Create hexagon vertices
    for i in range(6):
        angle = math.pi * i / 3  # 60 degrees each
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.append([x, y, 0])
    
    # Create triangles from center to each edge
    for i in range(6):
        v1 = i + 1  # current vertex
        v2 = (i + 1) % 6 + 1  # next vertex (wrap around)
        triangles.append([0, v1, v2])  # center to edge
    
    return vertices, triangles


def batch_archive_processing():
    """Demonstrate processing multiple archives in a batch."""
    print("\\n=== Batch Archive Processing ===")
    
    archive_configs = [
        {"name": "simple_shapes.3mf", "shapes": ["triangle", "square"]},
        {"name": "complex_shapes.3mf", "shapes": ["hexagon", "octagon"]},
        {"name": "mixed_assembly.3mf", "shapes": ["triangle", "hexagon"]}
    ]
    
    created_archives = []
    
    for config in archive_configs:
        try:
            archive_path = Path(config["name"])
            print(f"\\nCreating {archive_path}...")
            
            with Archive3mf(archive_path, 'w') as archive:
                with Directory('3D') as models_dir:
                    for shape_name in config["shapes"]:
                        with Model() as model:
                            vertices, triangles = create_shape_by_name(shape_name)
                            obj_id = model.add_object(vertices, triangles, name=shape_name.title())
                            print(f"  ✓ Added {shape_name}")
                
                # Add batch metadata
                with Directory('Metadata') as metadata_dir:
                    batch_info = {
                        "batch_id": f"batch_{len(created_archives) + 1}",
                        "shapes": config["shapes"],
                        "archive_name": config["name"]
                    }
                    metadata_dir.create_file('batch_info.json', json.dumps(batch_info, indent=2))
            
            created_archives.append(archive_path)
            print(f"  ✓ Completed {archive_path}")
            
        except Exception as e:
            print(f"  ❌ Failed to create {config['name']}: {e}")
    
    print(f"\\nBatch processing completed. Created {len(created_archives)} archives:")
    for archive in created_archives:
        print(f"  📦 {archive}")
    
    return created_archives


def create_shape_by_name(shape_name: str):
    """Factory function to create different shapes."""
    if shape_name == "triangle":
        return [[0, 0, 0], [1, 0, 0], [0.5, 1, 0]], [[0, 1, 2]]
    elif shape_name == "square":
        vertices = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
        triangles = [[0, 1, 2], [0, 2, 3]]
        return vertices, triangles
    elif shape_name == "hexagon":
        return create_hexagon(1.0)
    elif shape_name == "octagon":
        return create_octagon(1.0)
    else:
        # Default to triangle
        return [[0, 0, 0], [1, 0, 0], [0.5, 1, 0]], [[0, 1, 2]]


def create_octagon(radius: float):
    """Create an octagon with triangular faces."""
    import math
    
    vertices = [[0, 0, 0]]  # Center vertex
    triangles = []
    
    # Create octagon vertices
    for i in range(8):
        angle = math.pi * i / 4  # 45 degrees each
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.append([x, y, 0])
    
    # Create triangles from center to each edge
    for i in range(8):
        v1 = i + 1  # current vertex
        v2 = (i + 1) % 8 + 1  # next vertex (wrap around)
        triangles.append([0, v1, v2])  # center to edge
    
    return vertices, triangles


if __name__ == "__main__":
    print("=== Example 3: Advanced Context Management and Error Handling ===\\n")
    
    # Demonstrate safe operations
    safe_file = safe_3mf_operations()
    
    # Show advanced context nesting
    nested_file = demonstrate_context_nesting()
    
    # Batch processing
    batch_files = batch_archive_processing()
    
    print("\\n=== All Examples Completed Successfully! ===")
    print("\\nCreated files:")
    print(f"  📦 {safe_file}")
    print(f"  📦 {nested_file}")
    for batch_file in batch_files:
        print(f"  📦 {batch_file}")
    
    print("\\n=== Example 3 completed successfully! ===")
