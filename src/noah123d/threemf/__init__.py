# -*- coding: utf-8 -*-
"""
3mf (called threemf because of Python naming conventions) package for noah123d — shared parameters and base classes.
----
file:
    name:       __init__.py
    uuid:       57345d9c-5ecb-446d-b186-f425738c90ec
description:    3mf package for noah123d — shared parameters and base classes.
authors:         felix@42sol.eu
project:
    name:       noah123d
    uuid:       93fe70d7-2d29-4ebf-bf0e-51d75dbfda30
    url:        https://github.com/42sol-eu/noah123d
"""

# [[[cog
# import sys
# from pathlib import Path
# sys.path.insert(0, str(Path(cog.inFile).parent.parent.parent.parent / "a7d"))
# from cog_helpers import generate_subpackage_imports_and_all
# content = generate_subpackage_imports_and_all(str(Path(cog.inFile).parent), group_by_file=True)
# cog.out(content)
# ]]]
from .analyzer import (
    Analyzer,
    analyze_3mf,
    get_model_center_of_mass,
    get_model_dimensions,
)
from .archive import (
    Archive,
    add_file,
    current_archive,
    extract_file,
    get_temp_path,
    is_writable,
    list_contents,
)
from .directory import (
    Directory,
    create_file,
    current_directory,
    delete_file,
    list_files,
    list_subdirectories,
    read_file,
)
from .metadata import (
    Metadata,
    add_conversion_info,
    add_custom_metadata,
    add_properties,
)
from .model import (
    Model,
    add_conversion_metadata,
    add_object,
    add_object_from_stl,
    analyze_model_content,
    clear_objects,
    current_model,
    get_object,
    get_object_count,
    list_objects,
    load_stl_with_info,
    remove_object,
)
from .textures import (
    Textures,
    add_texture,
    get_texture_metadata,
    list_texture_files,
)
from .three_d import (
    ThreeD,
    add_thumbnail,
    create_model_file,
    list_model_files,
)
from .xml_3mf import content_types_header, relationships_header

__all__ = [
    # From src/noah123d/threemf/metadata.py
    "add_conversion_info",
    "add_custom_metadata",
    "add_properties",
    "Metadata",

    # From src/noah123d/threemf/analyzer.py
    "analyze_3mf",
    "Analyzer",
    "get_model_center_of_mass",
    "get_model_dimensions",

    # From src/noah123d/threemf/model.py
    "add_conversion_metadata",
    "add_object",
    "add_object_from_stl",
    "analyze_model_content",
    "clear_objects",
    "current_model",
    "get_object",
    "get_object_count",
    "list_objects",
    "load_stl_with_info",
    "Model",
    "remove_object",

    # From src/noah123d/threemf/archive.py
    "add_file",
    "Archive",
    "current_archive",
    "extract_file",
    "get_temp_path",
    "is_writable",
    "list_contents",

    # From src/noah123d/threemf/directory.py
    "create_file",
    "current_directory",
    "delete_file",
    "Directory",
    "list_files",
    "list_subdirectories",
    "read_file",

    # From src/noah123d/threemf/three_d.py
    "add_thumbnail",
    "create_model_file",
    "list_model_files",
    "ThreeD",

    # From src/noah123d/threemf/xml_3mf.py
    "content_types_header",
    "relationships_header",

    # From src/noah123d/threemf/textures.py
    "add_texture",
    "get_texture_metadata",
    "list_texture_files",
    "Textures",
]
# [[[end]]] (sum: RrPFmiWvRZ)
