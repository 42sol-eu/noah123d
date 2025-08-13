# -*- coding: utf-8 -*-
"""
Reusable parameter classes for build123d projects.

This module provides base parameter classes and utilities for managing
parameters across different 3D modeling projects.

This file is designed to be added to the noah123d package.

----
file:
    name:       parameters.py (for noah123d package)
    uuid:       a706e3df-cd43-46ee-bcb5-db8e268dfa13
description:    Reusable parameter classes and utilities for build123d projects
authors:         felix@42sol.eu
project:
    name:       noah123d
    uuid:       93fe70d7-2d29-4ebf-bf0e-51d75dbfda30
    url:        https://github.com/42sol-eu/noah123d
"""

# %% [Imports]
from dataclasses import dataclass, fields, field  # https://docs.python.org/3/library/dataclasses.html
from pathlib import Path  #!md| [docs](https://docs.python.org/3/library/pathlib.html)
from typing import Dict, Any, Optional


from dataclasses import dataclass
from typing import Optional


# %% [Internal Imports]
from .constants import *
from .logging import *


@dataclass
class ModelParameters:
    """Base parameters used in all models."""
    name: str
    width: float
    height: float
    depth: float
    material: Optional[str] = None

    def __post_init__(self) -> None:
        logging.debug(
            "ModelParameters initialized with name=%s, width=%.2f, height=%.2f, depth=%.2f, material=%s",
            self.name, self.width, self.height, self.depth, self.material
        )
