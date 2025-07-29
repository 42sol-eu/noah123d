"""Model class for managing 3D objects within a 3MF archive."""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from contextvars import ContextVar
import numpy as np
from stl import mesh

from .archive3mf import Archive3mf, current_archive
from .directory import Directory, current_directory

# Context variable to track the current model
current_model: ContextVar[Optional['Model']] = ContextVar('current_model', default=None)


class Model:
    """Manages 3D objects within a 3MF archive."""
    
    def __init__(self, name: str = "3dmodel.model", model_dir: str = "3D"):
        """
        Initialize the Model.
        
        Args:
            name: Name of the model file (default: "3dmodel.model")
            model_dir: Directory containing the model (default: "3D")
        """
        self.name = name
        self.model_dir = model_dir
        self._context_token = None
        self._parent_archive: Optional[Archive3mf] = None
        self._parent_directory: Optional[Directory] = None
        self._objects: List[Dict[str, Any]] = []
        self._next_object_id = 1
        
    def __enter__(self) -> 'Model':
        """Enter the context manager."""
        # Set this model as the current model in context
        self._context_token = current_model.set(self)
        
        # Get parent contexts
        self._parent_archive = current_archive.get()
        self._parent_directory = current_directory.get()
        
        if not self._parent_archive:
            raise RuntimeError("Model must be used within an Archive3mf context")
            
        # Load existing model if it exists
        self._load_existing_model()
        
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager."""
        # Save the model to the archive
        self._save_model()
        
        # Reset the context variable
        if self._context_token:
            current_model.reset(self._context_token)
            
    def _load_existing_model(self):
        """Load existing model from the archive."""
        if not self._parent_archive:
            return
            
        model_path = f"{self.model_dir}/{self.name}"
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
        
        # Save to archive
        model_path = f"{self.model_dir}/{self.name}"
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
                    vertices.append(vertex.tolist())
                    vertex_index += 1
                    
                triangle_indices.append(vertex_map[vertex_key])
                
            triangles.append(triangle_indices)
            
        return self.add_object(vertices, triangles)
        
    def add_object(self, vertices: List[List[float]], triangles: List[List[int]], 
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
    def get_parent_archive(cls) -> Optional[Archive3mf]:
        """Get the parent archive from context."""
        return current_archive.get()
        
    @classmethod
    def get_parent_directory(cls) -> Optional[Directory]:
        """Get the parent directory from context."""
        return current_directory.get()
