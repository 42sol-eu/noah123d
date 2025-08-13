"""Directory class for managing directories inside a 3MF Archive."""

import os
from pathlib import Path
from typing import Optional, List, Union
from contextvars import ContextVar
from ..core.context_decorators import context_function
from .archive import Archive, current_archive

# Context variable to track the current directory
current_directory: ContextVar[Optional['Directory']] = ContextVar('current_directory', default=None)


class Directory:
    """Manages directories inside a 3MF Archive."""
    
    def __init__(self, path: Union[str, Path], create: bool = True):
        """
        Initialize the Directory.
        
        Args:
            path: Directory path within the archive
            create: Whether to create the directory if it doesn't exist
        """
        self.path = Path(path)
        self.create = create
        self._context_token = None
        self._parent_archive: Optional[Archive] = None
        
    def __enter__(self) -> 'Directory':
        """Enter the context manager."""
        # Set this directory as the current directory in context
        self._context_token = current_directory.set(self)
        
        # Get the parent archive from context
        self._parent_archive = current_archive.get()
        if not self._parent_archive:
            raise RuntimeError("Directory must be used within an Archive context")
            
        # Create directory in the temporary location if needed
        if self.create:
            self._ensure_directory_exists()
            
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager."""
        # Reset the context variable
        if self._context_token:
            current_directory.reset(self._context_token)
            
    @classmethod
    def get_current(cls) -> Optional['Directory']:
        """Get the current directory from context."""
        return current_directory.get()
        
    @classmethod
    def get_parent_archive(cls) -> Optional[Archive]:
        """Get the parent archive from context."""
        return current_archive.get()

    def _ensure_directory_exists(self):
        """Ensure the directory exists in the archive's temporary location."""
        if not self._parent_archive:
            return
            
        temp_path = self._parent_archive.get_temp_path()
        if temp_path:
            full_path = temp_path / self.path
            full_path.mkdir(parents=True, exist_ok=True)
                    
    def get_archive_path(self) -> str:
        """Get the path as it appears in the archive."""
        return str(self.path).replace('\\', '/')
        
    def exists(self) -> bool:
        """Check if this directory exists."""
        full_path = self.get_full_path()
        return full_path.exists() if full_path else False

    def get_full_path(self) -> Optional[Path]:
        """Get the full filesystem path to this directory."""
        if not self._parent_archive:
            return None
            
        temp_path = self._parent_archive.get_temp_path()
        if temp_path:
            return temp_path / self.path
        return None
        
    def create_subdirectory(self, name: str) -> 'Directory':
        """Create a subdirectory and return a Directory instance for it."""
        subdir_path = self.path / name
        return Directory(subdir_path, create=True)
        
    def list_subdirectories(self) -> List[str]:
        """List subdirectories in this directory."""
        full_path = self.get_full_path()
        if full_path and full_path.exists():
            return [d.name for d in full_path.iterdir() if d.is_dir()]
        return []

    def list_files(self) -> List[str]:
        """List files in this directory."""
        full_path = self.get_full_path()
        if full_path and full_path.exists():
            return [f.name for f in full_path.iterdir() if f.is_file()]
        return []
        
    def create_file(self, filename: str, content: Union[str, bytes]):
        """Create a file in this directory."""
        full_path = self.get_full_path()
        if full_path:
            # Ensure the directory exists before creating the file
            full_path.mkdir(parents=True, exist_ok=True)
            file_path = full_path / filename
            if isinstance(content, str):
                file_path.write_text(content, encoding='utf-8')
            else:
                file_path.write_bytes(content)
                
    def read_file(self, filename: str) -> Optional[bytes]:
        """Read a file from this directory."""
        full_path = self.get_full_path()
        if full_path:
            file_path = full_path / filename
            if file_path.exists():
                return file_path.read_bytes()
        return None
        
    def delete_file(self, filename: str) -> bool:
        """Delete a file from this directory."""
        full_path = self.get_full_path()
        if full_path:
            file_path = full_path / filename
            if file_path.exists():
                file_path.unlink()
                return True
        return False


# Generic directory functions (work with any directory type)
@context_function(current_directory)
def create_file(filename: str, content: Union[str, bytes]) -> None:
    """Create a file in the current directory.
    
    Must be called within a directory context manager.
    """
    pass  # Implementation handled by decorator


@context_function(current_directory)
def read_file(filename: str) -> Optional[bytes]:
    """Read a file from the current directory.
    
    Must be called within a directory context manager.
    """
    pass  # Implementation handled by decorator


@context_function(current_directory)
def delete_file(filename: str) -> bool:
    """Delete a file from the current directory.
    
    Must be called within a directory context manager.
    """
    pass  # Implementation handled by decorator


@context_function(current_directory)
def list_files() -> List[str]:
    """List files in the current directory.
    
    Must be called within a directory context manager.
    """
    pass  # Implementation handled by decorator


@context_function(current_directory)
def list_subdirectories() -> List[str]:
    """List subdirectories in the current directory.
    
    Must be called within a directory context manager.
    """
    pass  # Implementation handled by decorator
