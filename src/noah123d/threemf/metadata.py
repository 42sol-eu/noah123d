"""Specialized directory classes for 3MF archives."""

from pathlib import Path
from typing import Union, Optional, List, Dict, Any
from .directory import Directory, current_directory
from ..core.context_decorators import context_function, context_function_with_check

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


# Metadata specific functions
@context_function_with_check(current_directory, Metadata, "Metadata")
def add_conversion_info(source_file: str, converter: str = "noah123d", 
                        aobjects_count: int = 0, additional_info: Dict[str, Any] = None) -> None:
    """Add conversion information metadata to the current Metadata directory.
    
    Must be called within a Metadata context manager.
    """
    pass  # Implementation handled by decorator


@context_function_with_check(current_directory, Metadata, "Metadata")
def add_properties(properties: Dict[str, Any], filename: str = "properties.xml") -> None:
    """Add properties as XML metadata to the current Metadata directory.
    
    Must be called within a Metadata context manager.
    """
    pass  # Implementation handled by decorator


@context_function_with_check(current_directory, Metadata, "Metadata")
def add_custom_metadata(filename: str, content: Union[str, bytes], 
                        description: str = "") -> None:
    """Add custom metadata file to the current Metadata directory.
    
    Must be called within a Metadata context manager.
    """
    pass  # Implementation handled by decorator

