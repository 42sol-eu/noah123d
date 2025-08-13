# -*- coding: utf-8 -*-
"""
Console visualization utilities for noah123d using rich.
----
file:
    name:       console.py
    uuid:       <to-be-generated>
description:    Console visualization utilities for noah123d using rich
authors:         felix@42sol.eu
project:
    name:       noah123d
    uuid:       93fe70d7-2d29-4ebf-bf0e-51d75dbfda30
    url:        https://github.com/42sol-eu/noah123d
"""

# %% [External imports]
from rich.console import (
    Console as RichConsole,
)  #!md| [docs](https://rich.readthedocs.io/en/stable/console.html)
from rich.table import (
    Table,
)  #!md| [docs](https://rich.readthedocs.io/en/stable/tables.html)
from pathlib import (
    Path
)  #!md| [docs](https://docs.python.org/3/library/pathlib.html)
from contextvars import ContextVar
from typing import Optional

# %% [Local imports]
# Note: Context variables imported lazily to avoid circular imports


# %% [Classes]
class Console:
    """Console visualization utilities for noah123d using rich."""
    
    def __init__(self):
        """Initialize the Console with a rich console instance."""
        self.console = RichConsole()
    
    def print_file_not_found(self, file_path: str):
        """Print a file not found error using rich console."""
        self.console.print(f"[red]❌ File not found: {file_path}[/red]")

    def print_file_info(self, file_path: str):
        """Print file info (name, size) using rich console."""
        path = Path(file_path)
        self.console.print(f"[bold blue]🔍 Analyzing 3MF Assembly: {file_path}[/bold blue]")
        self.console.print(f"📁 File size: {path.stat().st_size / (1024*1024):.2f} MB")

    def print_archive_contents(self, contents: list):
        """Print the contents of an archive using rich console."""
        self.console.print(f"\n📦 Archive contains {len(contents)} files:")
        for content in sorted(contents):
            self.console.print(f"   📄 {content}")

    def print_metadata_files(self, metadata_files: list):
        """Print metadata file info using rich console."""
        if metadata_files:
            self.console.print(f"\n📋 Metadata files found: {len(metadata_files)}")

    def print_model_analysis(self, object_count: int):
        """Print model analysis header using rich console."""
        self.console.print(f"\n🎯 Model Analysis:")
        self.console.print(f"   Total Objects: {object_count}")

    def print_object_table(self, object_details: list, title: str = "Objects"):
        """Print a table of object details using rich console.
        
        Args:
            object_details: list of dicts where keys become column headers
            title: Title for the table
        """
        if not object_details:
            self.console.print("[yellow]No objects to display[/yellow]")
            return
            
        # Get all unique keys from all objects to handle missing keys
        all_keys = set()
        for obj in object_details:
            all_keys.update(obj.keys())
        
        # Sort keys for consistent column order, with common keys first
        priority_keys = ['id', 'object_id', 'name', 'type']
        sorted_keys = []
        
        # Add priority keys first if they exist
        for key in priority_keys:
            if key in all_keys:
                sorted_keys.append(key)
                all_keys.remove(key)
        
        # Add remaining keys alphabetically
        sorted_keys.extend(sorted(all_keys))
        
        # Create table
        table = Table(title=title)
        
        # Add columns with appropriate styling
        for key in sorted_keys:
            style = self._get_column_style(key)
            # Format header: capitalize and replace underscores with spaces
            header = key.replace('_', ' ').title()
            table.add_column(header, style=style)
        
        # Add rows
        for obj in object_details:
            row = []
            for key in sorted_keys:
                value = obj.get(key, "N/A")
                # Format numbers with commas for readability
                if isinstance(value, (int, float)) and key in ['vertices', 'triangles', 'vertex_count', 'triangle_count']:
                    row.append(f"{value:,}")
                else:
                    row.append(str(value))
            table.add_row(*row)
        
        self.console.print(table)
    
    def _get_column_style(self, key: str) -> str:
        """Get appropriate style for a column based on its key."""
        key_lower = key.lower()
        if 'id' in key_lower:
            return "cyan"
        elif any(word in key_lower for word in ['vertices', 'vertex']):
            return "green"
        elif any(word in key_lower for word in ['triangles', 'triangle']):
            return "yellow"
        elif any(word in key_lower for word in ['count', 'number', 'size']):
            return "blue"
        elif any(word in key_lower for word in ['type', 'kind', 'category']):
            return "magenta"
        elif any(word in key_lower for word in ['name', 'title']):
            return "white"
        else:
            return "dim"

    def print_assembly_totals(
        self,
        reported_count: int,
        actual_count: int,
        total_vertices: int,
        total_triangles: int,
    ):
        """Print assembly totals using rich console."""
        self.console.print(f"\n📊 Assembly Totals:")
        self.console.print(f"   Reported Object Count: {reported_count}")
        self.console.print(f"   Actual Objects Found: {actual_count}")
        self.console.print(f"   Total Vertices: {total_vertices:,}")
        self.console.print(f"   Total Triangles: {total_triangles:,}")

    def print_error(self, error: Exception):
        """Print an error message using rich console."""
        self.console.print(f"[red]❌ Error: {error}[/red]")

    def print_model_content_analysis(self, objects: list, object_count: int = None):
        """Print detailed model content analysis using rich console.
        
        Args:
            objects: List of model objects with their data
            object_count: Total object count (if different from len(objects))
        """
        if object_count is None:
            object_count = len(objects)
            
        self.console.print(f"\n🎯 Model Analysis:")
        self.console.print(f"   Total Objects: {object_count}")
        
        if objects:
            # Prepare object details for the flexible table
            object_details = []
            total_vertices = 0
            total_triangles = 0
            
            for obj in objects:
                vertices = len(obj.get('vertices', []))
                triangles = len(obj.get('triangles', []))
                total_vertices += vertices
                total_triangles += triangles
                
                # Calculate basic volume info
                volume_info = "3D Model"
                if triangles > 0:
                    if triangles < 100:
                        volume_info = "Low-poly"
                    elif triangles < 1000:
                        volume_info = "Medium-poly"
                    else:
                        volume_info = "High-poly"
                
                object_details.append({
                    'id': obj.get('id', 'N/A'),
                    'type': obj.get('type', 'model'),
                    'vertices': vertices,
                    'triangles': triangles,
                    'volume_info': volume_info
                })
            
            # Use the flexible table method
            self.print_object_table(object_details, "3D Objects Details")
            
            # Print totals
            self.console.print(f"\n📊 Total Statistics:")
            self.console.print(f"   Combined Vertices: {total_vertices:,}")
            self.console.print(f"   Combined Triangles: {total_triangles:,}")

    def print_stl_loading_info(self, stl_path: Path, obj_id: int, vertex_count: int, triangle_count: int):
        """Print information about STL loading process."""
        self.console.print(f"📁 Loading STL file: {stl_path.name}")
        self.console.print(f"✓ Added STL as object ID: {obj_id}")
        self.console.print(f"📊 Object details:")
        self.console.print(f"   - Vertices: {vertex_count:,}")
        self.console.print(f"   - Triangles: {triangle_count:,}")

    def print_start(self, task: str, details: dict):
        """Print conversion start information."""
        
        summary = details.get('summary', 'starting')
        self.console.print(f"[green]🚀 {task} {summary}...[/green]")
        
        for key, value in details.items():
            if key.find('- ') == 0:
                key = key.replace('- ', '', 1)
                self.console.print(f"- {key.capitalize()}:  {value}")
        
    def print_success(self, task: str):
        """Print conversion success message."""
        self.console.print(f"[bold green]✅ {task} completed successfully![/bold green]")

    def print_archive_created(self, archive_path: Path):
        """Print archive creation confirmation."""
        self.console.print(f"✓ Created 3MF archive: {archive_path}")

    def print_directory_created(self, directory_name: str):
        """Print directory creation confirmation."""
        self.console.print(f"✓ Created {directory_name} directory")

    def print_metadata_added(self):
        """Print metadata addition confirmation."""
        self.console.print(f"✓ Added conversion metadata")

    def print_analyzing_file(self, file_path: Path):
        """Print file analysis header."""
        self.console.print(f"\n[blue]📋 Analyzing 3MF file: {file_path.name}[/blue]")

    def print_batch_conversion_start(self, file_count: int):
        """Print batch conversion start message."""
        self.console.print(f"[blue]🔄 Batch converting {file_count} STL files...[/blue]")

    def print_batch_conversion_complete(self, converted_count: int, output_dir: Path):
        """Print batch conversion completion message."""
        self.console.print(f"\n[bold green]🎉 Batch conversion completed![/bold green]")
        self.console.print(f"Successfully converted {converted_count} files to {output_dir}")

    def print_processing_file(self, file_name: str):
        """Print file processing message."""
        self.console.print(f"\n📂 Processing: {file_name}")

    def print_conversion_failed(self, file_name: str, error: Exception):
        """Print conversion failure message."""
        self.console.print(f"[red]❌ Failed to convert {file_name}: {error}[/red]")

    def print_converted_file(self, output_file_name: str):
        """Print successful conversion message."""
        self.console.print(f"✅ Converted: {output_file_name}")

    def print_no_stl_files_found(self, input_dir: Path):
        """Print message when no STL files are found."""
        self.console.print(f"[yellow]No STL files found in: {input_dir}[/yellow]")

    def print_error(self, message: str):
        """Print error message with red formatting."""
        self.console.print(f"[red]{message}[/red]")

    def print_archive_contents(self, contents: list):
        """Print archive contents list."""
        self.console.print(f"\n📦 Archive Contents ({len(contents)} files):")
        for content in sorted(contents):
            self.console.print(f"   📄 {content}")

    def print_content(self, data, context_hint: str = None):
        """Context-aware content printer that adapts based on current context managers.
        
        Args:
            data: The data to print - can be list, dict, or other types
            context_hint: Optional hint to override context detection
        """
        
        # Get current context from context variables
        detected_context = self._detect_current_context()
        
        # Use explicit hint if provided, otherwise use detected context
        effective_context = context_hint or detected_context
        
        self.console.print(f'# {effective_context}')

        if not data:
            self.console.print("[dim]No content to display[/dim]")
            return
        
        # Handle different data types
        if isinstance(data, list):
            self._print_list_content(data, effective_context)
        elif isinstance(data, dict):
            self._print_dict_content(data, effective_context)
        else:
            # Fallback for other types
            self.console.print(f"Content: {data}")
    
    def _detect_current_context(self) -> str:
        """Detect the current context from context variables using lazy imports."""
        try:
            # Lazy import to avoid circular imports
            from ..threemf.archive import current_archive
            from ..threemf.directory import current_directory  
            from ..threemf.model import current_model
            
            # Check context variables in order of specificity
            model = current_model.get()
            directory = current_directory.get()
            archive = current_archive.get()
            
            if model is not None:
                return 'model'
            elif directory is not None:
                # Check for specialized directory types first by class name
                directory_class = directory.__class__.__name__
                if directory_class == 'Metadata':
                    return 'metadata'
                elif directory_class == 'Textures':
                    return 'textures'
                elif directory_class == 'ThreeD':
                    return 'objects'
                
                # Fallback to name-based detection for basic Directory class
                if hasattr(directory, 'name'):
                    dir_name = directory.name.lower()
                    if 'metadata' in dir_name:
                        return 'metadata'
                    elif 'texture' in dir_name:
                        return 'textures'  
                    elif '3d' in dir_name:
                        return 'objects'
                        
                return 'directory'
            elif archive is not None:
                return 'archive'
            else:
                return 'general'
        except ImportError:
            # Fallback if context variables can't be imported
            return 'general'
    
    def _print_list_content(self, data: list, context: str = None):
        """Print list content based on detected or provided context."""
        if not data:
            return
        
        # Analyze the first few items to determine content type
        sample_items = data[:3] if len(data) > 3 else data
        
        # Handle based on context
        if context == 'archive':
            # Archive contents format
            self.console.print(f"\n📦 Archive Contents ({len(data)} files):")
            for item in sorted(data):
                self.console.print(f"   📄 {item}")
                
        elif context == 'metadata' or context == 'directory' and self._looks_like_metadata(data):
            # Metadata files format
            if data:
                self.console.print(f"\n📋 Metadata files found: {len(data)}")
                for item in sorted(data):
                    self.console.print(f"   📄 {item}")
            else:
                self.console.print("\n📋 No metadata files found")
                
        elif context == 'textures' or context == 'directory' and self._looks_like_textures(data):
            # Texture files format
            if data:
                self.console.print(f"\n🎨 Texture files found: {len(data)}")
                for item in sorted(data):
                    self.console.print(f"   🖼️  {item}")
            else:
                self.console.print("\n🎨 No texture files found")
                
        elif context in ['model', 'objects'] and all(isinstance(item, dict) for item in sample_items):
            # Object details table format - only if items are actually dicts
            title = self._get_table_title(sample_items, context)
            self.print_object_table(data, title)
            
        elif context == 'objects' and all(isinstance(item, str) for item in sample_items):
            # 3D directory file listing
            self.console.print(f"\n🔺 3D Directory files ({len(data)} items):")
            for item in sorted(data):
                self.console.print(f"   📄 {item}")
                
        elif all(isinstance(item, dict) for item in sample_items):
            # Object details table format for dicts without specific context
            title = self._get_table_title(sample_items, context)
            self.print_object_table(data, title)
            
        elif all(isinstance(item, str) and ('/' in item or '.' in item) for item in sample_items):
            # File paths - default to archive format unless context suggests otherwise
            self.console.print(f"\n� Files ({len(data)} items):")
            for item in sorted(data):
                self.console.print(f"   📄 {item}")
        
        else:
            # Handle list of simple values
            title = f"Content ({len(data)} items)"
            if context and context != 'general':
                title = f"{context.title()} ({len(data)} items)"
            
            self.console.print(f"\n{title}:")
            for item in data:
                self.console.print(f"   • {item}")
    
    def _looks_like_metadata(self, data: list) -> bool:
        """Check if a list of items looks like metadata files."""
        if not data:
            return False
        # Check if most items contain 'metadata' in their path
        metadata_count = sum(1 for item in data if isinstance(item, str) and 'metadata' in item.lower())
        return metadata_count > len(data) / 2
    
    def _looks_like_textures(self, data: list) -> bool:
        """Check if a list of items looks like texture files."""
        if not data:
            return False
        # Check if most items are image files or contain 'texture' in their path
        texture_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tga')
        texture_count = sum(1 for item in data if isinstance(item, str) and 
                          (any(item.lower().endswith(ext) for ext in texture_extensions) or
                           'texture' in item.lower()))
        return texture_count > len(data) / 2
    
    def _print_dict_content(self, data: dict, context: str = None):
        """Print dictionary content based on context."""
        title = "Content"
        if context and context != 'general':
            title = context.title()
        
        self.console.print(f"\n📋 {title}:")
        for key, value in data.items():
            if isinstance(value, (list, dict)):
                self.console.print(f"   {key}: {type(value).__name__} with {len(value)} items")
            else:
                self.console.print(f"   {key}: {value}")
    
    def _get_table_title(self, sample_items: list, context: str = None) -> str:
        """Determine appropriate table title based on context and data content."""
        if context == 'model':
            return "Model Objects"
        elif context == 'objects':
            return "3D Objects"
        elif context == 'textures':
            return "Texture Details"
        elif context == 'metadata':
            return "Metadata Details"
        elif context and context != 'general':
            return f"{context.title()} Details"
        
        # Analyze keys to guess content type when no context
        if not sample_items:
            return "Content Details"
            
        all_keys = set()
        for item in sample_items:
            if isinstance(item, dict):
                all_keys.update(item.keys())
        
        if 'vertices' in all_keys and 'triangles' in all_keys:
            return "3D Objects Details"
        elif 'id' in all_keys:
            return "Objects"
        else:
            return "Content Details"


