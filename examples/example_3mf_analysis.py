"""Example demonstrating 3MF file analysis capabilities."""

from pathlib import Path
from rich import print
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from noah123d import analyze_3mf, get_model_center_of_mass, get_model_dimensions, Analysis3MF


def demo_basic_analysis():
    """Demonstrate basic 3MF file analysis."""
    console = Console()
    console.print("[bold blue]📊 Basic 3MF Analysis[/bold blue]")
    
    # Find a 3MF file to analyze
    test_files = list(Path(".").glob("*.3mf"))
    
    if not test_files:
        console.print("[yellow]No 3MF files found. Creating a test file first...[/yellow]")
        # Create a simple test file
        from noah123d import stl_to_3mf_grid
        stl_file = Path("_models/multiverse/tile_2x2_borde.stl")
        if stl_file.exists():
            stl_to_3mf_grid(stl_file, "test_analysis.3mf", count=4, grid_cols=2)
            test_files = [Path("test_analysis.3mf")]
        else:
            console.print("[red]No STL files available for testing[/red]")
            return
    
    # Analyze the first file
    test_file = test_files[0]
    console.print(f"\n[cyan]Analyzing: {test_file.name}[/cyan]")
    
    # Basic analysis
    analysis = analyze_3mf(test_file)
    
    if 'error' in analysis:
        console.print(f"[red]Analysis failed: {analysis['error']}[/red]")
        return
    
    # Display results
    summary = analysis['summary']
    console.print(Panel(
        f"[bold]File Analysis Results[/bold]\n"
        f"Objects: {summary['object_count']}\n"
        f"Total Vertices: {summary['total_vertices']:,}\n"
        f"Total Triangles: {summary['total_triangles']:,}\n"
        f"File Size: {analysis['file_size']:,} bytes",
        title=f"Summary: {test_file.name}"
    ))
    
    # Show overall dimensions and center of mass
    if summary.get('overall_dimensions'):
        dims = summary['overall_dimensions']
        console.print(f"📏 Overall Dimensions: {dims[0]:.2f} × {dims[1]:.2f} × {dims[2]:.2f} mm")
    
    if summary.get('overall_center_of_mass'):
        com = summary['overall_center_of_mass']
        console.print(f"⚖️  Overall Center of Mass: ({com[0]:.2f}, {com[1]:.2f}, {com[2]:.2f})")


def demo_convenience_functions():
    """Demonstrate convenience functions for getting specific information."""
    console = Console()
    console.print(f"\n[bold blue]🔧 Convenience Functions[/bold blue]")
    
    test_files = list(Path(".").glob("*.3mf"))
    if not test_files:
        console.print("[yellow]No 3MF files found to analyze[/yellow]")
        return
    
    test_file = test_files[0]
    
    # Get overall center of mass
    center_of_mass = get_model_center_of_mass(test_file)
    if center_of_mass:
        console.print(f"🎯 Center of Mass: ({center_of_mass[0]:.2f}, {center_of_mass[1]:.2f}, {center_of_mass[2]:.2f})")
    
    # Get overall dimensions
    dimensions = get_model_dimensions(test_file)
    if dimensions:
        console.print(f"📐 Dimensions: {dimensions[0]:.2f} × {dimensions[1]:.2f} × {dimensions[2]:.2f} mm")
    
    # Get individual model information
    analyzer = Analysis3MF()
    analysis = analyzer.analyze_file(test_file)
    
    if 'error' not in analysis and analysis['models']:
        console.print(f"\n[cyan]Individual Model Information:[/cyan]")
        
        for i, model in enumerate(analysis['models'][:3]):  # Show first 3 models
            model_id = model['object_id']
            
            # Get specific model center of mass
            model_com = get_model_center_of_mass(test_file, model_id)
            model_dims = get_model_dimensions(test_file, model_id)
            
            console.print(f"Model {model_id}:")
            console.print(f"  Center of Mass: ({model_com[0]:.2f}, {model_com[1]:.2f}, {model_com[2]:.2f})")
            console.print(f"  Dimensions: {model_dims[0]:.2f} × {model_dims[1]:.2f} × {model_dims[2]:.2f} mm")
            console.print(f"  Volume: {model['volume']:.2f} mm³")
            console.print(f"  Surface Area: {model['surface_area']:.2f} mm²")


