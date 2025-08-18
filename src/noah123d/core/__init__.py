# -*- coding: utf-8 -*-
"""
Core package for noah123d — shared parameters and base classes.
----
file:
    name:       __init__.py
    uuid:       7f8dd612-44b2-41ad-9049-7133096fb44f
description:    Core package for noah123d — shared parameters and base classes.
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
from .constants import mm, no, yes
from .context_decorators import auto_context_function_with_checks, context_function, context_function_with_check
from .logging import Log
from .model import BaseModel
from .parameters import ModelParameters

__all__ = [
    # From src/noah123d/core/logging.py
    "Log",

    # From src/noah123d/core/constants.py
    "mm",
    "no",
    "yes",

    # From src/noah123d/core/model.py
    "BaseModel",

    # From src/noah123d/core/parameters.py
    "ModelParameters",

    # From src/noah123d/core/context_decorators.py
    "auto_context_function_with_checks",
    "context_function",
    "context_function_with_check",
]
# [[[end]]] (sum: Wdn7dQk6FR)
