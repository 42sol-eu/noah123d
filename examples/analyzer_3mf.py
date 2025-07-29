"""3MF File Analyzer - Extract and analyze models from 3MF files."""

from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import json
from rich import print
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from noah123d import Archive3mf, Directory, Model


class Model3MFAnalyzer:
    """Analyzer for 3MF files to extract model information including center of mass and dimensions."""
    
    def __init__(self):
        """Initialize the analyzer."""
        self.console = Console()
    
    def analyze_3mf_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyze a 3MF file and extract detailed model information.
        
        Args:
            file_path: Path to the 3MF file
            
        Returns:
            Dictionary containing analysis results
        """
        if not file_path.exists():
            return {'error': f'File not found: {file_path}'}
        
        try:
            analysis = {
                'file_path': str(file_path),
                'file_size': file_path.stat().st_size,
                'models': [],
                'summary': {}
            }
            
            with Archive3mf(file_path, 'r') as archive:
                # Get archive contents
                contents = archive.list_contents()
                analysis['archive_contents'] = contents
                
                # Analyze models in 3D directory
                with Directory('3D') as models_dir:
                    with Model() as model:
                        object_count = model.get_object_count()
                        analysis['summary']['object_count'] = object_count
                        
                        if object_count == 0:
                            analysis['summary']['message'] = 'No objects found in 3MF file'
                            return analysis
                        
                        total_vertices = 0
                        total_triangles = 0
                        all_vertices = []
                        
                        # Analyze each object
                        for obj_id in model.list_objects():
                            obj = model.get_object(obj_id)
                            if obj:
                                obj_analysis = self._analyze_object(obj, obj_id)
                                analysis['models'].append(obj_analysis)
                                
                                total_vertices += len(obj['vertices'])
                                total_triangles += len(obj['triangles'])
                                all_vertices.extend(obj['vertices'])
                        
                        # Calculate overall statistics
                        analysis['summary'].update({
                            'total_vertices': total_vertices,
                            'total_triangles': total_triangles,
                            'overall_bounds': self._calculate_bounds(all_vertices),
                            'overall_center_of_mass': self._calculate_center_of_mass(all_vertices),
                            'overall_dimensions': None
                        })
                        
                        if all_vertices:
                            bounds = analysis['summary']['overall_bounds']
                            analysis['summary']['overall_dimensions'] = [
                                bounds['max'][0] - bounds['min'][0],
                                bounds['max'][1] - bounds['min'][1], 
                                bounds['max'][2] - bounds['min'][2]
                            ]
            
            return analysis
            
        except Exception as e:
            return {'error': f'Failed to analyze 3MF file: {str(e)}'}
    
    def _analyze_object(self, obj: Dict[str, Any], obj_id: int) -> Dict[str, Any]:
        """Analyze a single object and extract detailed information."""
        vertices = obj['vertices']
        triangles = obj['triangles']
        
        # Basic counts
        vertex_count = len(vertices)
        triangle_count = len(triangles)
        
        # Calculate bounding box
        bounds = self._calculate_bounds(vertices)
        
        # Calculate dimensions
        dimensions = [
            bounds['max'][0] - bounds['min'][0],
            bounds['max'][1] - bounds['min'][1],
            bounds['max'][2] - bounds['min'][2]
        ]
        
        # Calculate center of mass (geometric center)
        center_of_mass = self._calculate_center_of_mass(vertices)
        
        # Calculate volume and surface area (approximate)
        volume = self._calculate_volume(vertices, triangles)
        surface_area = self._calculate_surface_area(vertices, triangles)
        
        # Calculate mesh quality metrics
        quality = self._analyze_mesh_quality(vertices, triangles)
        
        return {
            'object_id': obj_id,
            'object_type': obj.get('type', 'model'),
            'vertex_count': vertex_count,
            'triangle_count': triangle_count,
            'bounds': bounds,
            'dimensions': dimensions,
            'center_of_mass': center_of_mass,
            'volume': volume,
            'surface_area': surface_area,
            'quality': quality
        }
    
    def _calculate_bounds(self, vertices: List[List[float]]) -> Dict[str, List[float]]:
        """Calculate bounding box for vertices."""
        if not vertices:
            return {'min': [0, 0, 0], 'max': [0, 0, 0]}
        
        min_x = min(v[0] for v in vertices)
        max_x = max(v[0] for v in vertices)
        min_y = min(v[1] for v in vertices)
        max_y = max(v[1] for v in vertices)
        min_z = min(v[2] for v in vertices)
        max_z = max(v[2] for v in vertices)
        
        return {
            'min': [min_x, min_y, min_z],
            'max': [max_x, max_y, max_z]
        }
    
    def _calculate_center_of_mass(self, vertices: List[List[float]]) -> List[float]:
        """Calculate center of mass (geometric center) of vertices."""
        if not vertices:
            return [0, 0, 0]
        
        sum_x = sum(v[0] for v in vertices)
        sum_y = sum(v[1] for v in vertices)
        sum_z = sum(v[2] for v in vertices)
        count = len(vertices)
        
        return [sum_x / count, sum_y / count, sum_z / count]
    
    def _calculate_volume(self, vertices: List[List[float]], triangles: List[List[int]]) -> float:
        """Calculate approximate volume using divergence theorem."""
        if not triangles or not vertices:
            return 0.0
        
        volume = 0.0
        
        for triangle in triangles:
            if len(triangle) >= 3:
                try:
                    v1 = vertices[triangle[0]]
                    v2 = vertices[triangle[1]]
                    v3 = vertices[triangle[2]]
                    
                    # Calculate signed volume of tetrahedron formed by triangle and origin
                    volume += (v1[0] * (v2[1] * v3[2] - v2[2] * v3[1]) +
                              v2[0] * (v3[1] * v1[2] - v3[2] * v1[1]) +
                              v3[0] * (v1[1] * v2[2] - v1[2] * v2[1])) / 6.0
                except (IndexError, TypeError):
                    continue
        
        return abs(volume)
    
    def _calculate_surface_area(self, vertices: List[List[float]], triangles: List[List[int]]) -> float:
        """Calculate surface area of the mesh."""
        if not triangles or not vertices:
            return 0.0
        
        import math
        total_area = 0.0
        
        for triangle in triangles:
            if len(triangle) >= 3:
                try:
                    v1 = vertices[triangle[0]]
                    v2 = vertices[triangle[1]]
                    v3 = vertices[triangle[2]]
                    
                    # Calculate triangle area using cross product
                    edge1 = [v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]]
                    edge2 = [v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2]]
                    
                    cross = [
                        edge1[1] * edge2[2] - edge1[2] * edge2[1],
                        edge1[2] * edge2[0] - edge1[0] * edge2[2],
                        edge1[0] * edge2[1] - edge1[1] * edge2[0]
                    ]
                    
                    area = 0.5 * math.sqrt(cross[0]**2 + cross[1]**2 + cross[2]**2)
                    total_area += area
                    
                except (IndexError, TypeError, ValueError):
                    continue
        
        return total_area
    
    def _analyze_mesh_quality(self, vertices: List[List[float]], triangles: List[List[int]]) -> Dict[str, Any]:
        """Analyze mesh quality metrics."""
        if not triangles or not vertices:
            return {'valid': False, 'degenerate_triangles': 0, 'edge_count': 0}
        
        degenerate_count = 0
        edges = set()
        
        for triangle in triangles:
            if len(triangle) >= 3:
                try:
                    v1 = vertices[triangle[0]]
                    v2 = vertices[triangle[1]]
                    v3 = vertices[triangle[2]]
                    
                    # Check for degenerate triangle (very small area)
                    edge1 = [v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]]
                    edge2 = [v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2]]
                    
                    cross = [
                        edge1[1] * edge2[2] - edge1[2] * edge2[1],
                        edge1[2] * edge2[0] - edge1[0] * edge2[2],
                        edge1[0] * edge2[1] - edge1[1] * edge2[0]
                    ]
                    
                    area = 0.5 * (cross[0]**2 + cross[1]**2 + cross[2]**2)**0.5
                    if area < 1e-10:
                        degenerate_count += 1
                    
                    # Count unique edges
                    for i in range(3):
                        edge = tuple(sorted([triangle[i], triangle[(i + 1) % 3]]))
                        edges.add(edge)
                        
                except (IndexError, TypeError, ValueError):
                    degenerate_count += 1
        
        return {
            'valid': degenerate_count == 0,
            'degenerate_triangles': degenerate_count,
            'edge_count': len(edges),
            'manifold_estimate': len(edges) <= len(triangles) * 1.5  # Rough estimate
        }
    
    def print_analysis(self, analysis: Dict[str, Any], detailed: bool = True):
        """Print analysis results in a formatted way."""
        if 'error' in analysis:
            self.console.print(f"[red]Error: {analysis['error']}[/red]")
            return
        
        # File header
        file_path = Path(analysis['file_path'])
        self.console.print(Panel(
            f"[bold blue]3MF File Analysis: {file_path.name}[/bold blue]\n"
            f"File Size: {analysis['file_size']:,} bytes\n"
            f"Archive Contents: {len(analysis['archive_contents'])} files",
            title="File Information"
        ))
        
        # Summary
        summary = analysis['summary']
        self.console.print(f"\n[bold green]📊 Summary[/bold green]")
        self.console.print(f"Objects: {summary['object_count']}")
        self.console.print(f"Total Vertices: {summary['total_vertices']:,}")
        self.console.print(f"Total Triangles: {summary['total_triangles']:,}")
        
        if summary.get('overall_dimensions'):
            dims = summary['overall_dimensions']
            self.console.print(f"Overall Dimensions: {dims[0]:.2f} × {dims[1]:.2f} × {dims[2]:.2f} mm")
        
        if summary.get('overall_center_of_mass'):
            com = summary['overall_center_of_mass']
            self.console.print(f"Overall Center of Mass: ({com[0]:.2f}, {com[1]:.2f}, {com[2]:.2f})")
        
        # Individual models
        if analysis['models'] and detailed:
            self.console.print(f"\n[bold yellow]🔍 Individual Models[/bold yellow]")
            
            table = Table(title="Model Details")
            table.add_column("ID", style="cyan")
            table.add_column("Type", style="magenta")
            table.add_column("Vertices", style="green")
            table.add_column("Triangles", style="yellow")
            table.add_column("Dimensions (mm)", style="blue")
            table.add_column("Center of Mass", style="red")
            table.add_column("Volume (mm³)", style="purple")
            
            for model in analysis['models']:
                dims = model['dimensions']
                com = model['center_of_mass']
                
                table.add_row(
                    str(model['object_id']),
                    model['object_type'],
                    f"{model['vertex_count']:,}",
                    f"{model['triangle_count']:,}",
                    f"{dims[0]:.1f}×{dims[1]:.1f}×{dims[2]:.1f}",
                    f"({com[0]:.1f}, {com[1]:.1f}, {com[2]:.1f})",
                    f"{model['volume']:.1f}"
                )
            
            self.console.print(table)
            
            # Quality analysis
            self.console.print(f"\n[bold cyan]🔧 Mesh Quality Analysis[/bold cyan]")
            quality_table = Table(title="Mesh Quality")
            quality_table.add_column("Model ID", style="cyan")
            quality_table.add_column("Valid", style="green")
            quality_table.add_column("Degenerate Triangles", style="red")
            quality_table.add_column("Edges", style="blue")
            quality_table.add_column("Surface Area (mm²)", style="yellow")
            
            for model in analysis['models']:
                quality = model['quality']
                quality_table.add_row(
                    str(model['object_id']),
                    "✅ Yes" if quality['valid'] else "❌ No",
                    str(quality['degenerate_triangles']),
                    str(quality['edge_count']),
                    f"{model['surface_area']:.1f}"
                )
            
            self.console.print(quality_table)
    
    def export_analysis(self, analysis: Dict[str, Any], output_path: Path):
        """Export analysis results to JSON file."""
        try:
            with open(output_path, 'w') as f:
                json.dump(analysis, f, indent=2)
            self.console.print(f"[green]Analysis exported to: {output_path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Failed to export analysis: {e}[/red]")
    
    def compare_3mf_files(self, file_paths: List[Path]):
        """Compare multiple 3MF files."""
        self.console.print("[bold magenta]🔍 3MF File Comparison[/bold magenta]")
        
        analyses = []
        for file_path in file_paths:
            if file_path.exists():
                analysis = self.analyze_3mf_file(file_path)
                if 'error' not in analysis:
                    analyses.append(analysis)
                else:
                    self.console.print(f"[red]Skipping {file_path.name}: {analysis['error']}[/red]")
        
        if not analyses:
            self.console.print("[yellow]No valid files to compare[/yellow]")
            return
        
        # Comparison table
        table = Table(title="3MF File Comparison")
        table.add_column("File", style="cyan")
        table.add_column("Objects", style="magenta")
        table.add_column("Vertices", style="green")
        table.add_column("Triangles", style="yellow")
        table.add_column("File Size", style="blue")
        table.add_column("Dimensions", style="red")
        
        for analysis in analyses:
            file_name = Path(analysis['file_path']).name
            summary = analysis['summary']
            dims = summary.get('overall_dimensions', [0, 0, 0])
            
            table.add_row(
                file_name,
                str(summary['object_count']),
                f"{summary['total_vertices']:,}",
                f"{summary['total_triangles']:,}",
                f"{analysis['file_size']:,} bytes",
                f"{dims[0]:.1f}×{dims[1]:.1f}×{dims[2]:.1f}"
            )
        
        self.console.print(table)


def analyze_3mf_file(file_path: Path, detailed: bool = True, export_json: bool = False) -> Dict[str, Any]:
    """
    Convenience function to analyze a 3MF file.
    
    Args:
        file_path: Path to the 3MF file
        detailed: Whether to print detailed analysis
        export_json: Whether to export results to JSON
        
    Returns:
        Analysis results dictionary
    """
    analyzer = Model3MFAnalyzer()
    analysis = analyzer.analyze_3mf_file(file_path)
    
    if detailed:
        analyzer.print_analysis(analysis)
    
    if export_json and 'error' not in analysis:
        json_path = file_path.with_suffix('.json')
        analyzer.export_analysis(analysis, json_path)
    
    return analysis


if __name__ == "__main__":
    console = Console()
    console.print("[bold blue]🔍 3MF File Analyzer[/bold blue]")
    
    # Find 3MF files to analyze
    current_dir = Path(".")
    mf_files = list(current_dir.glob("*.3mf"))
    
    if not mf_files:
        console.print("[yellow]No 3MF files found in current directory[/yellow]")
        console.print("[yellow]Run the grid examples first to create some 3MF files[/yellow]")
    else:
        analyzer = Model3MFAnalyzer()
        
        # Analyze each file
        for mf_file in sorted(mf_files)[:3]:  # Limit to first 3 files
            console.print(f"\n{'='*60}")
            analysis = analyzer.analyze_3mf_file(mf_file)
            analyzer.print_analysis(analysis, detailed=True)
        
        # Compare all files
        if len(mf_files) > 1:
            console.print(f"\n{'='*60}")
            analyzer.compare_3mf_files(mf_files)
