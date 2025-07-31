"""Specialized directory classes for 3MF archives."""

from pathlib import Path
from typing import Union, Optional, List, Dict, Any
from .directory import Directory


class ThreeD(Directory):
    """Specialized directory class for the 3D directory in 3MF archives.
    
    The 3D directory is required in 3MF archives and contains:
    - 3D model files (.model)
    - Optional thumbnails
    - Other 3D-related resources
    """
    
    def __init__(self, create: bool = True):
        """Initialize the 3D directory.
        
        Args:
            create: Whether to create the directory if it doesn't exist (default: True)
        """
        super().__init__("3D", create=create)
    
    def create_model_file(self, filename: str = "3dmodel.model", content: str = "") -> None:
        """Create a 3D model file in this directory.
        
        Args:
            filename: Name of the model file (should end with .model)
            content: XML content of the model file
        """
        if not filename.endswith('.model'):
            raise ValueError("Model files should have a .model extension")
        self.create_file(filename, content)
    
    def list_model_files(self) -> List[str]:
        """List all .model files in this directory."""
        all_files = self.list_files()
        return [f for f in all_files if f.endswith('.model')]
    
    def add_thumbnail(self, filename: str, image_data: bytes) -> None:
        """Add a thumbnail image to the 3D directory.
        
        Args:
            filename: Name of the thumbnail file (should be .png or .jpg)
            image_data: Binary image data
        """
        allowed_extensions = ('.png', '.jpg', '.jpeg')
        if not any(filename.lower().endswith(ext) for ext in allowed_extensions):
            raise ValueError(f"Thumbnail must be one of: {allowed_extensions}")
        self.create_file(filename, image_data)


class Metadata(Directory):
    """Specialized directory class for the Metadata directory in 3MF archives.
    
    The Metadata directory is optional and contains:
    - Custom metadata files
    - Conversion information
    - Properties and additional data
    """
    
    def __init__(self, create: bool = True):
        """Initialize the Metadata directory.
        
        Args:
            create: Whether to create the directory if it doesn't exist (default: True)
        """
        super().__init__("Metadata", create=create)
    
    def add_conversion_info(self, source_file: str, converter: str = "noah123d", 
                        objects_count: int = 0, additional_info: Dict[str, Any] = None) -> None:
        """Add conversion information metadata.
        
        Args:
            source_file: Name of the original source file
            converter: Name of the converter used
            objects_count: Number of objects in the converted file
            additional_info: Additional conversion information
        """
        info_lines = [
            f"Source File: {source_file}",
            f"Converter: {converter}",
            f"Objects Count: {objects_count}",
            f"Conversion Date: {Path.cwd()}"  # This will be replaced with actual date
        ]
        
        if additional_info:
            info_lines.append("\nAdditional Information:")
            for key, value in additional_info.items():
                info_lines.append(f"{key}: {value}")
        
        content = "\n".join(info_lines)
        self.create_file("conversion_info.txt", content)
    
    def add_properties(self, properties: Dict[str, Any], filename: str = "properties.xml") -> None:
        """Add properties as XML metadata.
        
        Args:
            properties: Dictionary of properties to add
            filename: Name of the properties file
        """
        # Simple XML generation for properties
        xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<properties>']
        for key, value in properties.items():
            xml_lines.append(f'  <property name="{key}" value="{value}"/>')
        xml_lines.append('</properties>')
        
        content = "\n".join(xml_lines)
        self.create_file(filename, content)
    
    def add_custom_metadata(self, filename: str, content: Union[str, bytes], 
                            description: str = "") -> None:
        """Add custom metadata file.
        
        Args:
            filename: Name of the metadata file
            content: Content of the metadata file
            description: Optional description of the metadata
        """
        self.create_file(filename, content)
        
        # Also create a description file if description is provided
        if description:
            desc_filename = f"{Path(filename).stem}_description.txt"
            self.create_file(desc_filename, description)


class Textures(Directory):
    """Specialized directory class for the Textures directory in 3MF archives.
    
    The Textures directory is optional and contains:
    - Texture image files (.jpg, .png, etc.)
    - Material texture data
    - Surface patterns and colors
    """
    
    def __init__(self, create: bool = True):
        """Initialize the Textures directory.
        
        Args:
            create: Whether to create the directory if it doesn't exist (default: True)
        """
        super().__init__("Textures", create=create)
    
    def add_texture(self, filename: str, image_data: bytes, 
                    texture_type: str = "color") -> None:
        """Add a texture image to the directory.
        
        Args:
            filename: Name of the texture file
            image_data: Binary image data
            texture_type: Type of texture (color, normal, roughness, etc.)
        """
        allowed_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tga')
        if not any(filename.lower().endswith(ext) for ext in allowed_extensions):
            raise ValueError(f"Texture must be one of: {allowed_extensions}")
        
        self.create_file(filename, image_data)
        
        # Create metadata about the texture
        metadata_filename = f"{Path(filename).stem}_metadata.txt"
        metadata_content = f"Texture Type: {texture_type}\nFilename: {filename}"
        self.create_file(metadata_filename, metadata_content)
    
    def list_texture_files(self) -> List[str]:
        """List all texture image files in this directory."""
        all_files = self.list_files()
        texture_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tga')
        return [f for f in all_files if any(f.lower().endswith(ext) for ext in texture_extensions)]
    
    def get_texture_metadata(self, texture_filename: str) -> Optional[str]:
        """Get metadata for a specific texture file.
        
        Args:
            texture_filename: Name of the texture file
            
        Returns:
            Metadata content as string, or None if not found
        """
        metadata_filename = f"{Path(texture_filename).stem}_metadata.txt"
        metadata_data = self.read_file(metadata_filename)
        return metadata_data.decode('utf-8') if metadata_data else None


