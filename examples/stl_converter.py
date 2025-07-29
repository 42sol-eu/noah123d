"""Simple STL to 3MF converter utility."""

from pathlib import Path
from typing import Optional, Union
from noah123d import Archive3mf, Directory, Model


def stl_to_3mf(stl_path: Union[str, Path], output_path: Union[str, Path], 
               include_metadata: bool = True) -> bool:
    """
    Convert an STL file to 3MF format.
    
    Args:
        stl_path: Path to the input STL file
        output_path: Path for the output 3MF file
        include_metadata: Whether to include conversion metadata (default: True)
        
    Returns:
        True if conversion was successful, False otherwise
        
    Example:
        >>> from noah123d.converters import stl_to_3mf
        >>> success = stl_to_3mf("model.stl", "model.3mf")
        >>> print(f"Conversion {'successful' if success else 'failed'}")
    """
    try:
        stl_path = Path(stl_path)
        output_path = Path(output_path)
        
        if not stl_path.exists():
            print(f"Error: STL file not found: {stl_path}")
            return False
            
        # Create the 3MF archive
        with Archive3mf(output_path, 'w') as archive:
            # Create the 3D directory
            with Directory('3D') as models_dir:
                # Create a model and add the STL
                with Model() as model:
                    # Add the STL object to the model
                    obj_id = model.add_object_from_stl(stl_path)
                    
                    if include_metadata:
                        # Get object info for metadata
                        obj = model.get_object(obj_id)
                        vertex_count = len(obj['vertices']) if obj else 0
                        triangle_count = len(obj['triangles']) if obj else 0
                        
                        # Create metadata
                        with Directory('Metadata') as metadata_dir:
                            metadata_content = f"""STL to 3MF Conversion Report
Source File: {stl_path.name}
Output File: {output_path.name}
Converter: Noah123D STL Converter
Date: {Path(__file__).stat().st_mtime}

Model Statistics:
- Objects: {model.get_object_count()}
- Vertices: {vertex_count:,}
- Triangles: {triangle_count:,}

Conversion successful!
"""
                            metadata_dir.create_file('conversion_report.txt', metadata_content)
        
        return True
        
    except Exception as e:
        print(f"Conversion failed: {e}")
        return False


def get_stl_info(stl_path: Union[str, Path]) -> Optional[dict]:
    """
    Get information about an STL file without converting it.
    
    Args:
        stl_path: Path to the STL file
        
    Returns:
        Dictionary with STL file information, or None if file cannot be read
        
    Example:
        >>> from noah123d.converters import get_stl_info
        >>> info = get_stl_info("model.stl")
        >>> if info:
        ...     print(f"Triangles: {info['triangles']}")
    """
    try:
        from stl import mesh
        
        stl_path = Path(stl_path)
        if not stl_path.exists():
            return None
            
        stl_mesh = mesh.Mesh.from_file(str(stl_path))
        
        # Calculate unique vertices
        vertices = set()
        triangle_count = len(stl_mesh.vectors)
        
        for triangle in stl_mesh.vectors:
            for vertex in triangle:
                vertices.add(tuple(vertex))
        
        return {
            'file_path': str(stl_path),
            'file_size': stl_path.stat().st_size,
            'triangles': triangle_count,
            'unique_vertices': len(vertices),
            'total_vertices': triangle_count * 3,
            'bounding_box': {
                'min': stl_mesh.min_.tolist(),
                'max': stl_mesh.max_.tolist()
            },
            'dimensions': (stl_mesh.max_ - stl_mesh.min_).tolist()
        }
        
    except Exception as e:
        print(f"Error reading STL file: {e}")
        return None


def batch_stl_to_3mf(input_pattern: str, output_dir: Union[str, Path] = "converted",
                     include_metadata: bool = True) -> list:
    """
    Convert multiple STL files matching a pattern to 3MF format.
    
    Args:
        input_pattern: Glob pattern for STL files (e.g., "models/*.stl")
        output_dir: Directory to save converted 3MF files
        include_metadata: Whether to include conversion metadata
        
    Returns:
        List of successfully converted file paths
        
    Example:
        >>> from noah123d.converters import batch_stl_to_3mf
        >>> converted = batch_stl_to_3mf("models/*.stl", "output")
        >>> print(f"Converted {len(converted)} files")
    """
    from pathlib import Path
    import glob
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    stl_files = glob.glob(input_pattern)
    converted_files = []
    
    for stl_file in stl_files:
        stl_path = Path(stl_file)
        output_path = output_dir / f"{stl_path.stem}.3mf"
        
        if stl_to_3mf(stl_path, output_path, include_metadata):
            converted_files.append(str(output_path))
        
    return converted_files


if __name__ == "__main__":
    # Simple test/demo
    print("Noah123D STL to 3MF Converter")
    print("=============================")
    
    # Test with the available STL file
    test_stl = Path("_models/multiverse/tile_2x2_borde.stl")
    test_output = Path("test_conversion.3mf")
    
    if test_stl.exists():
        print(f"Testing conversion: {test_stl.name}")
        
        # Get STL info first
        info = get_stl_info(test_stl)
        if info:
            print(f"STL Info:")
            print(f"  File size: {info['file_size']:,} bytes")
            print(f"  Triangles: {info['triangles']:,}")
            print(f"  Unique vertices: {info['unique_vertices']:,}")
            print(f"  Dimensions: {info['dimensions']}")
        
        # Convert to 3MF
        success = stl_to_3mf(test_stl, test_output)
        print(f"Conversion: {'✅ Success' if success else '❌ Failed'}")
        
        if success and test_output.exists():
            print(f"Output file: {test_output} ({test_output.stat().st_size:,} bytes)")
    else:
        print(f"Test STL file not found: {test_stl}")
        print("Please place an STL file in the _models directory to test.")
