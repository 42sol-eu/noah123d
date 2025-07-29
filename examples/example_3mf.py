"""Example usage of the Archive3mf, Directory, and Model classes."""

from pathlib import Path
from noah123d import Archive3mf, Directory, Model


def create_sample_3mf():
    """Create a sample 3MF file with a simple cube."""
    output_path = Path("arc.3mf")
    
    # Create the 3MF archive
    with Archive3mf(output_path, 'w') as archive:
        print(f"Created archive: {archive.file_path}")
        
        # Create the 3D directory
        with Directory('3D') as models_dir:
            print(f"Created directory: {models_dir.get_archive_path()}")
            
            # Create a model and add a cube
            with Model() as model:
                print("Creating a simple cube model...")
                
                # Define cube vertices (unit cube)
                vertices = [
                    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # bottom face
                    [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]   # top face
                ]
                
                # Define cube triangles (2 triangles per face, 6 faces = 12 triangles)
                triangles = [
                    # Bottom face
                    [0, 1, 2], [0, 2, 3],
                    # Top face  
                    [4, 7, 6], [4, 6, 5],
                    # Front face
                    [0, 4, 5], [0, 5, 1],
                    # Back face
                    [2, 6, 7], [2, 7, 3],
                    # Left face
                    [0, 3, 7], [0, 7, 4],
                    # Right face
                    [1, 5, 6], [1, 6, 2]
                ]
                
                # Add the cube to the model
                obj_id = model.add_object(vertices, triangles)
                print(f"Added cube with object ID: {obj_id}")
                print(f"Model now contains {model.get_object_count()} objects")
                
        # Create additional directories for metadata
        with Directory('Metadata') as metadata_dir:
            metadata_dir.create_file('info.txt', 'Created with Noah123D')
            print(f"Created metadata directory with info file")
            
    print(f"3MF file created successfully: {output_path}")
    return output_path


def read_3mf_info(file_path: Path):
    """Read and display information about a 3MF file."""
    print(f"\nReading 3MF file: {file_path}")
    
    with Archive3mf(file_path, 'r') as archive:
        print("Archive contents:")
        for content in archive.list_contents():
            print(f"  - {content}")
            
        # Read the model
        with Directory('3D') as models_dir:
            with Model() as model:
                print(f"\nModel contains {model.get_object_count()} objects:")
                for obj_id in model.list_objects():
                    obj = model.get_object(obj_id)
                    if obj:
                        print(f"  Object {obj_id}: {len(obj['vertices'])} vertices, {len(obj['triangles'])} triangles")


if __name__ == "__main__":
    # Create a sample 3MF file
    sample_file = create_sample_3mf()
    
    # Read it back
    read_3mf_info(sample_file)
    
    print("\nExample completed successfully!")