# Backward compatibility - re-export Directory for existing code
from .directory import Directory, current_directory


# Module-level convenience functions that work with the current directory context
def add_thumbnail(filename: str, image_data: bytes) -> None:
    """Add a thumbnail image to the current 3D directory.
    
    Must be called within a ThreeD context manager.
    
    Args:
        filename: Name of the thumbnail file (should be .png or .jpg)
        image_data: Binary image data
        
    Raises:
        RuntimeError: If not called within a ThreeD context
        TypeError: If current directory is not a ThreeD instance
        ValueError: If thumbnail format is invalid
    """
    current_dir = current_directory.get()
    if not current_dir:
        raise RuntimeError("add_thumbnail() must be called within a directory context manager")
    
    if not isinstance(current_dir, ThreeD):
        raise TypeError("add_thumbnail() can only be used within a ThreeD context")
    
    current_dir.add_thumbnail(filename, image_data)


def create_model_file(filename: str = "3dmodel.model", content: str = "") -> None:
    """Create a 3D model file in the current 3D directory.
    
    Must be called within a ThreeD context manager.
    
    Args:
        filename: Name of the model file (should end with .model)
        content: XML content of the model file
        
    Raises:
        RuntimeError: If not called within a ThreeD context
        TypeError: If current directory is not a ThreeD instance
        ValueError: If filename doesn't end with .model
    """
    current_dir = current_directory.get()
    if not current_dir:
        raise RuntimeError("create_model_file() must be called within a directory context manager")
    
    if not isinstance(current_dir, ThreeD):
        raise TypeError("create_model_file() can only be used within a ThreeD context")
    
    current_dir.create_model_file(filename, content)


def list_model_files() -> List[str]:
    """List all .model files in the current 3D directory.
    
    Must be called within a ThreeD context manager.
    
    Returns:
        List of model filenames
        
    Raises:
        RuntimeError: If not called within a ThreeD context
        TypeError: If current directory is not a ThreeD instance
    """
    current_dir = current_directory.get()
    if not current_dir:
        raise RuntimeError("list_model_files() must be called within a directory context manager")
    
    if not isinstance(current_dir, ThreeD):
        raise TypeError("list_model_files() can only be used within a ThreeD context")
    
    return current_dir.list_model_files()


def add_conversion_info(source_file: str, converter: str = "noah123d", 
                        objects_count: int = 0, additional_info: Dict[str, Any] = None) -> None:
    """Add conversion information metadata to the current Metadata directory.
    
    Must be called within a Metadata context manager.
    
    Args:
        source_file: Name of the original source file
        converter: Name of the converter used
        objects_count: Number of objects in the converted file
        additional_info: Additional conversion information
        
    Raises:
        RuntimeError: If not called within a Metadata context
        TypeError: If current directory is not a Metadata instance
    """
    current_dir = current_directory.get()
    if not current_dir:
        raise RuntimeError("add_conversion_info() must be called within a directory context manager")
    
    if not isinstance(current_dir, Metadata):
        raise TypeError("add_conversion_info() can only be used within a Metadata context")
    
    current_dir.add_conversion_info(source_file, converter, objects_count, additional_info)


def add_properties(properties: Dict[str, Any], filename: str = "properties.xml") -> None:
    """Add properties as XML metadata to the current Metadata directory.
    
    Must be called within a Metadata context manager.
    
    Args:
        properties: Dictionary of properties to add
        filename: Name of the properties file
        
    Raises:
        RuntimeError: If not called within a Metadata context
        TypeError: If current directory is not a Metadata instance
    """
    current_dir = current_directory.get()
    if not current_dir:
        raise RuntimeError("add_properties() must be called within a directory context manager")
    
    if not isinstance(current_dir, Metadata):
        raise TypeError("add_properties() can only be used within a Metadata context")
    
    current_dir.add_properties(properties, filename)


def add_custom_metadata(filename: str, content: Union[str, bytes], 
                        description: str = "") -> None:
    """Add custom metadata file to the current Metadata directory.
    
    Must be called within a Metadata context manager.
    
    Args:
        filename: Name of the metadata file
        content: Content of the metadata file
        description: Optional description of the metadata
        
    Raises:
        RuntimeError: If not called within a Metadata context
        TypeError: If current directory is not a Metadata instance
    """
    current_dir = current_directory.get()
    if not current_dir:
        raise RuntimeError("add_custom_metadata() must be called within a directory context manager")
    
    if not isinstance(current_dir, Metadata):
        raise TypeError("add_custom_metadata() can only be used within a Metadata context")
    
    current_dir.add_custom_metadata(filename, content, description)


