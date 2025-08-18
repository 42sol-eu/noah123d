# -*- coding: utf-8 -*-
"""
OCP viewer configuration and colormap visualization helper for build123d projects.
----
file:
    name:       viewer.py  
    uuid:       b2c3d4e5-6f7g-8h9i-0j1k-l2m3n4o5p6q7
description:    OCP viewer configuration and colormap visualization helper for build123d projects
authors:        felix@42sol.eu
project:
    name:       noah123d
    uuid:       93fe70d7-2d29-4ebf-bf0e-51d75dbfda30
    url:        https://github.com/42sol-eu/noah123d
"""

# %% [External imports]
from typing import Optional

# %% [Local imports]
try:
    from .colormap_helper import ColorMapHelper, _P
except ImportError:
    # For standalone testing
    from colormap_helper import ColorMapHelper, _P

# %% [Parameters]

_DEFAULT_PORT: int = 3939

try:
    from ocp_vscode import (
        set_port,
        Camera,
        reset_show
    )
    _ocp_available = True
    _DEFAULT_CAMERA = Camera.KEEP
except ImportError:
    _ocp_available = False
    DEFAULT_CAMERA = "keep"

# %% [Functions]
def setup_viewer(
    port: int = _DEFAULT_PORT,
    camera: str = _DEFAULT_CAMERA,
    auto_reset: bool = True
) -> None:
    """
    Set up the OCP viewer with default configuration.
    
    Args:
        port:       Port for the OCP viewer (default: 3939)
        camera:     Camera mode (default: Camera.KEEP)
        auto_reset: Whether to reset the viewer first
    """
    if not _P.OCP_VSCODE_AVAILABLE:
        raise ImportError("ocp_vscode is required for viewer setup")
    
    try:
        # Set the port first to avoid connection issues
        set_port(port)
        
        # Reset the viewer if requested
        if auto_reset:
            reset_show()
            
    except Exception as e:
        # Log warning but don't fail completely
        import warnings
        warnings.warn(f"Failed to fully configure OCP viewer: {e}")

# %% [Backwards Compatibility Alias]
# Keep the old class name for backwards compatibility
ViewerHelper = ColorMapHelper
