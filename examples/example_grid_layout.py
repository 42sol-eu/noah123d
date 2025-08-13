"""Example demonstrating STL to 3MF conversion with grid layout of multiple copies."""

from pathlib import Path
from rich import print
from rich.console import Console
from rich.table import Table
from noah123d import STLConverter, stl_to_3mf_grid, get_stl_info


def demo_grid_layouts():
    """Demonstrate different grid layouts for STL conversion."""
    console = Console()
    console.print("[bold blue]🔲 STL Grid Layout Examples[/bold blue]")
    
    stl_file = Path("_models/multiverse/tile_2x2_borde.stl")
    
    if not stl_file.exists():
        console.print(f"[red]STL file not found: {stl_file}[/red]")
        return
    
    # Get STL info first
    info = get_stl_info(stl_file)
    if info and 'error' not in info:
        console.print(f"\n[cyan]📊 Source STL: {stl_file.name}[/cyan]")
        console.print(f"Dimensions: {info['dimensions'][0]:.1f} × {info['dimensions'][1]:.1f} × {info['dimensions'][2]:.1f} mm")
        console.print(f"Triangles: {info['triangles']:,}")
    
    # Example 1: 2x2 grid (4 copies)
    console.print(f"\n[yellow]Example 1: 2×2 Grid (4 copies)[/yellow]")
    output_file = Path("grid_2x2.3mf")
    success = stl_to_3mf_grid(
        stl_path=stl_file,
        output_path=output_file,
        count=4,
        grid_cols=2,
        spacing_factor=1.2,  # 20% spacing
        center_grid=True
    )
    
    if success:
        console.print(f"✅ Created: {output_file.name} ({output_file.stat().st_size:,} bytes)")
    else:
        console.print(f"❌ Failed to create {output_file.name}")
    
    # Example 2: 3x3 grid (9 copies)
    console.print(f"\n[yellow]Example 2: 3×3 Grid (9 copies)[/yellow]")
    output_file = Path("grid_3x3.3mf")
    success = stl_to_3mf_grid(
        stl_path=stl_file,
        output_path=output_file,
        count=9,
        grid_cols=3,
        spacing_factor=1.1,  # 10% spacing
        center_grid=True
    )
    
    if success:
        console.print(f"✅ Created: {output_file.name} ({output_file.stat().st_size:,} bytes)")
    else:
        console.print(f"❌ Failed to create {output_file.name}")
    
    # Example 3: Single row (5 copies)
    console.print(f"\n[yellow]Example 3: Single Row (5 copies)[/yellow]")
    output_file = Path("grid_1x5.3mf")
    success = stl_to_3mf_grid(
        stl_path=stl_file,
        output_path=output_file,
        count=5,
        grid_cols=5,
        spacing_factor=1.5,  # 50% spacing
        center_grid=True
    )
    
    if success:
        console.print(f"✅ Created: {output_file.name} ({output_file.stat().st_size:,} bytes)")
    else:
        console.print(f"❌ Failed to create {output_file.name}")
    
    # Example 4: Auto-layout (6 copies)
    console.print(f"\n[yellow]Example 4: Auto Layout (6 copies)[/yellow]")
    output_file = Path("grid_auto.3mf")
    success = stl_to_3mf_grid(
        stl_path=stl_file,
        output_path=output_file,
        count=6,  # Will auto-calculate as 3x2 grid
        spacing_factor=1.0,  # No gap (touching)
        center_grid=False
    )
    
    if success:
        console.print(f"✅ Created: {output_file.name} ({output_file.stat().st_size:,} bytes)")
    else:
        console.print(f"❌ Failed to create {output_file.name}")


def demo_advanced_grid():
    """Demonstrate advanced grid conversion with custom spacing."""
    console = Console()
    console.print(f"\n[bold blue]🚀 Advanced Grid Conversion[/bold blue]")
    
    stl_file = Path("_models/multiverse/tile_2x2_borde.stl")
    
    if not stl_file.exists():
        console.print(f"[red]STL file not found: {stl_file}[/red]")
        return
    
    # Create converter with custom settings
    converter = STLConverter(include_metadata=True, validate=True)
    
    # Test different grid configurations
    configurations = [
        {"count": 4, "cols": 2, "spacing": 1.0, "name": "tight_2x2"},
        {"count": 4, "cols": 2, "spacing": 1.5, "name": "spaced_2x2"},
        {"count": 8, "cols": 4, "spacing": 1.2, "name": "wide_4x2"},
        {"count": 12, "cols": 3, "spacing": 1.1, "name": "medium_3x4"},
    ]
    
    table = Table(title="Grid Conversion Results")
    table.add_column("Configuration", style="cyan")
    table.add_column("Grid Layout", style="magenta")
    table.add_column("Spacing", style="green")
    table.add_column("File Size", style="yellow")
    table.add_column("Objects", style="blue")
    table.add_column("Time (s)", style="red")
    
    for config in configurations:
        output_file = Path(f"advanced_{config['name']}.3mf")
        
        console.print(f"Creating {config['name']}...")
        
        success = converter.convert_with_copies(
            stl_path=stl_file,
            output_path=output_file,
            count=config['count'],
            grid_cols=config['cols'],
            spacing_factor=config['spacing'],
            center_grid=True
        )
        
        if success:
            stats = converter.get_conversion_stats()[str(output_file)]
            file_size = output_file.stat().st_size
            
            table.add_row(
                config['name'],
                f"{stats['grid_layout'][0]}×{stats['grid_layout'][1]}",
                f"{config['spacing']:.1f}",
                f"{file_size:,} bytes",
                str(config['count']),
                f"{stats['conversion_time']:.3f}"
            )
        else:
            table.add_row(config['name'], "Failed", "-", "-", "-", "-")
    
    console.print(table)
    
    # Show overall statistics
    stats = converter.get_conversion_stats()
    if stats:
        console.print(f"\n[bold green]📊 Conversion Summary[/bold green]")
        total_objects = sum(s.get('copies', 0) for s in stats.values() if 'error' not in s)
        total_time = sum(s.get('conversion_time', 0) for s in stats.values() if 'error' not in s)
        total_triangles = sum(s.get('triangles', 0) for s in stats.values() if 'error' not in s)
        
        console.print(f"Total objects created: {total_objects}")
        console.print(f"Total triangles processed: {total_triangles:,}")
        console.print(f"Total conversion time: {total_time:.3f} seconds")
        console.print(f"Average speed: {total_triangles / total_time:,.0f} triangles/second")


