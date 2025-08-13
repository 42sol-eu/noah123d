"""Example: Converting multiple STL files with counts to a single 3MF assembly."""

from pathlib import Path
from rich import print
from rich.console import Console
from rich.table import Table
from noah123d import multi_stl_to_3mf, STLConverter, get_stl_info


def create_multi_stl_assembly():
    """
    Demonstrate creating a 3MF assembly from multiple STL files with different counts.
    
    This example shows how to combine different STL parts into a single 3MF file,
    specifying how many copies of each part should be included.
    """
    console = Console()
    console.print("[bold blue]🔧 Multi-STL Assembly Example[/bold blue]")
    console.print("Creating a 3MF assembly from multiple STL files with specified counts...\n")
    
    # Example 1: Simple assembly with different layout modes
    console.print("[green]Example 1: Creating assemblies with different layout modes[/green]")
    
    # Define the STL objects for our assembly
    # Note: These are example paths - you would use your actual STL files
    stl_objects = [
        {
            'path': '_models/multiverse/tile_2x2_borde.stl',
            'count': 1,
            'name': 'Base_Tile'
        },
        {
            'path': '_models/multiverse/clip_dual.stl', 
            'count': 4,
            'name': 'Clip'
        },
        {
            'path': '_models/multiverse/clip_dual_light.stl',
            'count': 2,
            'name': 'Light_Clip'
        }
    ]
    
    # Check if STL files exist
    existing_stl_objects = []
    for obj in stl_objects:
        stl_path = Path(obj['path'])
        if stl_path.exists():
            existing_stl_objects.append(obj)
            console.print(f"✓ Found: {stl_path.name}")
        else:
            console.print(f"⚠ Missing: {stl_path} (skipping)")
    
    if not existing_stl_objects:
        console.print("[red]No STL files found. Please ensure STL files exist in the _models/multiverse/ directory.[/red]")
        return
    
    # Create assemblies with different layout modes
    layout_modes = ['grid', 'linear', 'stack']
    
    for layout_mode in layout_modes:
        output_file = f"assembly_{layout_mode}.3mf"
        console.print(f"\n📦 Creating {layout_mode} layout assembly: {output_file}")
        
        success = multi_stl_to_3mf(
            stl_objects=existing_stl_objects,
            output_path=output_file,
            layout_mode=layout_mode,
            spacing_factor=1.2,  # 20% spacing between objects
            center_layout=True,
            include_metadata=True
        )
        
        if success:
            console.print(f"✅ Successfully created {output_file}")
            analyze_assembly(output_file, console)
        else:
            console.print(f"❌ Failed to create {output_file}")


def create_custom_assembly():
    """Create a custom assembly with user-defined specifications."""
    console = Console()
    console.print("\n[green]Example 2: Custom assembly with varied counts[/green]")
    
    # Create a more complex assembly
    custom_objects = []
    
    # Find available STL files in the models directory
    model_dir = Path("_models/multiverse")
    if model_dir.exists():
        stl_files = list(model_dir.glob("*.stl"))
        
        if stl_files:
            # Create an assembly using available STL files
            for i, stl_file in enumerate(stl_files[:3]):  # Use up to 3 different files
                count = [1, 3, 2][i % 3]  # Varying counts
                custom_objects.append({
                    'path': str(stl_file),
                    'count': count,
                    'name': f"Part_{stl_file.stem}"
                })
            
            console.print("Creating custom assembly with:")
            for obj in custom_objects:
                console.print(f"  - {obj['count']}x {obj['name']} ({Path(obj['path']).name})")
            
            success = multi_stl_to_3mf(
                stl_objects=custom_objects,
                output_path="custom_assembly.3mf",
                layout_mode='grid',
                spacing_factor=1.5,
                center_layout=True
            )
            
            if success:
                console.print("✅ Custom assembly created: custom_assembly.3mf")
                analyze_assembly("custom_assembly.3mf", console)
            else:
                console.print("❌ Failed to create custom assembly")
        else:
            console.print("No STL files found in _models/multiverse directory")
    else:
        console.print("_models/multiverse directory not found")


def demonstrate_advanced_converter():
    """Demonstrate using the STLConverter class directly for more control."""
    console = Console()
    console.print("\n[green]Example 3: Using STLConverter class for advanced control[/green]")
    
    # Create converter with custom settings
    converter = STLConverter(
        include_metadata=True,
        compress=True,
        validate=True
    )
    
    # Example with error handling and statistics
    model_dir = Path("_models/multiverse")
    if model_dir.exists():
        stl_files = list(model_dir.glob("*.stl"))
        
        if stl_files:
            # Create assembly specification
            advanced_objects = [
                {
                    'path': str(stl_files[0]),
                    'count': 2,
                    'name': 'Primary_Component'
                }
            ]
            
            # Add more files if available
            if len(stl_files) > 1:
                advanced_objects.append({
                    'path': str(stl_files[1]),
                    'count': 6,
                    'name': 'Secondary_Component'
                })
            
            success = converter.convert_multiple_stl_with_counts(
                stl_objects=advanced_objects,
                output_path="advanced_assembly.3mf",
                layout_mode='grid',
                spacing_factor=1.3,
                center_layout=True
            )
            
            if success:
                console.print("✅ Advanced assembly created: advanced_assembly.3mf")
                
                # Get conversion statistics
                stats = converter.get_conversion_stats()
                if "advanced_assembly.3mf" in stats:
                    assembly_stats = stats["advanced_assembly.3mf"]
                    console.print("\n📊 Conversion Statistics:")
                    console.print(f"  - STL Files: {assembly_stats.get('total_stl_files', 'N/A')}")
                    console.print(f"  - Total Objects: {assembly_stats.get('total_objects', 'N/A')}")
                    console.print(f"  - Total Vertices: {assembly_stats.get('total_vertices', 'N/A'):,}")
                    console.print(f"  - Total Triangles: {assembly_stats.get('total_triangles', 'N/A'):,}")
                    console.print(f"  - Conversion Time: {assembly_stats.get('conversion_time', 0):.3f}s")
                    console.print(f"  - Layout Mode: {assembly_stats.get('layout_mode', 'N/A')}")
                
                analyze_assembly("advanced_assembly.3mf", console)
            else:
                console.print("❌ Failed to create advanced assembly")
                # Check for errors in stats
                stats = converter.get_conversion_stats()
                if "advanced_assembly.3mf" in stats and 'error' in stats["advanced_assembly.3mf"]:
                    console.print(f"Error: {stats['advanced_assembly.3mf']['error']}")


