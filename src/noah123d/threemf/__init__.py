
from .directory import (
    Directory,
    create_file,
    read_file,
    delete_file,
    list_files,
    list_subdirectories,
)

from .three_d import ThreeD, add_thumbnail, create_model_file, list_model_files

from .metadata import (
    Metadata,
    add_conversion_info,
    add_properties,
    add_custom_metadata,
    # TODO: add context aware functions
)
from .textures import (
    Textures,
    # TODO: add context aware functions
)

from .model import (
    Model,
    add_object, 
    add_object_from_stl, 
    list_objects, 
    get_object,
    get_object_count, 
    clear_objects,
    remove_object,
)

from .archive import (
    Archive,
    list_contents,
    extract_file,
    add_file,
    get_temp_path,
    is_writable,
)

from .analyzer import Analyzer, analyze_3mf

__all__ = [
    "Directory",
    "ThreeD",
    "Metadata",
    "Textures",
    "Model",
    "Archive",
    "Analyzer",
    "analyze_3mf",
]