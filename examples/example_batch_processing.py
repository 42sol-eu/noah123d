"""Example 2: Batch processing and multiple models in a single 3MF archive."""

from pathlib import Path
from noah123d import Archive, Directory, Model
import json


def create_multi_model_3mf():
    """Create a 3MF file with multiple models and complex structure."""
    output_path = Path("complex_assembly.3mf")
    
    with Archive(output_path, 'w') as archive:
        print(f"Creating complex assembly: {archive.file_path}")
        
        # Create main 3D directory
        with Directory('3D') as models_dir:
            print("Creating multiple models...")
            
            # Model 1: Cylinder
            with Model() as cylinder_model:
                print("  Creating cylinder model...")
                vertices, triangles = create_cylinder(radius=1.0, height=2.0, segments=12)
                obj_id = cylinder_model.add_object(vertices, triangles, name="Cylinder")
                print(f"    Added cylinder with {len(vertices)} vertices, {len(triangles)} triangles")
            
            # Model 2: Pyramid
            with Model() as pyramid_model:
                print("  Creating pyramid model...")
                vertices, triangles = create_pyramid(base_size=2.0, height=1.5)
                obj_id = pyramid_model.add_object(vertices, triangles, name="Pyramid")
                print(f"    Added pyramid with {len(vertices)} vertices, {len(triangles)} triangles")
            
            # Model 3: Assembly combining previous models
            with Model() as assembly_model:
                print("  Creating assembly model...")
                # Add cylinder at origin
                cylinder_verts, cylinder_tris = create_cylinder(radius=0.5, height=1.0, segments=8)
                cylinder_id = assembly_model.add_object(cylinder_verts, cylinder_tris, name="Support")
                
                # Add pyramid on top (translate Z by cylinder height)
                pyramid_verts, pyramid_tris = create_pyramid(base_size=1.0, height=0.8)
                translated_verts = [[v[0], v[1], v[2] + 1.0] for v in pyramid_verts]
                pyramid_id = assembly_model.add_object(translated_verts, pyramid_tris, name="Top")
                
                print(f"    Assembly contains {assembly_model.get_object_count()} components")
        
        # Create metadata with build information
        with Directory('Metadata') as metadata_dir:
            build_info = {
                "created_by": "Noah123d Example 2",
                "creation_date": "2025-07-29",
                "models": ["Cylinder", "Pyramid", "Assembly"],
                "total_objects": 5,
                "description": "Complex multi-model 3MF assembly"
            }
            metadata_dir.create_file('build_info.json', json.dumps(build_info, indent=2))
            
            # Create material definitions
            materials = {
                "materials": [
                    {"id": 1, "name": "PLA", "color": "#FF0000", "density": 1.25},
                    {"id": 2, "name": "ABS", "color": "#00FF00", "density": 1.04},
                    {"id": 3, "name": "PETG", "color": "#0000FF", "density": 1.27}
                ]
            }
            metadata_dir.create_file('materials.json', json.dumps(materials, indent=2))
            print("    Created metadata files: build_info.json, materials.json")
        
        # Create textures directory (even if empty)
        with Directory('Textures') as textures_dir:
            textures_dir.create_file('readme.txt', 'This directory is reserved for texture files')
            print("    Created textures directory")
    
    print(f"Complex 3MF assembly created: {output_path}")
    return output_path


def create_cylinder(radius: float, height: float, segments: int):
    """Generate vertices and triangles for a cylinder."""
    vertices = []
    triangles = []
    
    # Bottom center vertex
    vertices.append([0, 0, 0])
    bottom_center = 0
    
    # Top center vertex  
    vertices.append([0, 0, height])
    top_center = 1
    
    # Bottom circle vertices
    import math
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.append([x, y, 0])  # bottom
        vertices.append([x, y, height])  # top
    
    # Bottom face triangles
    for i in range(segments):
        v1 = 2 + i * 2  # bottom vertex
        v2 = 2 + ((i + 1) % segments) * 2  # next bottom vertex
        triangles.append([bottom_center, v2, v1])
    
    # Top face triangles
    for i in range(segments):
        v1 = 3 + i * 2  # top vertex
        v2 = 3 + ((i + 1) % segments) * 2  # next top vertex
        triangles.append([top_center, v1, v2])
    
    # Side face triangles
    for i in range(segments):
        bottom1 = 2 + i * 2
        top1 = 3 + i * 2
        bottom2 = 2 + ((i + 1) % segments) * 2
        top2 = 3 + ((i + 1) % segments) * 2
        
        # Two triangles per side face
        triangles.append([bottom1, top1, bottom2])
        triangles.append([bottom2, top1, top2])
    
    return vertices, triangles