def demo_detailed_analysis():
    """Demonstrate detailed analysis of multiple models."""
    console = Console()
    console.print(f"\n[bold blue]🔍 Detailed Multi-Model Analysis[/bold blue]")
    
    # Find grid files (which have multiple models)
    grid_files = list(Path(".").glob("grid_*.3mf")) + list(Path(".").glob("advanced_*.3mf"))
    
    if not grid_files:
        console.print("[yellow]No grid files found. Run the grid examples first.[/yellow]")
        return
    
    # Analyze a grid file with multiple objects
    grid_file = grid_files[0]
    console.print(f"Analyzing grid file: {grid_file.name}")
    
    analyzer = Analysis3MF()
    analysis = analyzer.analyze_file(grid_file)
    
    if 'error' in analysis:
        console.print(f"[red]Analysis failed: {analysis['error']}[/red]")
        return
    
    # Create detailed table
    table = Table(title=f"Detailed Analysis: {grid_file.name}")
    table.add_column("Model ID", style="cyan")
    table.add_column("Position", style="green")
    table.add_column("Dimensions", style="yellow")
    table.add_column("Volume", style="blue")
    table.add_column("Surface Area", style="red")
    table.add_column("Vertices", style="magenta")
    
    total_volume = 0
    total_surface_area = 0
    
    for model in analysis['models']:
        com = model['center_of_mass']
        dims = model['dimensions']
        
        table.add_row(
            str(model['object_id']),
            f"({com[0]:.1f}, {com[1]:.1f}, {com[2]:.1f})",
            f"{dims[0]:.1f}×{dims[1]:.1f}×{dims[2]:.1f}",
            f"{model['volume']:.1f}",
            f"{model['surface_area']:.1f}",
            f"{model['vertex_count']:,}"
        )
        
        total_volume += model['volume']
        total_surface_area += model['surface_area']
    
    console.print(table)
    
    # Summary statistics
    console.print(f"\n[bold green]📈 Summary Statistics[/bold green]")
    console.print(f"Total Models: {len(analysis['models'])}")
    console.print(f"Total Volume: {total_volume:.1f} mm³")
    console.print(f"Total Surface Area: {total_surface_area:.1f} mm²")
    console.print(f"Average Volume per Model: {total_volume / len(analysis['models']):.1f} mm³")


def demo_file_comparison():
    """Demonstrate comparison between different 3MF files."""
    console = Console()
    console.print(f"\n[bold blue]⚖️  3MF File Comparison[/bold blue]")
    
    # Find multiple 3MF files
    mf_files = list(Path(".").glob("*.3mf"))
    
    if len(mf_files) < 2:
        console.print("[yellow]Need at least 2 3MF files for comparison[/yellow]")
        return
    
    # Analyze multiple files
    comparison_table = Table(title="3MF File Comparison")
    comparison_table.add_column("File", style="cyan")
    comparison_table.add_column("Objects", style="magenta")
    comparison_table.add_column("Total Volume", style="green")
    comparison_table.add_column("Avg Volume/Object", style="yellow")
    comparison_table.add_column("Overall Dimensions", style="blue")
    comparison_table.add_column("Center of Mass", style="red")
    
    for mf_file in sorted(mf_files)[:5]:  # Limit to 5 files
        analysis = analyze_3mf(mf_file)
        
        if 'error' not in analysis:
            summary = analysis['summary']
            
            # Calculate total volume
            total_volume = sum(model['volume'] for model in analysis['models'])
            avg_volume = total_volume / len(analysis['models']) if analysis['models'] else 0
            
            # Format dimensions and center of mass
            dims = summary.get('overall_dimensions', [0, 0, 0])
            com = summary.get('overall_center_of_mass', [0, 0, 0])
            
            comparison_table.add_row(
                mf_file.name,
                str(summary['object_count']),
                f"{total_volume:.1f} mm³",
                f"{avg_volume:.1f} mm³",
                f"{dims[0]:.1f}×{dims[1]:.1f}×{dims[2]:.1f}",
                f"({com[0]:.1f}, {com[1]:.1f}, {com[2]:.1f})"
            )
        else:
            comparison_table.add_row(mf_file.name, "Error", "-", "-", "-", "-")
    
    console.print(comparison_table)


def demo_analysis_export():
    """Demonstrate exporting analysis results."""
    console = Console()
    console.print(f"\n[bold blue]💾 Analysis Export[/bold blue]")
    
    test_files = list(Path(".").glob("*.3mf"))
    if not test_files:
        console.print("[yellow]No 3MF files found to analyze[/yellow]")
        return
    
    test_file = test_files[0]
    
    # Analyze and export
    analyzer = Analysis3MF()
    analysis = analyzer.analyze_file(test_file)
    
    if 'error' not in analysis:
        # Export to JSON
        import json
        export_file = test_file.with_suffix('.analysis.json')
        
        with open(export_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        console.print(f"✅ Analysis exported to: {export_file.name}")
        console.print(f"File size: {export_file.stat().st_size:,} bytes")
        
        # Show sample of exported data
        console.print(f"\n[dim]Sample exported data structure:[/dim]")
        sample = {
            'file_path': analysis['file_path'],
            'summary': {
                'object_count': analysis['summary']['object_count'],
                'total_vertices': analysis['summary']['total_vertices'],
                'overall_dimensions': analysis['summary'].get('overall_dimensions', 'N/A')
            },
            'models_count': len(analysis['models'])
        }
        console.print(json.dumps(sample, indent=2))
    else:
        console.print(f"[red]Analysis failed: {analysis['error']}[/red]")


if __name__ == "__main__":
    console = Console()
    
    console.print("[bold magenta]🎯 Noah123D 3MF File Analyzer Examples[/bold magenta]")
    console.print("=" * 70)
    
    # Run all demo functions
    demo_basic_analysis()
    demo_convenience_functions()
    demo_detailed_analysis()
    demo_file_comparison()
    demo_analysis_export()
    
    console.print(f"\n[bold green]🎉 3MF analysis examples completed![/bold green]")
    console.print(f"[yellow]💡 Tip: Use the analyzer to inspect your 3MF files before 3D printing![/yellow]")