def analyze_grid_files():
    """Analyze the created grid files with detailed model information."""
    console = Console()
    console.print(f"\n[bold blue]📋 Grid File Analysis[/bold blue]")
    
    # Find all grid files
    grid_files = list(Path(".").glob("grid_*.3mf")) + list(Path(".").glob("advanced_*.3mf"))
    
    if not grid_files:
        console.print("[yellow]No grid files found to analyze[/yellow]")
        return
    
    from noah123d import Archive, Directory, Model, analyze_3mf, get_model_center_of_mass, get_model_dimensions
    
    analysis_table = Table(title="Grid File Analysis")
    analysis_table.add_column("File", style="cyan")
    analysis_table.add_column("Objects", style="magenta")
    analysis_table.add_column("Total Vertices", style="green")
    analysis_table.add_column("Total Triangles", style="yellow")
    analysis_table.add_column("File Size", style="blue")
    
    for grid_file in sorted(grid_files):
        try:
            with Archive(grid_file, 'r') as archive:
                with Directory('3D') as models_dir:
                    with Model() as model:
                        object_count = model.get_object_count()
                        total_vertices = 0
                        total_triangles = 0
                        
                        for obj_id in model.list_objects():
                            obj = model.get_object(obj_id)
                            if obj:
                                total_vertices += len(obj['vertices'])
                                total_triangles += len(obj['triangles'])
                        
                        file_size = grid_file.stat().st_size
                        
                        analysis_table.add_row(
                            grid_file.name,
                            str(object_count),
                            f"{total_vertices:,}",
                            f"{total_triangles:,}",
                            f"{file_size:,} bytes"
                        )
        
        except Exception as e:
            analysis_table.add_row(grid_file.name, "Error", "-", "-", f"Error: {e}")
    
    console.print(analysis_table)
    
    # Detailed analysis of first grid file using new analyzer
    if grid_files:
        console.print(f"\n[bold cyan]🔍 Detailed Analysis of {grid_files[0].name}[/bold cyan]")
        
        analysis = analyze_3mf(grid_files[0])
        if 'error' not in analysis:
            summary = analysis['summary']
            
            # Overall information
            console.print(f"Overall center of mass: {summary.get('overall_center_of_mass', 'N/A')}")
            console.print(f"Overall dimensions: {summary.get('overall_dimensions', 'N/A')}")
            
            # Individual model analysis
            if analysis['models']:
                model_table = Table(title="Individual Model Analysis")
                model_table.add_column("Model ID", style="cyan")
                model_table.add_column("Center of Mass", style="green")
                model_table.add_column("Dimensions", style="yellow")
                model_table.add_column("Volume", style="blue")
                model_table.add_column("Surface Area", style="red")
                
                for model in analysis['models'][:5]:  # Show first 5 models
                    com = model['center_of_mass']
                    dims = model['dimensions']
                    
                    model_table.add_row(
                        str(model['object_id']),
                        f"({com[0]:.1f}, {com[1]:.1f}, {com[2]:.1f})",
                        f"{dims[0]:.1f}×{dims[1]:.1f}×{dims[2]:.1f}",
                        f"{model['volume']:.1f} mm³",
                        f"{model['surface_area']:.1f} mm²"
                    )
                
                console.print(model_table)
                
                if len(analysis['models']) > 5:
                    console.print(f"[dim]... and {len(analysis['models']) - 5} more models[/dim]")
        else:
            console.print(f"[red]Analysis failed: {analysis['error']}[/red]")


if __name__ == "__main__":
    console = Console()
    
    console.print("[bold magenta]🎯 Noah123d Grid Layout Examples[/bold magenta]")
    console.print("=" * 60)
    
    # Run all examples
    demo_grid_layouts()
    demo_advanced_grid()
    analyze_grid_files()
    
    console.print(f"\n[bold green]🎉 Grid layout examples completed![/bold green]")
    console.print(f"[yellow]💡 Tip: Open the generated 3MF files in a 3D viewer to see the grid layouts![/yellow]")
