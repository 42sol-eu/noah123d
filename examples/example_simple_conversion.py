"""Example usage of STL to 3MF converter using the noah123d library with context-aware methods."""

from pathlib import Path
from rich import print
from rich.console import Console
from noah123d import Archive, Directory, Model


def demo_context_aware_conversion():
    """Demo using instance methods within proper context."""
    console = Console()
    console.print("\n[yellow]Demo: Context-aware conversion (instance methods)[/yellow]")
    
    stl_path = Path("_models/multiverse/tile_2x2_borde.stl")
    output_path = Path("context_aware_tile.3mf")
    
    if not stl_path.exists():
        console.print(f"[red]STL file not found: {stl_path}[/red]")
        return None
    
    console.print(f"[green]Converting using context-aware methods...[/green]")
    
    # Use the context system properly - Archive -> Directory -> Model
    with Archive(output_path, 'w') as archive:
        console.print(f"✓ Created 3MF archive: {archive.file_path}")
        
        with Directory('3D') as models_dir:
            console.print(f"✓ Created 3D models directory")
            
            with Model() as model:
                # Use the new instance method
                obj_id = model.load_stl_with_info(stl_path)
                if obj_id:
                    # Add conversion metadata using instance method
                    model.add_conversion_metadata(stl_path)
                    console.print(f"✓ Added object with ID: {obj_id}")
    
    console.print(f"[bold green]✅ Context-aware conversion completed![/bold green]")
    return output_path


if __name__ == "__main__":
    console = Console()
    console.print("[bold blue]🚀 Noah123d STL to 3MF Converter Examples[/bold blue]")
    
    # Example 1: Convert using class method (self-contained)
    console.print("\n[yellow]Example 1: Class method conversion (self-contained)[/yellow]")
    stl_path = Path("_models/multiverse/tile_2x2_borde.stl")
    output_path = Path("converted_tile.3mf")
    
    if stl_path.exists():
        converted_file = Model.convert_stl_to_3mf(stl_path, output_path)
        if converted_file:
            Model.analyze_3mf_content(converted_file)
    else:
        console.print(f"[red]STL file not found: {stl_path}[/red]")
        console.print("[yellow]Please ensure the STL file exists or update the path[/yellow]")
    
    # Example 2: Context-aware conversion
    context_file = demo_context_aware_conversion()
    if context_file:
        Model.analyze_3mf_content(context_file)
    
    # Example 3: Batch conversion demo
    console.print("\n[yellow]Example 3: Batch conversion demo[/yellow]")
    input_dir = Path("_models")
    output_dir = Path("converted_models")
    
    if input_dir.exists():
        converted_files = Model.batch_convert_stl_files(input_dir, output_dir)
        console.print(f"[green]Converted {len(converted_files)} files successfully[/green]")
    else:
        console.print(f"[yellow]Models directory not found: {input_dir}[/yellow]")
        console.print("[yellow]Skipping batch conversion example[/yellow]")
    
    # Example 4: Create empty 3MF
    console.print("\n[yellow]Example 4: Create empty 3MF[/yellow]")
    with Archive('empty.3mf', 'w') as archive:
        with Directory('3D') as models_dir:
            with Model() as model:
                model.analyze_3mf_content()
    
    console.print(f"\n[bold green]🎯 STL Converter examples completed![/bold green]")