def analyze_assembly(file_path: str, console: Console):
    """Analyze the created 3MF assembly file."""
    from noah123d import Archive, Directory, Model
    
    assembly_path = Path(file_path)
    if not assembly_path.exists():
        return
    
    console.print(f"\n🔍 Analyzing assembly: {file_path}")
    
    try:
        with Archive(assembly_path, 'r') as archive:
            contents = archive.list_contents()
            console.print(f"  Archive contains {len(contents)} files")
            
            # Check for metadata
            if any('Metadata' in content for content in contents):
                console.print("  ✓ Metadata included")
                
            with Directory('3D') as models_dir:
                with Model() as model:
                    object_count = model.get_object_count()
                    console.print(f"  📦 Contains {object_count} 3D objects")
                    
                    if object_count > 0:
                        # Show first few objects
                        for i in range(min(3, object_count)):
                            obj = model.get_object(i + 1)
                            if obj:
                                name = obj.get('name', f'Object_{i+1}')
                                vertices = len(obj.get('vertices', []))
                                triangles = len(obj.get('triangles', []))
                                console.print(f"    - {name}: {vertices:,} vertices, {triangles:,} triangles")
                        
                        if object_count > 3:
                            console.print(f"    ... and {object_count - 3} more objects")
                            
    except Exception as e:
        console.print(f"  ❌ Error analyzing assembly: {e}")


def show_usage_examples():
    """Show various usage examples and best practices."""
    console = Console()
    console.print("\n[bold cyan]📚 Usage Examples and Best Practices[/bold cyan]")
    
    # Create a table with usage examples
    table = Table(title="Multi-STL to 3MF Usage Examples")
    table.add_column("Use Case", style="cyan")
    table.add_column("Code Example", style="green")
    table.add_column("Description", style="yellow")
    
    table.add_row(
        "Simple Assembly",
        """stl_objects = [
    {'path': 'base.stl', 'count': 1},
    {'path': 'screw.stl', 'count': 4}
]
multi_stl_to_3mf(stl_objects, 'assembly.3mf')""",
        "Basic assembly with default grid layout"
    )
    
    table.add_row(
        "Linear Layout",
        """multi_stl_to_3mf(
    stl_objects, 
    'linear_assembly.3mf',
    layout_mode='linear'
)""",
        "Arrange all objects in a single line"
    )
    
    table.add_row(
        "Custom Spacing",
        """multi_stl_to_3mf(
    stl_objects,
    'spaced_assembly.3mf', 
    spacing_factor=2.0,
    center_layout=False
)""",
        "Double spacing, no centering"
    )
    
    table.add_row(
        "Vertical Stack",
        """multi_stl_to_3mf(
    stl_objects,
    'stack_assembly.3mf',
    layout_mode='stack'
)""",
        "Stack objects vertically (Z-axis)"
    )
    
    console.print(table)
    
    console.print("\n[bold]🎯 Key Features:[/bold]")
    console.print("  • Multiple STL files with individual counts")
    console.print("  • Flexible layout modes: grid, linear, stack")
    console.print("  • Automatic spacing calculation")
    console.print("  • Detailed metadata generation")
    console.print("  • Error handling and validation")
    console.print("  • Performance statistics")


if __name__ == "__main__":
    console = Console()
    
    try:
        # Show usage examples first
        show_usage_examples()
        
        # Run the examples
        create_multi_stl_assembly()
        create_custom_assembly()
        demonstrate_advanced_converter()
        
        console.print("\n[bold green]🎉 Multi-STL assembly examples completed![/bold green]")
        console.print("\nCheck the generated .3mf files:")
        
        # List generated files
        for file_pattern in ["assembly_*.3mf", "custom_assembly.3mf", "advanced_assembly.3mf"]:
            import glob
            files = glob.glob(file_pattern)
            for file in files:
                file_path = Path(file)
                if file_path.exists():
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    console.print(f"  📄 {file} ({size_mb:.2f} MB)")
        
    except Exception as e:
        console.print(f"[red]❌ Error running examples: {e}[/red]")
        import traceback
        console.print(f"[red]{traceback.format_exc()}[/red]")