def create_pyramid(base_size: float, height: float):
    """Generate vertices and triangles for a pyramid."""
    half_base = base_size / 2
    
    vertices = [
        [-half_base, -half_base, 0],  # 0: base corner 1
        [half_base, -half_base, 0],   # 1: base corner 2
        [half_base, half_base, 0],    # 2: base corner 3
        [-half_base, half_base, 0],   # 3: base corner 4
        [0, 0, height]                # 4: apex
    ]
    
    triangles = [
        # Base (bottom face)
        [0, 2, 1], [0, 3, 2],
        # Side faces
        [0, 1, 4],  # front
        [1, 2, 4],  # right
        [2, 3, 4],  # back
        [3, 0, 4]   # left
    ]
    
    return vertices, triangles


def analyze_3mf_structure(file_path: Path):
    """Analyze and display the structure of a 3MF file."""
    print(f"\nAnalyzing 3MF file: {file_path}")
    
    with Archive(file_path, 'r') as archive:
        print("\\n=== Archive Structure ===")
        contents = archive.list_contents()
        directories = [c for c in contents if c.endswith('/')]
        files = [c for c in contents if not c.endswith('/')]
        
        print(f"Directories ({len(directories)}):")
        for dir_name in sorted(directories):
            print(f"  📁 {dir_name}")
            
        print(f"\\nFiles ({len(files)}):")
        for file_name in sorted(files):
            print(f"  📄 {file_name}")
        
        # Analyze models in 3D directory
        print("\\n=== 3D Models Analysis ===")
        try:
            with Directory('3D') as models_dir:
                with Model() as model:
                    object_count = model.get_object_count()
                    print(f"Total objects found: {object_count}")
                    
                    total_vertices = 0
                    total_triangles = 0
                    
                    for obj_id in model.list_objects():
                        obj = model.get_object(obj_id)
                        if obj:
                            vertices = len(obj['vertices'])
                            triangles = len(obj['triangles'])
                            name = obj.get('name', f'Object_{obj_id}')
                            
                            print(f"  🔺 {name}: {vertices} vertices, {triangles} triangles")
                            total_vertices += vertices
                            total_triangles += triangles
                    
                    print(f"\\nTotals: {total_vertices} vertices, {total_triangles} triangles")
        except Exception as e:
            print(f"Could not analyze 3D models: {e}")
        
        # Display metadata
        print("\\n=== Metadata ===")
        try:
            with Directory('Metadata') as metadata_dir:
                # Try to read build info
                try:
                    build_info_content = metadata_dir.read_file('build_info.json')
                    build_info = json.loads(build_info_content)
                    print("Build Information:")
                    for key, value in build_info.items():
                        print(f"  {key}: {value}")
                except:
                    print("No build_info.json found")
                
                # Try to read materials
                try:
                    materials_content = metadata_dir.read_file('materials.json')
                    materials = json.loads(materials_content)
                    print("\\nMaterials:")
                    for material in materials.get('materials', []):
                        print(f"  ID {material['id']}: {material['name']} ({material['color']})")
                except:
                    print("No materials.json found")
        except Exception as e:
            print(f"Could not read metadata: {e}")


if __name__ == "__main__":
    print("=== Example 2: Complex Multi-Model 3MF Assembly ===\\n")
    
    # Create complex assembly
    assembly_file = create_multi_model_3mf()
    
    # Analyze the created file
    analyze_3mf_structure(assembly_file)
    
    print("\\n=== Example 2 completed successfully! ===")
