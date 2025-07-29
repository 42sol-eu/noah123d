"""Example usage of STL to 3MF converter using the noah123d library."""

from pathlib import Path
from rich import print
from rich.console import Console
from rich.table import Table
from noah123d import Archive3mf, Directory, Model


def convert_stl_to_3mf(stl_path: Path, output_path: Path):
    """
    Convert an STL file to a 3MF archive.
    
    Args:
        stl_path: Path to the input STL file
        output_path: Path to the output 3MF file
    """
    console = Console()
    
    if not stl_path.exists():
        console.print(f"[red]Error: STL file not found: {stl_path}[/red]")
        return None
        
    console.print(f"[green]Converting STL to 3MF...[/green]")
    console.print(f"Input:  {stl_path}")
    console.print(f"Output: {output_path}")
    
    # Create the 3MF archive
    with Archive3mf(output_path, 'w') as archive:
        console.print(f"✓ Created 3MF archive: {archive.file_path}")
        
        # Create the 3D directory
        with Directory('3D') as models_dir:
            console.print(f"✓ Created 3D models directory")
            
            # Create a model and add the STL
            with Model() as model:
                console.print(f"📁 Loading STL file: {stl_path.name}")
                
                # Add the STL object to the model
                obj_id = model.add_object_from_stl(stl_path)
                console.print(f"✓ Added STL as object ID: {obj_id}")
                
                # Get object info
                obj = model.get_object(obj_id)
                if obj:
                    vertex_count = len(obj['vertices'])
                    triangle_count = len(obj['triangles'])
                    console.print(f"📊 Object details:")
                    console.print(f"   - Vertices: {vertex_count:,}")
                    console.print(f"   - Triangles: {triangle_count:,}")
                
        # Create metadata directory with conversion info
        with Directory('Metadata') as metadata_dir:
            metadata_content = f"""STL to 3MF Conversion
Source STL: {stl_path.name}
Converted by: Noah123D STL Converter
Objects: {model.get_object_count()}
"""
            metadata_dir.create_file('conversion_info.txt', metadata_content)
            console.print(f"✓ Added conversion metadata")
            
    console.print(f"[bold green]✅ Conversion completed successfully![/bold green]")
    return output_path


def analyze_3mf_content(file_path: Path):
    """
    Analyze and display detailed information about a 3MF file.
    
    Args:
        file_path: Path to the 3MF file to analyze
    """
    console = Console()
    
    if not file_path.exists():
        console.print(f"[red]Error: 3MF file not found: {file_path}[/red]")
        return
        
    console.print(f"\n[blue]📋 Analyzing 3MF file: {file_path.name}[/blue]")
    
    with Archive3mf(file_path, 'r') as archive:
        # Show archive contents
        contents = archive.list_contents()
        console.print(f"\n📦 Archive Contents ({len(contents)} files):")
        for content in sorted(contents):
            console.print(f"   📄 {content}")
            
        # Read the model details
        with Directory('3D') as models_dir:
            with Model() as model:
                object_count = model.get_object_count()
                console.print(f"\n🎯 Model Analysis:")
                console.print(f"   Total Objects: {object_count}")
                
                if object_count > 0:
                    # Create a table for object details
                    table = Table(title="3D Objects Details")
                    table.add_column("Object ID", style="cyan")
                    table.add_column("Type", style="magenta")
                    table.add_column("Vertices", style="green")
                    table.add_column("Triangles", style="yellow")
                    table.add_column("Volume Info", style="blue")
                    
                    total_vertices = 0
                    total_triangles = 0
                    
                    for obj_id in model.list_objects():
                        obj = model.get_object(obj_id)
                        if obj:
                            vertices = len(obj['vertices'])
                            triangles = len(obj['triangles'])
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
                            
                            table.add_row(
                                str(obj_id),
                                obj.get('type', 'model'),
                                f"{vertices:,}",
                                f"{triangles:,}",
                                volume_info
                            )
                    
                    console.print(table)
                    console.print(f"\n📊 Total Statistics:")
                    console.print(f"   Combined Vertices: {total_vertices:,}")
                    console.print(f"   Combined Triangles: {total_triangles:,}")


def batch_convert_stl_files(input_dir: Path, output_dir: Path):
    """
    Convert all STL files in a directory to 3MF format.
    
    Args:
        input_dir: Directory containing STL files
        output_dir: Directory to save 3MF files
    """
    console = Console()
    
    if not input_dir.exists():
        console.print(f"[red]Error: Input directory not found: {input_dir}[/red]")
        return
        
    # Find all STL files
    stl_files = list(input_dir.glob("**/*.stl"))
    
    if not stl_files:
        console.print(f"[yellow]No STL files found in: {input_dir}[/yellow]")
        return
        
    console.print(f"[blue]🔄 Batch converting {len(stl_files)} STL files...[/blue]")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    converted_files = []
    
    for stl_file in stl_files:
        # Create output filename
        output_file = output_dir / f"{stl_file.stem}.3mf"
        
        console.print(f"\n📂 Processing: {stl_file.name}")
        
        try:
            result = convert_stl_to_3mf(stl_file, output_file)
            if result:
                converted_files.append(result)
                console.print(f"✅ Converted: {output_file.name}")
        except Exception as e:
            console.print(f"[red]❌ Failed to convert {stl_file.name}: {e}[/red]")
    
    console.print(f"\n[bold green]🎉 Batch conversion completed![/bold green]")
    console.print(f"Successfully converted {len(converted_files)} files to {output_dir}")


if __name__ == "__main__":
    console = Console()
    console.print("[bold blue]🚀 Noah123D STL to 3MF Converter Examples[/bold blue]")
    
    # Example 1: Convert a single STL file
    console.print("\n[yellow]Example 1: Single STL conversion[/yellow]")
    stl_path = Path("_models/multiverse/tile_2x2_borde.stl")
    output_path = Path("converted_tile.3mf")
    
    if stl_path.exists():
        converted_file = convert_stl_to_3mf(stl_path, output_path)
        if converted_file:
            analyze_3mf_content(converted_file)
    else:
        console.print(f"[red]STL file not found: {stl_path}[/red]")
        console.print("[yellow]Please ensure the STL file exists or update the path[/yellow]")
    
    # Example 2: Batch conversion demo
    console.print("\n[yellow]Example 2: Batch conversion demo[/yellow]")
    input_dir = Path("_models")
    output_dir = Path("converted_models")
    
    if input_dir.exists():
        batch_convert_stl_files(input_dir, output_dir)
    else:
        console.print(f"[yellow]Models directory not found: {input_dir}[/yellow]")
        console.print("[yellow]Skipping batch conversion example[/yellow]")
    
    console.print(f"\n[bold green]🎯 STL Converter examples completed![/bold green]")
