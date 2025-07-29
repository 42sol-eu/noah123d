"""STL to 3MF converter utilities for the noah123d package."""

from pathlib import Path
from typing import Optional, Union, List, Dict, Any
import glob
from .archive3mf import Archive3mf
from .directory import Directory
from .model import Model


class STLConverter:
    """STL to 3MF converter with advanced features."""
    
    def __init__(self, include_metadata: bool = True, 
                 compress: bool = True, 
                 validate: bool = True):
        """
        Initialize the STL converter.
        
        Args:
            include_metadata: Include conversion metadata in 3MF files
            compress: Enable compression for 3MF files (not yet implemented)
            validate: Validate STL files before conversion
        """
        self.include_metadata = include_metadata
        self.compress = compress
        self.validate = validate
        self.conversion_stats = {}
    
    def convert(self, stl_path: Union[str, Path], 
                output_path: Union[str, Path]) -> bool:
        """
        Convert an STL file to 3MF format.
        
        Args:
            stl_path: Path to the input STL file
            output_path: Path for the output 3MF file
            
        Returns:
            True if conversion was successful, False otherwise
        """
        try:
            stl_path = Path(stl_path)
            output_path = Path(output_path)
            
            if not stl_path.exists():
                raise FileNotFoundError(f"STL file not found: {stl_path}")
            
            if self.validate:
                self._validate_stl(stl_path)
            
            # Track conversion start
            import time
            start_time = time.time()
            
            # Create the 3MF archive
            with Archive3mf(output_path, 'w') as archive:
                # Create the 3D directory
                with Directory('3D') as models_dir:
                    # Create a model and add the STL
                    with Model() as model:
                        # Add the STL object to the model
                        obj_id = model.add_object_from_stl(stl_path)
                        
                        # Get object statistics
                        obj = model.get_object(obj_id)
                        stats = self._calculate_stats(obj, stl_path, start_time)
                        
                        if self.include_metadata:
                            self._add_metadata(stats, output_path)
                        
                        # Store conversion statistics
                        self.conversion_stats[str(output_path)] = stats
            
            return True
            
        except Exception as e:
            self.conversion_stats[str(output_path)] = {'error': str(e)}
            return False
    
    def convert_with_copies(self, stl_path: Union[str, Path], 
                           output_path: Union[str, Path],
                           count: int = 1,
                           grid_cols: Optional[int] = None,
                           spacing_factor: float = 1.1,
                           center_grid: bool = True) -> bool:
        """
        Convert an STL file to 3MF format with multiple copies arranged in a grid.
        
        Args:
            stl_path: Path to the input STL file
            output_path: Path for the output 3MF file
            count: Total number of copies to create
            grid_cols: Number of columns in the grid (auto-calculated if None)
            spacing_factor: Multiplier for object spacing (1.0 = touching, 1.1 = 10% gap)
            center_grid: Whether to center the grid around the origin
            
        Returns:
            True if conversion was successful, False otherwise
        """
        try:
            stl_path = Path(stl_path)
            output_path = Path(output_path)
            
            if not stl_path.exists():
                raise FileNotFoundError(f"STL file not found: {stl_path}")
            
            if self.validate:
                self._validate_stl(stl_path)
            
            # Track conversion start
            import time
            start_time = time.time()
            
            # Get STL info to calculate dimensions
            stl_info = self.get_stl_info(stl_path)
            if not stl_info or 'error' in stl_info:
                raise ValueError("Could not analyze STL file for grid placement")
            
            dimensions = stl_info['dimensions']
            bounding_box = stl_info['bounding_box']
            
            # Calculate grid layout
            grid_layout = self._calculate_grid_layout(count, grid_cols)
            positions = self._calculate_grid_positions(
                grid_layout, dimensions, spacing_factor, center_grid, bounding_box, count
            )
            
            # Create the 3MF archive
            with Archive3mf(output_path, 'w') as archive:
                # Create the 3D directory
                with Directory('3D') as models_dir:
                    # Create a model and add multiple copies
                    with Model() as model:
                        # Load the STL and get object data
                        master_obj_id = model.add_object_from_stl(stl_path)
                        master_obj = model.get_object(master_obj_id)
                        
                        # Remove the original object since we'll place all objects at calculated positions
                        model.remove_object(master_obj_id)
                        
                        # Create objects at calculated positions
                        for i, position in enumerate(positions):
                            # Create translated copy for each position (including the first one)
                            translated_vertices = self._translate_vertices(
                                master_obj['vertices'], position
                            )
                            model.add_object(translated_vertices, master_obj['triangles'])
                        
                        # Calculate combined statistics
                        total_vertices = len(master_obj['vertices']) * count
                        total_triangles = len(master_obj['triangles']) * count
                        
                        stats = {
                            'source_file': str(stl_path),
                            'source_size': stl_path.stat().st_size,
                            'vertices': total_vertices,
                            'triangles': total_triangles,
                            'conversion_time': time.time() - start_time,
                            'timestamp': time.time(),
                            'copies': count,
                            'grid_layout': grid_layout,
                            'spacing_factor': spacing_factor
                        }
                        
                        if self.include_metadata:
                            self._add_grid_metadata(stats, output_path, positions)
                        
                        # Store conversion statistics
                        self.conversion_stats[str(output_path)] = stats
            
            return True
            
        except Exception as e:
            self.conversion_stats[str(output_path)] = {'error': str(e)}
            return False
    
    def batch_convert(self, input_pattern: str, 
                     output_dir: Union[str, Path] = "converted",
                     preserve_structure: bool = False) -> List[str]:
        """
        Convert multiple STL files matching a pattern to 3MF format.
        
        Args:
            input_pattern: Glob pattern for STL files (e.g., "models/*.stl")
            output_dir: Directory to save converted 3MF files
            preserve_structure: Preserve directory structure in output
            
        Returns:
            List of successfully converted file paths
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        stl_files = glob.glob(input_pattern, recursive=True)
        converted_files = []
        
        for stl_file in stl_files:
            stl_path = Path(stl_file)
            
            if preserve_structure:
                # Preserve relative directory structure
                relative_path = stl_path.relative_to(Path(input_pattern).parent)
                output_path = output_dir / relative_path.with_suffix('.3mf')
                output_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                output_path = output_dir / f"{stl_path.stem}.3mf"
            
            if self.convert(stl_path, output_path):
                converted_files.append(str(output_path))
        
        return converted_files
    
    def get_stl_info(self, stl_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about an STL file.
        
        Args:
            stl_path: Path to the STL file
            
        Returns:
            Dictionary with STL file information, or None if file cannot be read
        """
        try:
            from stl import mesh
            
            stl_path = Path(stl_path)
            if not stl_path.exists():
                return None
            
            stl_mesh = mesh.Mesh.from_file(str(stl_path))
            
            # Calculate unique vertices
            vertices = set()
            triangle_count = len(stl_mesh.vectors)
            
            for triangle in stl_mesh.vectors:
                for vertex in triangle:
                    vertices.add(tuple(vertex))
            
            # Calculate volume and surface area
            volume, cog, inertia = stl_mesh.get_mass_properties()
            
            return {
                'file_path': str(stl_path),
                'file_size': stl_path.stat().st_size,
                'triangles': triangle_count,
                'unique_vertices': len(vertices),
                'total_vertices': triangle_count * 3,
                'volume': volume,
                'center_of_gravity': cog.tolist(),
                'bounding_box': {
                    'min': stl_mesh.min_.tolist(),
                    'max': stl_mesh.max_.tolist()
                },
                'dimensions': (stl_mesh.max_ - stl_mesh.min_).tolist(),
                'surface_area': self._calculate_surface_area(stl_mesh),
                'is_valid': self._validate_mesh(stl_mesh)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_conversion_stats(self) -> Dict[str, Any]:
        """Get statistics from recent conversions."""
        return self.conversion_stats.copy()
    
    def clear_stats(self):
        """Clear conversion statistics."""
        self.conversion_stats.clear()
    
    def _validate_stl(self, stl_path: Path):
        """Validate STL file before conversion."""
        if stl_path.stat().st_size == 0:
            raise ValueError("STL file is empty")
        
        # Additional validation could be added here
        info = self.get_stl_info(stl_path)
        if info and 'error' in info:
            raise ValueError(f"Invalid STL file: {info['error']}")
    
    def _validate_mesh(self, stl_mesh) -> bool:
        """Validate mesh geometry."""
        try:
            # Check for degenerate triangles
            for triangle in stl_mesh.vectors:
                # Calculate triangle area
                v1, v2, v3 = triangle
                area = 0.5 * abs((v2[0] - v1[0]) * (v3[1] - v1[1]) - 
                                (v3[0] - v1[0]) * (v2[1] - v1[1]))
                if area < 1e-10:  # Very small area threshold
                    return False
            return True
        except:
            return False
    
    def _calculate_surface_area(self, stl_mesh) -> float:
        """Calculate surface area of the mesh."""
        import numpy as np
        
        total_area = 0.0
        for triangle in stl_mesh.vectors:
            v1, v2, v3 = triangle
            # Calculate triangle area using cross product
            edge1 = v2 - v1
            edge2 = v3 - v1
            cross = np.cross(edge1, edge2)
            area = 0.5 * np.linalg.norm(cross)
            total_area += area
        
        return total_area
    
    def _calculate_grid_layout(self, count: int, grid_cols: Optional[int] = None) -> tuple:
        """Calculate optimal grid layout (rows, cols) for given count."""
        import math
        
        if grid_cols is None:
            # Calculate optimal square-ish grid
            grid_cols = math.ceil(math.sqrt(count))
        
        grid_rows = math.ceil(count / grid_cols)
        return (grid_rows, grid_cols)
    
    def _calculate_grid_positions(self, grid_layout: tuple, dimensions: List[float], 
                                 spacing_factor: float, center_grid: bool,
                                 bounding_box: Dict[str, List[float]], count: int) -> List[List[float]]:
        """Calculate positions for objects in a grid layout."""
        rows, cols = grid_layout
        positions = []
        
        # Calculate spacing between objects
        x_spacing = dimensions[0] * spacing_factor
        y_spacing = dimensions[1] * spacing_factor
        
        # Calculate grid dimensions
        total_width = (cols - 1) * x_spacing
        total_height = (rows - 1) * y_spacing
        
        # Calculate starting position (center grid if requested)
        if center_grid:
            start_x = -total_width / 2
            start_y = -total_height / 2
        else:
            start_x = 0
            start_y = 0
        
        # Generate positions
        for row in range(rows):
            for col in range(cols):
                if len(positions) >= count:  # Stop when we have enough positions
                    break
                    
                x = start_x + col * x_spacing
                y = start_y + row * y_spacing
                z = 0  # Keep all objects at the same Z level
                
                # Don't adjust for bounding box here - the STL is already properly positioned
                # The adjustment will be done consistently in the object creation logic
                
                positions.append([x, y, z])
            
            if len(positions) >= count:  # Break outer loop too
                break
                
        return positions
    
    def _translate_vertices(self, vertices: List[List[float]], 
                           translation: List[float]) -> List[List[float]]:
        """Translate vertices by the given translation vector."""
        return [
            [v[0] + translation[0], v[1] + translation[1], v[2] + translation[2]]
            for v in vertices
        ]
    
    def _translate_object(self, obj: Dict[str, Any], translation: List[float]):
        """Translate an object's vertices in place."""
        for i, vertex in enumerate(obj['vertices']):
            obj['vertices'][i] = [
                vertex[0] + translation[0],
                vertex[1] + translation[1], 
                vertex[2] + translation[2]
            ]
    
    def _calculate_stats(self, obj: Dict[str, Any], stl_path: Path, 
                        start_time: float) -> Dict[str, Any]:
        """Calculate conversion statistics."""
        import time
        
        end_time = time.time()
        conversion_time = end_time - start_time
        
        stats = {
            'source_file': str(stl_path),
            'source_size': stl_path.stat().st_size,
            'vertices': len(obj['vertices']) if obj else 0,
            'triangles': len(obj['triangles']) if obj else 0,
            'conversion_time': conversion_time,
            'timestamp': end_time
        }
        
        return stats
    
    def _add_metadata(self, stats: Dict[str, Any], output_path: Path):
        """Add conversion metadata to the 3MF file."""
        with Directory('Metadata') as metadata_dir:
            metadata_content = f"""STL to 3MF Conversion Report
Generated by: Noah123d STL Converter v2025.0.1
Date: {Path(__file__).stat().st_mtime}

Source Information:
- File: {Path(stats['source_file']).name}
- Size: {stats['source_size']:,} bytes

Output Information:
- File: {output_path.name}
- Vertices: {stats['vertices']:,}
- Triangles: {stats['triangles']:,}

Performance:
- Conversion Time: {stats['conversion_time']:.3f} seconds
- Triangles/Second: {stats['triangles'] / stats['conversion_time']:,.0f}

Conversion successful!
"""
            metadata_dir.create_file('conversion_report.txt', metadata_content)
    
    def _add_grid_metadata(self, stats: Dict[str, Any], output_path: Path, 
                          positions: List[List[float]]):
        """Add grid conversion metadata to the 3MF file."""
        with Directory('Metadata') as metadata_dir:
            metadata_content = f"""STL to 3MF Grid Conversion Report
Generated by: Noah123d STL Converter v2025.0.1
Date: {Path(__file__).stat().st_mtime}

Source Information:
- File: {Path(stats['source_file']).name}
- Size: {stats['source_size']:,} bytes

Grid Configuration:
- Copies: {stats['copies']}
- Grid Layout: {stats['grid_layout'][0]} rows × {stats['grid_layout'][1]} columns
- Spacing Factor: {stats['spacing_factor']:.2f}

Output Information:
- File: {output_path.name}
- Total Vertices: {stats['vertices']:,}
- Total Triangles: {stats['triangles']:,}
- Objects in Build: {len(positions)}

Performance:
- Conversion Time: {stats['conversion_time']:.3f} seconds
- Triangles/Second: {stats['triangles'] / stats['conversion_time']:,.0f}

Object Positions:
"""
            
            for i, pos in enumerate(positions):
                metadata_content += f"- Object {i+1}: X={pos[0]:.2f}, Y={pos[1]:.2f}, Z={pos[2]:.2f}\n"
            
            metadata_content += "\nGrid conversion successful!"
            
            metadata_dir.create_file('grid_conversion_report.txt', metadata_content)


# Convenience functions for backward compatibility and simple usage
def stl_to_3mf(stl_path: Union[str, Path], output_path: Union[str, Path], 
               include_metadata: bool = True) -> bool:
    """
    Simple function to convert an STL file to 3MF format.
    
    Args:
        stl_path: Path to the input STL file
        output_path: Path for the output 3MF file
        include_metadata: Whether to include conversion metadata
        
    Returns:
        True if conversion was successful, False otherwise
    """
    converter = STLConverter(include_metadata=include_metadata)
    return converter.convert(stl_path, output_path)


def get_stl_info(stl_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
    """
    Get information about an STL file.
    
    Args:
        stl_path: Path to the STL file
        
    Returns:
        Dictionary with STL file information, or None if file cannot be read
    """
    converter = STLConverter()
    return converter.get_stl_info(stl_path)


def batch_stl_to_3mf(input_pattern: str, output_dir: Union[str, Path] = "converted",
                     include_metadata: bool = True) -> List[str]:
    """
    Convert multiple STL files matching a pattern to 3MF format.
    
    Args:
        input_pattern: Glob pattern for STL files (e.g., "models/*.stl")
        output_dir: Directory to save converted 3MF files
        include_metadata: Whether to include conversion metadata
        
    Returns:
        List of successfully converted file paths
    """
    converter = STLConverter(include_metadata=include_metadata)
    return converter.batch_convert(input_pattern, output_dir)


def stl_to_3mf_grid(stl_path: Union[str, Path], output_path: Union[str, Path],
                    count: int = 1, grid_cols: Optional[int] = None,
                    spacing_factor: float = 1.1, center_grid: bool = True,
                    include_metadata: bool = True) -> bool:
    """
    Convert an STL file to 3MF format with multiple copies in a grid layout.
    
    Args:
        stl_path: Path to the input STL file
        output_path: Path for the output 3MF file
        count: Total number of copies to create
        grid_cols: Number of columns in the grid (auto-calculated if None)
        spacing_factor: Multiplier for object spacing (1.0 = touching, 1.1 = 10% gap)
        center_grid: Whether to center the grid around the origin
        include_metadata: Whether to include conversion metadata
        
    Returns:
        True if conversion was successful, False otherwise
        
    Example:
        >>> # Create a 2x2 grid of parts with 20% spacing
        >>> success = stl_to_3mf_grid("part.stl", "grid.3mf", count=4, 
        ...                          grid_cols=2, spacing_factor=1.2)
    """
    converter = STLConverter(include_metadata=include_metadata)
    return converter.convert_with_copies(stl_path, output_path, count, 
                                       grid_cols, spacing_factor, center_grid)
