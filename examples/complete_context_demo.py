"""Complete example demonstrating all context-aware functions: Archive, Directory, and Model."""

from pathlib import Path
import tempfile

# Archive context functions
from noah123d.archive import Archive, add_file, list_contents, is_writable, get_temp_path

# Directory context functions
from noah123d.directories import ThreeD, add_thumbnail, create_model_file
from noah123d.directories import Metadata, add_conversion_info, add_properties

# Model context functions
from noah123d import Model, add_object, get_object_count, list_objects, analyze_model_content


def complete_context_example():
    """Complete example using all three types of context functions."""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "complete_example.3mf"
        
        print("🚀 Creating complete 3MF archive using context functions...")
        
        with Archive(archive_path, 'w') as archive:
            print(f"✓ Created archive: {archive.file_path}")
            print(f"✓ Archive is writable: {is_writable()}")
            
            # Add some direct archive files using context functions
            add_file("README.txt", "This 3MF was created using Noah123d context functions")
            add_file("metadata.json", '{"created_by": "noah123d", "version": "1.0"}')
            
            # Check archive contents using context function
            contents = list_contents()
            print(f"✓ Archive contains {len(contents)} files initially")
            
            with ThreeD() as threed:
                print("✓ Created 3D directory context")
                
                # Add thumbnail using context function (no threed.add_thumbnail needed)
                add_thumbnail("preview.png", b"fake_png_thumbnail_data")
                print("✓ Added thumbnail using context function")
                
                with Model("geometry.model") as model:
                    print("✓ Created model context")
                    
                    # Create complex geometry using context functions
                    # Triangle
                    triangle_vertices = [[0, 0, 0], [10, 0, 0], [5, 10, 0]]
                    triangle_faces = [[0, 1, 2]]
                    obj1 = add_object(triangle_vertices, triangle_faces, "triangle")
                    print(f"✓ Added triangle (ID: {obj1}) using context function")
                    
                    # Square made of two triangles
                    square_vertices = [
                        [20, 0, 0], [30, 0, 0], [30, 10, 0], [20, 10, 0]
                    ]
                    square_faces = [[0, 1, 2], [0, 2, 3]]
                    obj2 = add_object(square_vertices, square_faces, "square")
                    print(f"✓ Added square (ID: {obj2}) using context function")
                    
                    # Cube
                    cube_vertices = [
                        [0, 0, 10], [10, 0, 10], [10, 10, 10], [0, 10, 10],  # top
                        [0, 0, 0], [10, 0, 0], [10, 10, 0], [0, 10, 0]        # bottom
                    ]
                    cube_faces = [
                        [0, 1, 2], [0, 2, 3],  # top
                        [4, 5, 6], [4, 6, 7],  # bottom
                        [0, 1, 5], [0, 5, 4],  # front
                        [1, 2, 6], [1, 6, 5],  # right
                        [2, 3, 7], [2, 7, 6],  # back
                        [3, 0, 4], [3, 4, 7],  # left
                    ]
                    obj3 = add_object(cube_vertices, cube_faces, "cube")
                    print(f"✓ Added cube (ID: {obj3}) using context function")
                    
                    # Check model state using context functions
                    count = get_object_count()
                    objects = list_objects()
                    print(f"✓ Model contains {count} objects: {objects}")
                    
                    # Analyze model using context function
                    print("📊 Model analysis:")
                    analyze_model_content()
            
            with Metadata() as metadata:
                print("✓ Created metadata directory context")
                
                # Add conversion info using context function
                add_conversion_info(
                    source_file="original_shapes.blend",
                    converter="noah123d",
                    objects_count=3,
                    additional_info={
                        "triangles": 16,
                        "vertices": 16,
                        "export_quality": "high"
                    }
                )
                print("✓ Added conversion info using context function")
                
                # Add properties using context function
                add_properties({
                    "title": "Complex Geometry Example",
                    "author": "Noah123d Context Functions",
                    "description": "Demonstrates triangle, square, and cube objects",
                    "creation_date": "2025-07-31",
                    "software": "noah123d-context-demo"
                })
                print("✓ Added properties using context function")
            
            # Check final archive contents using context function
            final_contents = list_contents()
            print(f"✓ Final archive contains {len(final_contents)} files:")
            for content in sorted(final_contents):
                print(f"   📄 {content}")
            
            # Show temp path info using context function
            temp_path = get_temp_path()
            print(f"✓ Temporary files stored in: {temp_path}")
                    
        print(f"✅ Complete archive saved to: {archive_path}")
        return archive_path


def nested_context_comparison():
    """Compare nested context usage with traditional instance methods."""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        
        print("\n" + "="*60)
        print("Context Functions vs Instance Methods Comparison")
        print("="*60)
        
        # Context functions approach
        context_path = Path(temp_dir) / "context_approach.3mf"
        
        print("\n🔵 Using Context Functions:")
        with Archive(context_path, 'w') as archive:
            with ThreeD() as threed:
                with Model("shapes.model") as model:
                    # All using context functions - no object names needed!
                    add_file("info.txt", "Created with context functions")
                    add_thumbnail("thumb.png", b"thumbnail_data")
                    obj_id = add_object([[0,0,0], [1,0,0], [0,1,0]], [[0,1,2]])
                    
                    print(f"  ✓ Archive writable: {is_writable()}")
                    print(f"  ✓ Object count: {get_object_count()}")
                    print(f"  ✓ Archive files: {len(list_contents())}")
        
        # Instance methods approach
        instance_path = Path(temp_dir) / "instance_approach.3mf"
        
        print("\n🔴 Using Instance Methods:")
        with Archive(instance_path, 'w') as archive:
            with ThreeD() as threed:
                with Model("shapes.model") as model:
                    # Traditional approach - need object names
                    archive.add_file("info.txt", "Created with instance methods")
                    threed.add_thumbnail("thumb.png", b"thumbnail_data")
                    obj_id = model.add_object([[0,0,0], [1,0,0], [0,1,0]], [[0,1,2]])
                    
                    print(f"  ✓ Archive writable: {archive.is_writable()}")
                    print(f"  ✓ Object count: {model.get_object_count()}")
                    print(f"  ✓ Archive files: {len(archive.list_contents())}")
        
        print("\n✅ Both approaches produce equivalent results!")
        print("Context functions just make the code cleaner and less repetitive.")
        
        return context_path, instance_path


if __name__ == "__main__":
    print("=" * 70)
    print("Noah123d Complete Context Functions Demo")
    print("=" * 70)
    
    # Run complete example
    complete_archive = complete_context_example()
    
    # Run comparison
    context_archive, instance_archive = nested_context_comparison()
    
    print(f"\n🎉 Demo completed successfully!")
    print(f"Created archives:")
    print(f"  • Complete example: {complete_archive}")
    print(f"  • Context approach: {context_archive}")
    print(f"  • Instance approach: {instance_archive}")
    
    print(f"\n💡 Key benefits of context functions:")
    print(f"  • Cleaner, more readable code")
    print(f"  • Less repetitive context object references")
    print(f"  • Same functionality as instance methods")
    print(f"  • Proper error handling for incorrect usage")
    print(f"  • Full backward compatibility")
