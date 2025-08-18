# -*- coding: utf-8 -*-
"""
Main package for noah123d.
----
file:
    name:       __init__.py
    uuid:       auto-generated
description:    Main package for noah123d
authors:         felix@42sol.eu
project:
    name:       noah123d
    uuid:       93fe70d7-2d29-4ebf-bf0e-51d75dbfda30
    url:        https://github.com/42sol-eu/noah123d
"""

# [[[cog
# import sys
# from pathlib import Path
# # Use absolute path to ensure a7d is found regardless of working directory
# project_root = Path(cog.inFile).resolve().parent.parent.parent
# sys.path.insert(0, str(project_root / "a7d"))
# from cog_helpers import generate_main_package_imports_and_all
# content = generate_main_package_imports_and_all(str(Path(cog.inFile).parent), group_by_file=True, update_first=True)
# cog.out(content)
# ]]]
from .__main__ import (
    G_all_models,
    center_model_origin,
    console,
    load_model,
    main,
    move_model_origin,
    process_model,
    show_mesh_bounds,
)
from .converters import (
    STLConverter,
    batch_stl_to_3mf,
    get_stl_info,
    multi_stl_to_3mf,
    stl_to_3mf,
    stl_to_3mf_grid,
)
from .core import (
    BaseModel,
    Log,
    ModelParameters,
    auto_context_function_with_checks,
    context_function,
    context_function_with_check,
    mm,
    no,
    yes,
)
from .tasks import create_empty_3mf
from .threemf import (
    Analyzer,
    Archive,
    Directory,
    Metadata,
    Model,
    Textures,
    ThreeD,
    add_conversion_info,
    add_conversion_metadata,
    add_custom_metadata,
    add_file,
    add_object,
    add_object_from_stl,
    add_properties,
    add_texture,
    add_thumbnail,
    analyze_3mf,
    analyze_model_content,
    clear_objects,
    content_types_header,
    create_file,
    create_model_file,
    current_archive,
    current_directory,
    current_model,
    delete_file,
    extract_file,
    get_model_center_of_mass,
    get_model_dimensions,
    get_object,
    get_object_count,
    get_temp_path,
    get_texture_metadata,
    is_writable,
    list_contents,
    list_files,
    list_model_files,
    list_objects,
    list_subdirectories,
    list_texture_files,
    load_stl_with_info,
    read_file,
    relationships_header,
    remove_object,
)
from .visual import (
    ColorMapHelper,
    Console,
    ViewerHelper,
    print_archive_contents,
    print_assembly_totals,
    print_error,
    print_file_info,
    print_file_not_found,
    print_metadata_files,
    print_model_analysis,
    print_object_table,
    setup_viewer,
)

__all__ = [
    #
    # from noah123d/tasks.py
    "create_empty_3mf",
    #
    # from noah123d/converters.py
    "batch_stl_to_3mf",
    "get_stl_info",
    "multi_stl_to_3mf",
    "stl_to_3mf",
    "stl_to_3mf_grid",
    "STLConverter",
    #
    # from noah123d/__main__.py
    "center_model_origin",
    "console",
    "G_all_models",
    "load_model",
    "main",
    "move_model_origin",
    "process_model",
    "show_mesh_bounds",
    #
    # from noah123d/core/__init__.py
    "auto_context_function_with_checks",
    "BaseModel",
    "context_function",
    "context_function_with_check",
    "Log",
    "mm",
    "ModelParameters",
    "no",
    "yes",
    #
    # from noah123d/threemf/__init__.py
    "add_conversion_info",
    "add_conversion_metadata",
    "add_custom_metadata",
    "add_file",
    "add_object",
    "add_object_from_stl",
    "add_properties",
    "add_texture",
    "add_thumbnail",
    "analyze_3mf",
    "analyze_model_content",
    "Analyzer",
    "Archive",
    "clear_objects",
    "content_types_header",
    "create_file",
    "create_model_file",
    "current_archive",
    "current_directory",
    "current_model",
    "delete_file",
    "Directory",
    "extract_file",
    "get_model_center_of_mass",
    "get_model_dimensions",
    "get_object",
    "get_object_count",
    "get_temp_path",
    "get_texture_metadata",
    "is_writable",
    "list_contents",
    "list_files",
    "list_model_files",
    "list_objects",
    "list_subdirectories",
    "list_texture_files",
    "load_stl_with_info",
    "Metadata",
    "Model",
    "read_file",
    "relationships_header",
    "remove_object",
    "Textures",
    "ThreeD",
    #
    # from noah123d/visual/__init__.py
    "ColorMapHelper",
    "Console",
    "print_archive_contents",
    "print_assembly_totals",
    "print_error",
    "print_file_info",
    "print_file_not_found",
    "print_metadata_files",
    "print_model_analysis",
    "print_object_table",
    "setup_viewer",
    "ViewerHelper",
]
# [[[end]]] (sum: 7hL9LN1czy)
