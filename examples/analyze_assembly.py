import sys
from pathlib import Path

# Add the parent directory to Python path for development
sys.path.insert(0, str(Path(__file__).parent.parent))

from noah123d import Archive3mf, Directory, Model
from rich.console import Console
from rich.table import Table

def analyze_assembly(file_path: str):
    """Analyze the created 3MF assembly file."""
    console = Console()
    assembly_path = Path(file_path)
    
    if not assembly_path.exists():
        console.print(f"[red]❌ File not found: {file_path}[/red]")
        return
    
    console.print(f"[bold blue]🔍 Analyzing 3MF Assembly: {file_path}[/bold blue]")
    console.print(f"📁 File size: {assembly_path.stat().st_size / (1024*1024):.2f} MB")
    
    try:
        with Archive3mf(assembly_path, 'r') as archive:
            contents = archive.list_contents()
            console.print(f"\n📦 Archive contains {len(contents)} files:")
            for content in sorted(contents):
                console.print(f"   📄 {content}")
            
            # Check for metadata
            metadata_files = [c for c in contents if 'Metadata' in c]
            if metadata_files:
                console.print(f"\n📋 Metadata files found: {len(metadata_files)}")
                
            with Directory('3D') as models_dir:
                with Model() as model:
                    object_count = model.get_object_count()
                    console.print(f"\n🎯 Model Analysis:")
                    console.print(f"   Total Objects: {object_count}")
                    
                    if object_count > 0:
                        # Create a table for object details
                        table = Table(title="3D Objects in Assembly")
                        table.add_column("Object ID", style="cyan")
                        table.add_column("Vertices", style="green")
                        table.add_column("Triangles", style="yellow")
                        
                        total_vertices = 0
                        total_triangles = 0
                        actual_objects = 0
                        
                        # Check a wider range of object IDs to find all objects
                        for i in range(1, max(20, object_count + 10)):  # Check up to 20 or object_count+10
                            obj = model.get_object(i)
                            if obj:
                                vertices = len(obj.get('vertices', []))
                                triangles = len(obj.get('triangles', []))
                                total_vertices += vertices
                                total_triangles += triangles
                                actual_objects += 1
                                table.add_row(
                                    str(i),
                                    f"{vertices:,}",
                                    f"{triangles:,}"
                                )
                        
                        console.print(table)
                        
                        console.print(f"\n📊 Assembly Totals:")
                        console.print(f"   Reported Object Count: {object_count}")
                        console.print(f"   Actual Objects Found: {actual_objects}")
                        console.print(f"   Total Vertices: {total_vertices:,}")
                        console.print(f"   Total Triangles: {total_triangles:,}")
                        
    except Exception as e:
        console.print(f"[red]❌ Error analyzing assembly: {e}[/red]")

if __name__ == "__main__":
    import sys
    file_to_analyze = sys.argv[1] if len(sys.argv) > 1 else "printer_kit.3mf"
    analyze_assembly(file_to_analyze)
