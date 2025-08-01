"""Archive3mf class for managing 3MF zip archives."""

import zipfile
import tempfile
import os
from pathlib import Path
from typing import Optional, Union
from contextvars import ContextVar
import contextlib
from rich import print 
from rich.console import Console

from .xml_3mf import content_types_header, relationships_header

# Context variable to track the current archive
current_archive: ContextVar[Optional['Archive3mf']] = ContextVar('current_archive', default=None)


class Archive3mf:
    """Manages a 3MF zip archive using Python's standard library."""
    
    def __init__(self, file_path: Union[str, Path], mode: str = 'r'):
        """
        Initialize the Archive3mf.
        
        Args:
            file_path: Path to the 3MF file
            mode: File mode ('r', 'w', 'a')
        """
        self.file_path = Path(file_path)
        self.mode = mode
        self._zipfile: Optional[zipfile.ZipFile] = None
        self._temp_dir: Optional[tempfile.TemporaryDirectory] = None
        self._context_token = None
        
    def __enter__(self) -> 'Archive3mf':
        """Enter the context manager."""
        # Set this archive as the current archive in context
        self._context_token = current_archive.set(self)
        
        # Create temporary directory for all modes
        self._temp_dir = tempfile.TemporaryDirectory()
            
        # Open the zip file
        if self.mode == 'w' or not self.file_path.exists():
            self._zipfile = zipfile.ZipFile(self.file_path, 'w', zipfile.ZIP_DEFLATED)
            # Create basic 3MF structure
            self._create_basic_structure()
        else:
            self._zipfile = zipfile.ZipFile(self.file_path, self.mode)
            if self._temp_dir:
                self._zipfile.extractall(self._temp_dir.name)
                
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager."""
        # Close the zip file
        if self._zipfile:
            if self.mode in ('w', 'a') and self._temp_dir:
                # Re-pack the temporary directory if it was used
                self._repack_from_temp()
            self._zipfile.close()
            
        # Clean up temporary directory
        if self._temp_dir:
            self._temp_dir.cleanup()
            
        # Reset the context variable
        if self._context_token:
            current_archive.reset(self._context_token)
            
    @classmethod
    def get_current(cls) -> Optional['Archive3mf']:
        """Get the current archive from context."""
        return current_archive.get()

    def _create_basic_structure(self):
        """Create the basic 3MF file structure."""
        # Create [Content_Types].xml
        self._zipfile.writestr('[Content_Types].xml', content_types_header)
        
        # Create _rels/.rels
        self._zipfile.writestr('_rels/.rels', relationships_header)
        
    def _repack_from_temp(self):
        """Repack the archive from temporary directory."""
        if not self._temp_dir:
            return
            
        # Close current zipfile
        self._zipfile.close()
        
        # Create new zipfile
        self._zipfile = zipfile.ZipFile(self.file_path, 'w', zipfile.ZIP_DEFLATED)
        
        # Add all files from temp directory
        temp_path = Path(self._temp_dir.name)
        for file_path in temp_path.rglob('*'):
            if file_path.is_file():
                arc_name = file_path.relative_to(temp_path)
                self._zipfile.write(file_path, arc_name)
                
    def get_temp_path(self) -> Optional[Path]:
        """Get the temporary directory path for file operations."""
        return Path(self._temp_dir.name) if self._temp_dir else None
        
    def list_contents(self) -> list[str]:
        """List all files in the archive."""
        if self._zipfile:
            return self._zipfile.namelist()
        return []
        
    def extract_file(self, filename: str) -> Optional[bytes]:
        """Extract a specific file from the archive."""
        if self._zipfile and filename in self._zipfile.namelist():
            return self._zipfile.read(filename)
        return None
        
    def add_file(self, filename: str, data: Union[str, bytes]):
        """Add a file to the archive."""
        if self._zipfile:
            if isinstance(data, str):
                data = data.encode('utf-8')
            self._zipfile.writestr(filename, data)
    
    def is_writable(self) -> bool:
        """Check if the archive is opened in a writable mode."""
        return self.mode in ('w', 'a')


# Import decorator utilities
from .context_decorators import context_function

# Module-level convenience functions using decorators
@context_function(current_archive)
def list_contents() -> list[str]:
    """List all files in the current archive.
    
    Must be called within an Archive3mf context manager.
    """
    pass  # Implementation handled by decorator


@context_function(current_archive)
def extract_file(filename: str) -> Optional[bytes]:
    """Extract a specific file from the current archive.
    
    Must be called within an Archive3mf context manager.
    """
    pass  # Implementation handled by decorator


@context_function(current_archive)
def add_file(filename: str, data: Union[str, bytes]) -> None:
    """Add a file to the current archive.
    
    Must be called within an Archive3mf context manager.
    """
    pass  # Implementation handled by decorator


@context_function(current_archive)
def get_temp_path() -> Optional[Path]:
    """Get the temporary directory path for file operations from the current archive.
    
    Must be called within an Archive3mf context manager.
    """
    pass  # Implementation handled by decorator


@context_function(current_archive)
def is_writable() -> bool:
    """Check if the current archive is opened in a writable mode.
    
    Must be called within an Archive3mf context manager.
    """
    pass  # Implementation handled by decorator