# %% [Functions] - Backwards compatibility functions
def print_file_not_found(console: RichConsole, file_path: str):
    """Print a file not found error using rich console."""
    console.print(f"[red]❌ File not found: {file_path}[/red]")


def print_file_info(console: RichConsole, file_path: str):
    """Print file info (name, size) using rich console."""
    path = Path(file_path)
    console.print(f"[bold blue]🔍 Analyzing 3MF Assembly: {file_path}[/bold blue]")
    console.print(f"📁 File size: {path.stat().st_size / (1024*1024):.2f} MB")


def print_archive_contents(console: RichConsole, contents: list):
    """Print the contents of an archive using rich console."""
    console.print(f"\n📦 Archive contains {len(contents)} files:")
    for content in sorted(contents):
        console.print(f"   📄 {content}")


def print_metadata_files(console: RichConsole, metadata_files: list):
    """Print metadata file info using rich console."""
    if metadata_files:
        console.print(f"\n📋 Metadata files found: {len(metadata_files)}")


def print_model_analysis(console: RichConsole, object_count: int):
    """Print model analysis header using rich console."""
    console.print(f"\n🎯 Model Analysis:")
    console.print(f"   Total Objects: {object_count}")


def print_object_table(console: RichConsole, object_details: list):
    """Print a table of 3D object details using rich console.
    object_details: list of dicts with keys 'id', 'vertices', 'triangles'
    """
    # For backward compatibility, use the old hardcoded approach
    table = Table(title="3D Objects in Assembly")
    table.add_column("Object ID", style="cyan")
    table.add_column("Vertices", style="green")
    table.add_column("Triangles", style="yellow")
    for obj in object_details:
        table.add_row(str(obj["id"]), f"{obj['vertices']:,}", f"{obj['triangles']:,}")
    console.print(table)


def print_assembly_totals(
    console: RichConsole,
    reported_count: int,
    actual_count: int,
    total_vertices: int,
    total_triangles: int,
):
    """Print assembly totals using rich console."""
    console.print(f"\n📊 Assembly Totals:")
    console.print(f"   Reported Object Count: {reported_count}")
    console.print(f"   Actual Objects Found: {actual_count}")
    console.print(f"   Total Vertices: {total_vertices:,}")
    console.print(f"   Total Triangles: {total_triangles:,}")


def print_error(console: RichConsole, error: Exception):
    """Print an error message using rich console."""
    console.print(f"[red]❌ Error: {error}[/red]")

if __name__ == "__main__":
    console = Console()
    console.print("please use this file from the `noah123d` package!")