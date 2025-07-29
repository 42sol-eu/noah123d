"""Noah123D - Building assemblies from STL models."""

__version__ = "2025.0.1"

from .__main__ import main
from .archive3mf import Archive3mf
from .directory import Directory
from .model import Model
from .converters import STLConverter, stl_to_3mf, get_stl_info, batch_stl_to_3mf, stl_to_3mf_grid
from .analyzer import Analysis3MF, analyze_3mf, get_model_center_of_mass, get_model_dimensions

__all__ = [
    "main", 
    "Archive3mf", 
    "Directory", 
    "Model",
    "STLConverter",
    "stl_to_3mf",
    "get_stl_info", 
    "batch_stl_to_3mf",
    "stl_to_3mf_grid",
    "Analysis3MF",
    "analyze_3mf",
    "get_model_center_of_mass",
    "get_model_dimensions"
]
