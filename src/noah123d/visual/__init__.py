# -*- coding: utf-8 -*-
"""
Visual package for noah123d — visualization and console utilities.
----
file:
    name:       __init__.py
    uuid:       8d7e9f2a-4b3c-456d-8e90-1f2a3b4c5d6e
description:    Visual package for noah123d — visualization and console utilities.
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
# project_root = Path(cog.inFile).resolve().parent.parent.parent.parent
# sys.path.insert(0, str(project_root / "a7d"))
# from cog_helpers import generate_subpackage_imports_and_all
# content = generate_subpackage_imports_and_all(str(Path(cog.inFile).parent), group_by_file=True)
# cog.out(content)
# ]]]
from .colormap_helper import ColorMapHelper
from .console import (
    Console,
    print_archive_contents,
    print_assembly_totals,
    print_error,
    print_file_info,
    print_file_not_found,
    print_metadata_files,
    print_model_analysis,
    print_object_table,
)
from .viewer import ViewerHelper, setup_viewer

__all__ = [
    # From src/noah123d/visual/console.py
    "Console",
    "print_archive_contents",
    "print_assembly_totals",
    "print_error",
    "print_file_info",
    "print_file_not_found",
    "print_metadata_files",
    "print_model_analysis",
    "print_object_table",

    # From src/noah123d/visual/viewer.py
    "setup_viewer",
    "ViewerHelper",

    # From src/noah123d/visual/colormap_helper.py
    "ColorMapHelper",
]
# [[[end]]] (sum: ikTajX8xkM)
