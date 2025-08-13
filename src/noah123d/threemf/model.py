
"""Model class for managing 3D objects within a 3MF archive.]

"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from contextvars import ContextVar
import numpy as np
from stl import mesh
from rich import print
from noah123d.visual.console import Console as NoahConsole

from ..core.context_decorators import context_function

from .archive import Archive, current_archive
from .directory import Directory, current_directory, current_directory

# Context variable to track the current model
current_model: ContextVar[Optional['Model']] = ContextVar('current_model', default=None)


class Model:
    """Manages 3D objects within a 3MF archive."""
    
    def __init__(self, name: str = "3dmodel.model"):
        """
        Initialize the Model.
        
        Args:
            name: Name of the model file (default: "3dmodel.model")
        """
        self.name = name
        self._context_token = None
        self._parent_archive: Optional[Archive] = None
        self._parent_directory: Optional[Directory] = None
        self._objects: List[Dict[str, Any]] = []
        self._next_object_id = 1
        self.console = NoahConsole()
        
    def __enter__(self) -> 'Model':
        """Enter the context manager."""
        # Set this model as the current model in context
        self._context_token = current_model.set(self)
        
        # Get parent contexts
        self._parent_archive = current_archive.get()
        self._parent_directory = current_directory.get()
        
        if not self._parent_archive:
            raise RuntimeError("Model must be used within an Archive context")
            
        # Load existing model if it exists
        self._load_existing_model()
        
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager."""
        # Only save the model if the archive is writable
        if self._parent_archive and self._parent_archive.is_writable():
            self._save_model()
        
        # Reset the context variable
        if self._context_token:
            current_model.reset(self._context_token)
            
    def _load_existing_model(self):
        """Load existing model from the archive."""
        if not self._parent_archive:
            return
        
        # Get the model directory name from parent directory context
        model_dir = self._parent_directory.path.name if self._parent_directory else "3D"
        model_path = f"{model_dir}/{self.name}"
        model_data = self._parent_archive.extract_file(model_path)
        
        if model_data:
            try:
                root = ET.fromstring(model_data.decode('utf-8'))
                self._parse_existing_objects(root)
            except (ET.ParseError, UnicodeDecodeError):
                # If parsing fails, start with empty model
                pass
                
    def _parse_existing_objects(self, root: ET.Element):
        """Parse existing objects from XML."""
        # Find all object elements
        ns = {'model': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
        
        for obj_elem in root.findall('.//model:object', ns):
            obj_id = int(obj_elem.get('id', 0))
            obj_type = obj_elem.get('type', 'model')
            
            # Update next object ID
            if obj_id >= self._next_object_id:
                self._next_object_id = obj_id + 1
                
            # Parse mesh data if present
            mesh_elem = obj_elem.find('model:mesh', ns)
            vertices = []
            triangles = []
            
            if mesh_elem is not None:
                # Parse vertices
                for vertex_elem in mesh_elem.findall('model:vertices/model:vertex', ns):
                    x = float(vertex_elem.get('x', 0))
                    y = float(vertex_elem.get('y', 0))
                    z = float(vertex_elem.get('z', 0))
                    vertices.append([x, y, z])
                    
                # Parse triangles
                for triangle_elem in mesh_elem.findall('model:triangles/model:triangle', ns):
                    v1 = int(triangle_elem.get('v1', 0))
                    v2 = int(triangle_elem.get('v2', 0))
                    v3 = int(triangle_elem.get('v3', 0))
                    triangles.append([v1, v2, v3])
                    
            self._objects.append({
                'id': obj_id,
                'type': obj_type,
                'vertices': vertices,
                'triangles': triangles
            })
            
    def _save_model(self):
        """Save the model to the archive."""
        if not self._parent_archive:
            return
            
        # Create XML structure
        model_xml = self._create_model_xml()
        
        # Get the model directory name from parent directory context
        model_dir = self._parent_directory.path.name if self._parent_directory else "3D"
        model_path = f"{model_dir}/{self.name}"
        self._parent_archive.add_file(model_path, model_xml)
        
    def _create_model_xml(self) -> str:
        """Create the 3MF model XML."""
        # Create root element
        root = ET.Element('model')
        root.set('unit', 'millimeter')
        root.set('xmlns', 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02')
        
        # Create resources element
        resources = ET.SubElement(root, 'resources')
        
        # Add objects
        for obj in self._objects:
            obj_elem = ET.SubElement(resources, 'object')
            obj_elem.set('id', str(obj['id']))
            obj_elem.set('type', obj['type'])
            
            if obj['vertices'] and obj['triangles']:
                # Create mesh
                mesh_elem = ET.SubElement(obj_elem, 'mesh')
                
                # Add vertices
                vertices_elem = ET.SubElement(mesh_elem, 'vertices')
                for vertex in obj['vertices']:
                    vertex_elem = ET.SubElement(vertices_elem, 'vertex')
                    vertex_elem.set('x', str(vertex[0]))
                    vertex_elem.set('y', str(vertex[1]))
                    vertex_elem.set('z', str(vertex[2]))
                    
                # Add triangles
                triangles_elem = ET.SubElement(mesh_elem, 'triangles')
                for triangle in obj['triangles']:
                    triangle_elem = ET.SubElement(triangles_elem, 'triangle')
                    triangle_elem.set('v1', str(triangle[0]))
                    triangle_elem.set('v2', str(triangle[1]))
                    triangle_elem.set('v3', str(triangle[2]))
                    
        # Create build element
        build = ET.SubElement(root, 'build')
        for obj in self._objects:
            if obj['type'] == 'model':  # Only add model objects to build
                item = ET.SubElement(build, 'item')
                item.set('objectid', str(obj['id']))
                
        # Convert to string
        ET.indent(root, space="  ", level=0)
        return ET.tostring(root, encoding='unicode', xml_declaration=True)
        
    def add_object_from_stl(self, stl_path: Union[str, Path]) -> int:
        """
        Add an object from an STL file.
        
        Args:
            stl_path: Path to the STL file
            
        Returns:
            Object ID of the added object
        """
        stl_mesh = mesh.Mesh.from_file(str(stl_path))
        
        # Convert STL mesh to vertices and triangles
        vertices = []
        triangles = []
        
        vertex_map = {}
        vertex_index = 0
        
        for triangle in stl_mesh.vectors:
            triangle_indices = []
            
            for vertex in triangle:
                # Create a hashable key for the vertex
                vertex_key = tuple(vertex)
                
                if vertex_key not in vertex_map:
                    vertex_map[vertex_key] = vertex_index
                    # Handle both numpy arrays and plain lists
                    if hasattr(vertex, 'tolist'):
                        vertices.append(vertex.tolist())
                    else:
                        vertices.append(list(vertex))
                    vertex_index += 1
                    
                triangle_indices.append(vertex_map[vertex_key])
                
            triangles.append(triangle_indices)
            
        return self.add_object(vertices, triangles)
        
    def add_object( self, vertices: List[List[float]], triangles: List[List[int]], 
                    obj_type: str = "model") -> int:
        """
        Add a 3D object to the model.
        
        Args:
            vertices: List of vertex coordinates [x, y, z]
            triangles: List of triangle vertex indices [v1, v2, v3]
            obj_type: Type of object (default: "model")
            
        Returns:
            Object ID of the added object
        """
        obj_id = self._next_object_id
        self._next_object_id += 1
        
        self._objects.append({
            'id': obj_id,
            'type': obj_type,
            'vertices': vertices,
            'triangles': triangles
        })
        
        return obj_id
        
    def remove_object(self, obj_id: int) -> bool:
        """
        Remove an object from the model.
        
        Args:
            obj_id: ID of the object to remove
            
        Returns:
            True if object was removed, False if not found
        """
        for i, obj in enumerate(self._objects):
            if obj['id'] == obj_id:
                del self._objects[i]
                return True
        return False
        
    def get_object(self, obj_id: int) -> Optional[Dict[str, Any]]:
        """Get an object by ID."""
        for obj in self._objects:
            if obj['id'] == obj_id:
                return obj.copy()
        return None
        
    def list_objects(self) -> List[int]:
        """List all object IDs in the model."""
        return [obj['id'] for obj in self._objects]
        
    def get_object_count(self) -> int:
        """Get the number of objects in the model."""
        return len(self._objects)
        
    def clear_objects(self):
        """Remove all objects from the model."""
        self._objects.clear()
        self._next_object_id = 1
        
    @classmethod
    def get_current(cls) -> Optional['Model']:
        """Get the current model from context."""
        return current_model.get()
        
    @classmethod
    def get_parent_archive(cls) -> Optional[Archive]:
        """Get the parent archive from context."""
        return current_archive.get()

    @classmethod
    def get_parent_directory(cls) -> Optional[Directory]:
        """Get the parent directory from context."""
        return current_directory.get()
 
    @classmethod
    def create_simple_cube(cls, size: float = 1.0) -> 'Model':
        vertices = [
            [0, 0, 0],
            [size, 0, 0],
            [size, size, 0],
            [0, size, 0],
            [0, 0, size],
            [size, 0, size],
            [size, size, size],
            [0, size, size],
        ]
        triangles = [
            [0, 1, 2], [0, 2, 3],  # bottom
            [4, 5, 6], [4, 6, 7],  # top
            [0, 1, 5], [0, 5, 4],  # front
            [1, 2, 6], [1, 6, 5],  # right
            [2, 3, 7], [2, 7, 6],  # back
            [3, 0, 4], [3, 4, 7],  # left
        ]
        model = Model("cube.model")
        model.add_object(vertices, triangles)
        return model
        
   
    def load_stl_with_info(self, stl_path: Path) -> Optional[int]:
        """
        Load an STL file into this model with console output.
        
        Args:
            stl_path: Path to the STL file
            
        Returns:
            Object ID of the loaded STL or None if failed
        """
        if not stl_path.exists():
            self.console.print_error(f"Error: STL file not found: {stl_path}")
            return None
        
        # Add the STL object to the model
        obj_id = self.add_object_from_stl(stl_path)
        
        # Get object info
        obj = self.get_object(obj_id)
        if obj:
            vertex_count = len(obj['vertices'])
            triangle_count = len(obj['triangles'])
            self.console.print_stl_loading_info(stl_path, obj_id, vertex_count, triangle_count)
            
        return obj_id
    
    def analyze_model_content(self) -> None:
        """
        Analyze and display detailed information about this model.
        """
        objects = [self.get_object(obj_id) for obj_id in self.list_objects()]
        objects = [obj for obj in objects if obj is not None]  # Filter out None objects
        
        self.console.print_model_content_analysis(objects, self.get_object_count())
    
    def add_conversion_metadata(self, stl_path: Path) -> None:
        """
        Add conversion metadata to the current archive context.
        This method works within an existing Archive and Directory context.
        
        Args:
            stl_path: Path to the original STL file
        """
        # Get the parent archive and directory from context
        archive = self.get_parent_archive()
        if not archive:
            self.console.print_error("Error: No archive context available")
            return
            
        # Create metadata directory with conversion info
        with Directory('Metadata') as metadata_dir:
            metadata_content = f"""STL to 3MF Conversion
Source STL: {stl_path.name}
Converted by: Noah123d STL Converter
Objects: {self.get_object_count()}
Conversion Date: {Path.cwd()}
"""
            metadata_dir.create_file('conversion_info.txt', metadata_content)
            self.console.print_metadata_added()
    

    
    @classmethod
    def convert_stl_to_3mf(cls, stl_path: Path, output_path: Path) -> Optional[Path]:
        """
        Convert an STL file to a 3MF archive using the context system.
        
        Args:
            stl_path: Path to the input STL file
            output_path: Path to the output 3MF file
            
        Returns:
            Path to the created 3MF file or None if conversion failed
        """
        console = NoahConsole()
        
        if not stl_path.exists():
            console.print_error(f"Error: STL file not found: {stl_path}")
            return None

        console.print_start('conversion', 
                            {'summary': 'STL to 3MF', 
                                '- input': stl_path, 
                                '- output': output_path})

        # Create the 3MF archive using the context system
        with Archive(output_path, 'w') as archive:
            console.print_archive_created(archive.file_path)
            
            # Create the 3D directory using the context system
            with Directory('3D') as models_dir:
                console.print_directory_created("3D models")
                
                # Create a model within the directory context
                with cls("3dmodel.model") as model:
                    # Load STL using the new method
                    obj_id = model.load_stl_with_info(stl_path)
                    if obj_id is None:
                        return None
                    
                    object_count = model.get_object_count()
                    
            # Create metadata directory with conversion info
            with Directory('Metadata') as metadata_dir:
                metadata_content = f"""STL to 3MF Conversion
Source STL: {stl_path.name}
Converted by: Noah123d STL Converter
Objects: {object_count}
"""
                metadata_dir.create_file('conversion_info.txt', metadata_content)
                console.print_metadata_added()
                
        console.print_success("conversion")
        return output_path
    
    @classmethod
    def analyze_3mf_content(cls, file_path: Path) -> None:
        """
        Analyze and display detailed information about a 3MF file using the context system.
        
        Args:
            file_path: Path to the 3MF file to analyze
        """
        console = NoahConsole()
        
        if not file_path.exists():
            console.print_error(f"Error: 3MF file not found: {file_path}")
            return
            
        console.print_analyzing_file(file_path)
        
        # Open archive using the context system
        with Archive(file_path, 'r') as archive:
            # Show archive contents
            contents = archive.list_contents()
            console.print_archive_contents(contents)
                
            # Access the 3D directory using the context system
            with Directory('3D') as models_dir:
                # Create model within the directory context
                with cls("3dmodel.model") as model:
                    # Use the new analyze method
                    model.analyze_model_content()
    
    @classmethod
    def batch_convert_stl_files(cls, input_dir: Path, output_dir: Path) -> List[Path]:
        """
        Convert all STL files in a directory to 3MF format.
        
        Args:
            input_dir: Directory containing STL files
            output_dir: Directory to save 3MF files
            
        Returns:
            List of successfully converted 3MF files
        """
        console = NoahConsole()
        
        if not input_dir.exists():
            console.print_error(f"Error: Input directory not found: {input_dir}")
            return []
            
        # Find all STL files
        stl_files = list(input_dir.glob("**/*.stl"))
        
        if not stl_files:
            console.print_no_stl_files_found(input_dir)
            return []
            
        console.print_batch_conversion_start(len(stl_files))
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        converted_files = []
        
        for stl_file in stl_files:
            # Create output filename
            output_file = output_dir / f"{stl_file.stem}.3mf"
            
            console.print_processing_file(stl_file.name)
            
            try:
                result = cls.convert_stl_to_3mf(stl_file, output_file)
                if result:
                    converted_files.append(result)
                    console.print_converted_file(output_file.name)
            except Exception as e:
                console.print_conversion_failed(stl_file.name, e)
        
        console.print_batch_conversion_complete(len(converted_files), output_dir)
        
        return converted_files


# Module-level convenience functions using decorators
@context_function(current_model)
def add_object_from_stl(stl_path: Union[str, Path]) -> int:
    """Add an object from an STL file to the current model.
    
    Must be called within a Model context manager.
    """
    pass  # Implementation handled by decorator


@context_function(current_model)
def add_object(vertices: List[List[float]], triangles: List[List[int]], 
               obj_type: str = "model") -> int:
    """Add a 3D object to the current model.
    
    Must be called within a Model context manager.
    """
    pass  # Implementation handled by decorator


@context_function(current_model)
def remove_object(obj_id: int) -> bool:
    """Remove an object from the current model.
    
    Must be called within a Model context manager.
    """
    pass  # Implementation handled by decorator


@context_function(current_model)
def get_object(obj_id: int) -> Optional[Dict[str, Any]]:
    """Get an object by ID from the current model.
    
    Must be called within a Model context manager.
    """
    pass  # Implementation handled by decorator


@context_function(current_model)
def list_objects() -> List[int]:
    """List all object IDs in the current model.
    
    Must be called within a Model context manager.
    """
    pass  # Implementation handled by decorator


@context_function(current_model)
def get_object_count() -> int:
    """Get the number of objects in the current model.
    
    Must be called within a Model context manager.
    """
    pass  # Implementation handled by decorator


@context_function(current_model)
def clear_objects() -> None:
    """Remove all objects from the current model.
    
    Must be called within a Model context manager.
    """
    pass  # Implementation handled by decorator


@context_function(current_model)
def load_stl_with_info(stl_path: Path) -> Optional[int]:
    """Load an STL file into the current model with console output.
    
    Must be called within a Model context manager.
    """
    pass  # Implementation handled by decorator


@context_function(current_model)
def analyze_model_content() -> None:
    """Analyze and display detailed information about the current model.
    
    Must be called within a Model context manager.
    """
    pass  # Implementation handled by decorator


@context_function(current_model)
def add_conversion_metadata(stl_path: Path) -> None:
    """Add conversion metadata to the current archive context.
    
    Must be called within a Model context manager.
    """
    pass  # Implementation handled by decorator
