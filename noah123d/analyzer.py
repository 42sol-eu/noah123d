"""3MF file analysis utilities for the noah123d package."""

from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from .archive3mf import Archive3mf
from .directory import Directory
from .model import Model


class Analysis3MF:
    """3MF file analyzer for extracting model information."""
    
    def __init__(self):
        """Initialize the analyzer."""
        pass
    
    def analyze_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Analyze a 3MF file and extract model information.
        
        Args:
            file_path: Path to the 3MF file
            
        Returns:
            Dictionary containing analysis results
        """
        file_path = Path(file_path)  # Convert to Path object
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
                contents = archive.list_contents()
                analysis['archive_contents'] = contents
                
                with Directory('3D') as models_dir:
                    with Model() as model:
                        object_count = model.get_object_count()
                        analysis['summary']['object_count'] = object_count
                        
                        if object_count == 0:
                            return analysis
                        
                        total_vertices = 0
                        total_triangles = 0
                        all_vertices = []
                        
                        for obj_id in model.list_objects():
                            obj = model.get_object(obj_id)
                            if obj:
                                obj_analysis = self._analyze_object(obj, obj_id)
                                analysis['models'].append(obj_analysis)
                                
                                total_vertices += len(obj['vertices'])
                                total_triangles += len(obj['triangles'])
                                all_vertices.extend(obj['vertices'])
                        
                        # Overall statistics
                        analysis['summary'].update({
                            'total_vertices': total_vertices,
                            'total_triangles': total_triangles,
                            'overall_bounds': self._calculate_bounds(all_vertices),
                            'overall_center_of_mass': self._calculate_center_of_mass(all_vertices)
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
        """Analyze a single object."""
        vertices = obj['vertices']
        triangles = obj['triangles']
        
        bounds = self._calculate_bounds(vertices)
        dimensions = [
            bounds['max'][0] - bounds['min'][0],
            bounds['max'][1] - bounds['min'][1],
            bounds['max'][2] - bounds['min'][2]
        ]
        center_of_mass = self._calculate_center_of_mass(vertices)
        volume = self._calculate_volume(vertices, triangles)
        surface_area = self._calculate_surface_area(vertices, triangles)
        
        return {
            'object_id': obj_id,
            'object_type': obj.get('type', 'model'),
            'vertex_count': len(vertices),
            'triangle_count': len(triangles),
            'bounds': bounds,
            'dimensions': dimensions,
            'center_of_mass': center_of_mass,
            'volume': volume,
            'surface_area': surface_area
        }
    
    def _calculate_bounds(self, vertices: List[List[float]]) -> Dict[str, List[float]]:
        """Calculate bounding box."""
        if not vertices:
            return {'min': [0, 0, 0], 'max': [0, 0, 0]}
        
        min_coords = [min(v[i] for v in vertices) for i in range(3)]
        max_coords = [max(v[i] for v in vertices) for i in range(3)]
        
        return {'min': min_coords, 'max': max_coords}
    
    def _calculate_center_of_mass(self, vertices: List[List[float]]) -> List[float]:
        """Calculate center of mass."""
        if not vertices:
            return [0, 0, 0]
        
        return [sum(v[i] for v in vertices) / len(vertices) for i in range(3)]
    
    def _calculate_volume(self, vertices: List[List[float]], triangles: List[List[int]]) -> float:
        """Calculate mesh volume."""
        if not triangles or not vertices:
            return 0.0
        
        volume = 0.0
        for triangle in triangles:
            if len(triangle) >= 3:
                try:
                    v1, v2, v3 = [vertices[triangle[i]] for i in range(3)]
                    volume += (v1[0] * (v2[1] * v3[2] - v2[2] * v3[1]) +
                              v2[0] * (v3[1] * v1[2] - v3[2] * v1[1]) +
                              v3[0] * (v1[1] * v2[2] - v1[2] * v2[1])) / 6.0
                except (IndexError, TypeError):
                    continue
        
        return abs(volume)
    
    def _calculate_surface_area(self, vertices: List[List[float]], triangles: List[List[int]]) -> float:
        """Calculate surface area."""
        if not triangles or not vertices:
            return 0.0
        
        import math
        total_area = 0.0
        
        for triangle in triangles:
            if len(triangle) >= 3:
                try:
                    v1, v2, v3 = [vertices[triangle[i]] for i in range(3)]
                    
                    edge1 = [v2[i] - v1[i] for i in range(3)]
                    edge2 = [v3[i] - v1[i] for i in range(3)]
                    
                    cross = [
                        edge1[1] * edge2[2] - edge1[2] * edge2[1],
                        edge1[2] * edge2[0] - edge1[0] * edge2[2],
                        edge1[0] * edge2[1] - edge1[1] * edge2[0]
                    ]
                    
                    area = 0.5 * math.sqrt(sum(c**2 for c in cross))
                    total_area += area
                    
                except (IndexError, TypeError, ValueError):
                    continue
        
        return total_area
    
    def get_model_info(self, file_path: Path, model_id: int = None) -> Optional[Dict[str, Any]]:
        """Get information for a specific model or all models."""
        analysis = self.analyze_file(file_path)
        
        if 'error' in analysis:
            return None
            
        if model_id is None:
            return analysis
            
        for model in analysis['models']:
            if model['object_id'] == model_id:
                return model
                
        return None


def analyze_3mf(file_path: Path) -> Dict[str, Any]:
    """
    Convenience function to analyze a 3MF file.
    
    Args:
        file_path: Path to the 3MF file
        
    Returns:
        Analysis results dictionary
    """
    analyzer = Analysis3MF()
    return analyzer.analyze_file(file_path)


def get_model_center_of_mass(file_path: Path, model_id: int = None) -> Optional[List[float]]:
    """
    Get center of mass for a model in a 3MF file.
    
    Args:
        file_path: Path to the 3MF file
        model_id: Specific model ID (None for overall center of mass)
        
    Returns:
        Center of mass coordinates [x, y, z] or None if not found
    """
    analyzer = Analysis3MF()
    analysis = analyzer.analyze_file(file_path)
    
    if 'error' in analysis:
        return None
    
    if model_id is None:
        return analysis['summary'].get('overall_center_of_mass')
    
    for model in analysis['models']:
        if model['object_id'] == model_id:
            return model['center_of_mass']
    
    return None


def get_model_dimensions(file_path: Path, model_id: int = None) -> Optional[List[float]]:
    """
    Get dimensions for a model in a 3MF file.
    
    Args:
        file_path: Path to the 3MF file
        model_id: Specific model ID (None for overall dimensions)
        
    Returns:
        Dimensions [width, height, depth] or None if not found
    """
    analyzer = Analysis3MF()
    analysis = analyzer.analyze_file(file_path)
    
    if 'error' in analysis:
        return None
    
    if model_id is None:
        return analysis['summary'].get('overall_dimensions')
    
    for model in analysis['models']:
        if model['object_id'] == model_id:
            return model['dimensions']
    
    return None
