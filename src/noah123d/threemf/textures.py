"""Specialized directory classes for 3MF archives."""

from pathlib import Path
from typing import Union, Optional, List, Dict, Any
from .directory import Directory, current_directory
from ..core.context_decorators import context_function, context_function_with_check

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

# Textures specific functions
@context_function_with_check(current_directory, Textures, "Textures")
def add_texture(filename: str, image_data: bytes, texture_type: str = "color") -> None:
    """Add a texture image to the current Textures directory.
    
    Must be called within a Textures context manager.
    """
    pass  # Implementation handled by decorator


@context_function_with_check(current_directory, Textures, "Textures")
def list_texture_files() -> List[str]:
    """List all texture image files in the current Textures directory.
    
    Must be called within a Textures context manager.
    """
    pass  # Implementation handled by decorator


@context_function_with_check(current_directory, Textures, "Textures")
def get_texture_metadata(texture_filename: str) -> Optional[str]:
    """Get metadata for a specific texture file in the current Textures directory.
    
    Must be called within a Textures context manager.
    """
    pass  # Implementation handled by decorator
