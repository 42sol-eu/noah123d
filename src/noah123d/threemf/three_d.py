"""Specialized directory classes for 3MF archives."""

# %% [External imports]
from pathlib import Path
from typing import Union, Optional, List, Dict, Any

# %% [Local imports]
from .directory import Directory, current_directory, current_directory
from ..core.context_decorators import context_function, context_function_with_check


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

# Module-level convenience functions using decorators

# ThreeD specific functions
@context_function_with_check(current_directory, ThreeD, "ThreeD")
def add_thumbnail(filename: str, image_data: bytes) -> None:
    """Add a thumbnail image to the current 3D directory.
    
    Must be called within a ThreeD context manager.
    """
    pass  # Implementation handled by decorator


@context_function_with_check(current_directory, ThreeD, "ThreeD")  
def create_model_file(filename: str = "3dmodel.model", content: str = "") -> None:
    """Create a 3D model file in the current 3D directory.
    
    Must be called within a ThreeD context manager.
    """
    pass  # Implementation handled by decorator


@context_function_with_check(current_directory, ThreeD, "ThreeD")
def list_model_files() -> List[str]:
    """List all .model files in the current 3D directory.
    
    Must be called within a ThreeD context manager.
    """
    pass  # Implementation handled by decorator

