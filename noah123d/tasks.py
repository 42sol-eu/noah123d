from rich import print
from rich.console import Console
from pathlib import Path 

from . import Archive, Directory, Model

def create_empty_3mf(cls, output_path: Path) -> Optional[Path]:
    """
    Create an empty 3MF archive using the context system.
    
    Args:
        output_path: Path to the output 3MF file
        
    Returns:
        Path to the created 3MF file or None if creation failed
    """
    console = Console()
    console.print(f"[green]Creating empty 3MF archive...[/green]")
    console.print(f"Output: {output_path}")
    
    try:
        # Create the 3MF archive using the context system
        with Archive3mf(output_path, 'w') as archive:
            console.print(f"✓ Created 3MF archive: {archive.file_path}")
            
            # Create the 3D directory using the context system
            with Directory('3D') as models_dir:
                console.print(f"✓ Created 3D models directory")
                
                # Create an empty model within the directory context
                with cls() as model:
                    console.print(f"✓ Created empty model with {model.get_object_count()} objects")
                    
        console.print(f"[bold green]✅ Empty 3MF archive created successfully![/bold green]")
        return output_path
    except Exception as e:
        console.print(f"[red]❌ Failed to create 3MF archive: {e}[/red]")
        return None