def add_texture(filename: str, image_data: bytes, texture_type: str = "color") -> None:
    """Add a texture image to the current Textures directory.
    
    Must be called within a Textures context manager.
    
    Args:
        filename: Name of the texture file
        image_data: Binary image data
        texture_type: Type of texture (color, normal, roughness, etc.)
        
    Raises:
        RuntimeError: If not called within a Textures context
        TypeError: If current directory is not a Textures instance
        ValueError: If texture format is invalid
    """
    current_dir = current_directory.get()
    if not current_dir:
        raise RuntimeError("add_texture() must be called within a directory context manager")
    
    if not isinstance(current_dir, Textures):
        raise TypeError("add_texture() can only be used within a Textures context")
    
    current_dir.add_texture(filename, image_data, texture_type)


def list_texture_files() -> List[str]:
    """List all texture image files in the current Textures directory.
    
    Must be called within a Textures context manager.
    
    Returns:
        List of texture filenames
        
    Raises:
        RuntimeError: If not called within a Textures context
        TypeError: If current directory is not a Textures instance
    """
    current_dir = current_directory.get()
    if not current_dir:
        raise RuntimeError("list_texture_files() must be called within a directory context manager")
    
    if not isinstance(current_dir, Textures):
        raise TypeError("list_texture_files() can only be used within a Textures context")
    
    return current_dir.list_texture_files()


def get_texture_metadata(texture_filename: str) -> Optional[str]:
    """Get metadata for a specific texture file in the current Textures directory.
    
    Must be called within a Textures context manager.
    
    Args:
        texture_filename: Name of the texture file
        
    Returns:
        Metadata content as string, or None if not found
        
    Raises:
        RuntimeError: If not called within a Textures context
        TypeError: If current directory is not a Textures instance
    """
    current_dir = current_directory.get()
    if not current_dir:
        raise RuntimeError("get_texture_metadata() must be called within a directory context manager")
    
    if not isinstance(current_dir, Textures):
        raise TypeError("get_texture_metadata() can only be used within a Textures context")
    
    return current_dir.get_texture_metadata(texture_filename)


# Generic directory functions that work with any directory type
def create_file(filename: str, content: Union[str, bytes]) -> None:
    """Create a file in the current directory.
    
    Must be called within a directory context manager.
    
    Args:
        filename: Name of the file to create
        content: Content of the file (string or bytes)
        
    Raises:
        RuntimeError: If not called within a directory context
    """
    current_dir = current_directory.get()
    if not current_dir:
        raise RuntimeError("create_file() must be called within a directory context manager")
    
    current_dir.create_file(filename, content)


def read_file(filename: str) -> Optional[bytes]:
    """Read a file from the current directory.
    
    Must be called within a directory context manager.
    
    Args:
        filename: Name of the file to read
        
    Returns:
        File content as bytes, or None if not found
        
    Raises:
        RuntimeError: If not called within a directory context
    """
    current_dir = current_directory.get()
    if not current_dir:
        raise RuntimeError("read_file() must be called within a directory context manager")
    
    return current_dir.read_file(filename)


def delete_file(filename: str) -> bool:
    """Delete a file from the current directory.
    
    Must be called within a directory context manager.
    
    Args:
        filename: Name of the file to delete
        
    Returns:
        True if file was deleted, False if not found
        
    Raises:
        RuntimeError: If not called within a directory context
    """
    current_dir = current_directory.get()
    if not current_dir:
        raise RuntimeError("delete_file() must be called within a directory context manager")
    
    return current_dir.delete_file(filename)


def list_files() -> List[str]:
    """List files in the current directory.
    
    Must be called within a directory context manager.
    
    Returns:
        List of filenames
        
    Raises:
        RuntimeError: If not called within a directory context
    """
    current_dir = current_directory.get()
    if not current_dir:
        raise RuntimeError("list_files() must be called within a directory context manager")
    
    return current_dir.list_files()


def list_subdirectories() -> List[str]:
    """List subdirectories in the current directory.
    
    Must be called within a directory context manager.
    
    Returns:
        List of subdirectory names
        
    Raises:
        RuntimeError: If not called within a directory context
    """
    current_dir = current_directory.get()
    if not current_dir:
        raise RuntimeError("list_subdirectories() must be called within a directory context manager")
    
    return current_dir.list_subdirectories()


__all__ = [
    'Directory', 'ThreeD', 'Metadata', 'Textures',
    # ThreeD functions
    'add_thumbnail', 'create_model_file', 'list_model_files',
    # Metadata functions  
    'add_conversion_info', 'add_properties', 'add_custom_metadata',
    # Textures functions
    'add_texture', 'list_texture_files', 'get_texture_metadata',
    # Generic directory functions
    'create_file', 'read_file', 'delete_file', 'list_files', 'list_subdirectories'
]
