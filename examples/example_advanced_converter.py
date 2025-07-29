"""Advanced STL converter example using the noah123d.converters module."""

from pathlib import Path
from rich import print
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, TaskID
import time

# Import the new converter module
from noah123d import STLConverter, stl_to_3mf, get_stl_info, batch_stl_to_3mf


def demo_simple_conversion():
    """Demonstrate simple STL to 3MF conversion."""
    console = Console()
    console.print("\n[bold blue]🔄 Simple STL Conversion Demo[/bold blue]")
    
    stl_file = Path("_models/multiverse/tile_2x2_borde.stl")
    output_file = Path("simple_converted.3mf")
    
    if not stl_file.exists():
        console.print(f"[red]STL file not found: {stl_file}[/red]")
        return
    
    # Simple one-line conversion
    success = stl_to_3mf(stl_file, output_file)
    
    if success:
        console.print(f"[green]✅ Successfully converted {stl_file.name} to {output_file.name}[/green]")
        console.print(f"Output size: {output_file.stat().st_size:,} bytes")
    else:
        console.print(f"[red]❌ Conversion failed[/red]")


def demo_stl_info():
    """Demonstrate STL file analysis."""
    console = Console()
    console.print("\n[bold blue]📊 STL File Analysis Demo[/bold blue]")
    
    stl_file = Path("_models/multiverse/tile_2x2_borde.stl")
    
    if not stl_file.exists():
        console.print(f"[red]STL file not found: {stl_file}[/red]")
        return
    
    # Get detailed STL information
    info = get_stl_info(stl_file)
    
    if info and 'error' not in info:
        # Create a nice table for the information
        table = Table(title=f"STL Analysis: {stl_file.name}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("File Size", f"{info['file_size']:,} bytes")
        table.add_row("Triangles", f"{info['triangles']:,}")
        table.add_row("Unique Vertices", f"{info['unique_vertices']:,}")
        table.add_row("Total Vertices", f"{info['total_vertices']:,}")
        table.add_row("Volume", f"{info['volume']:.2f} mm³")
        table.add_row("Surface Area", f"{info['surface_area']:.2f} mm²")
        table.add_row("Dimensions (X,Y,Z)", 
                     f"{info['dimensions'][0]:.1f} × {info['dimensions'][1]:.1f} × {info['dimensions'][2]:.1f} mm")
        table.add_row("Center of Gravity", 
                     f"({info['center_of_gravity'][0]:.2f}, {info['center_of_gravity'][1]:.2f}, {info['center_of_gravity'][2]:.2f})")
        table.add_row("Valid Mesh", "✅ Yes" if info['is_valid'] else "❌ No")
        
        console.print(table)
    else:
        console.print(f"[red]Failed to analyze STL file: {info.get('error', 'Unknown error')}[/red]")


def demo_advanced_converter():
    """Demonstrate the advanced STL converter with progress tracking."""
    console = Console()
    console.print("\n[bold blue]🚀 Advanced STL Converter Demo[/bold blue]")
    
    # Create converter with custom settings
    converter = STLConverter(
        include_metadata=True,
        validate=True
    )
    
    stl_files = list(Path("_models").glob("**/*.stl"))
    
    if not stl_files:
        console.print("[yellow]No STL files found in _models directory[/yellow]")
        return
    
    output_dir = Path("advanced_converted")
    output_dir.mkdir(exist_ok=True)
    
    console.print(f"Converting {len(stl_files)} STL files...")
    
    with Progress() as progress:
        task = progress.add_task("Converting files...", total=len(stl_files))
        
        for stl_file in stl_files:
            output_file = output_dir / f"{stl_file.stem}.3mf"
            
            # Convert with the advanced converter
            success = converter.convert(stl_file, output_file)
            
            if success:
                progress.console.print(f"✅ {stl_file.name} → {output_file.name}")
            else:
                progress.console.print(f"❌ Failed: {stl_file.name}")
            
            progress.advance(task)
    
    # Show conversion statistics
    stats = converter.get_conversion_stats()
    
    if stats:
        console.print("\n[bold green]📈 Conversion Statistics[/bold green]")
        
        stats_table = Table()
        stats_table.add_column("File", style="cyan")
        stats_table.add_column("Vertices", style="green")
        stats_table.add_column("Triangles", style="yellow")
        stats_table.add_column("Time (s)", style="magenta")
        stats_table.add_column("Speed (tri/s)", style="blue")
        
        total_vertices = 0
        total_triangles = 0
        total_time = 0
        
        for output_path, file_stats in stats.items():
            if 'error' not in file_stats:
                vertices = file_stats['vertices']
                triangles = file_stats['triangles']
                conv_time = file_stats['conversion_time']
                speed = triangles / conv_time if conv_time > 0 else 0
                
                total_vertices += vertices
                total_triangles += triangles
                total_time += conv_time
                
                stats_table.add_row(
                    Path(output_path).name,
                    f"{vertices:,}",
                    f"{triangles:,}",
                    f"{conv_time:.3f}",
                    f"{speed:,.0f}"
                )
        
        console.print(stats_table)
        
        # Summary
        console.print(f"\n[bold]Summary:[/bold]")
        console.print(f"Total vertices processed: {total_vertices:,}")
        console.print(f"Total triangles processed: {total_triangles:,}")
        console.print(f"Total conversion time: {total_time:.3f} seconds")
        console.print(f"Average speed: {total_triangles / total_time:,.0f} triangles/second")


def demo_batch_conversion():
    """Demonstrate batch conversion with glob patterns."""
    console = Console()
    console.print("\n[bold blue]📦 Batch Conversion Demo[/bold blue]")
    
    # Batch convert all STL files in the _models directory
    converted_files = batch_stl_to_3mf("_models/**/*.stl", "batch_converted")
    
    console.print(f"[green]Successfully converted {len(converted_files)} files:[/green]")
    for file_path in converted_files:
        file_size = Path(file_path).stat().st_size
        console.print(f"  📄 {Path(file_path).name} ({file_size:,} bytes)")


if __name__ == "__main__":
    console = Console()
    
    console.print("[bold magenta]🎯 Noah123d Advanced STL Converter Examples[/bold magenta]")
    console.print("=" * 60)
    
    # Run all demos
    demo_simple_conversion()
    demo_stl_info()
    demo_advanced_converter()
    demo_batch_conversion()
    
    console.print("\n[bold green]🎉 All converter examples completed successfully![/bold green]")
