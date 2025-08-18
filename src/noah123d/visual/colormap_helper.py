# -*- coding: utf-8 -*-
"""
ColorMap visualization helper for build123d projects.
----
file:
    name:       colormap_helper.py  
    uuid:       a1b2c3d4-5e6f-7g8h-9i0j-k1l2m3n4o5p6
description:    ColorMap visualization helper for build123d projects
authors:        felix@42sol.eu
project:
    name:       noah123d
    uuid:       93fe70d7-2d29-4ebf-bf0e-51d75dbfda30
    url:        https://github.com/42sol-eu/noah123d
"""

# %% [External imports]
import copy
from typing import (
    List,
    Optional,
    Union,
    Any,
    Tuple
)

from build123d import (
    Box,
    GridLocations,
    Pos,
    Sphere
)

# %% [Parameters]

class _Parameters:
    OCP_VSCODE_AVAILABLE: bool = None
    DEFAULT_GRID_SIZE: int = 20
    DEFAULT_SPACING: float = 2.0
    DEFAULT_OBJECT_SIZE: float = 1.0

    # Popular colormap presets with their types (segmented vs listed)
    PRESET_COLORMAPS: dict[str, tuple[str, str]] = {
        'rainbow': ('hsv', 'segmented'),
        'heat': ('mpl:hot', 'segmented'),
        'cool': ('mpl:cool', 'segmented'),
        'viridis': ('mpl:viridis', 'listed'),
        'plasma': ('mpl:plasma', 'listed'),
        'blues': ('mpl:Blues', 'segmented'),
        'greens': ('mpl:Greens', 'segmented'),
        'reds': ('mpl:Reds', 'segmented'),
        'turbo': ('mpl:turbo', 'listed'),
        'summer': ('mpl:summer', 'segmented')
    }

_P = _Parameters()

try:
    from ocp_vscode import (
        ColorMap,
        set_colormap,
        reset_show,
        show,
        show_object,
        set_port,
        Camera
    )
    from ocp_vscode.colors import ListedColorMap
    _P.OCP_VSCODE_AVAILABLE = True
except ImportError:
    _P.OCP_VSCODE_AVAILABLE = False
    # Create dummy classes for when ocp_vscode is not available
    class ColorMap:
        @staticmethod
        def tab20(**kwargs):
            return None
        @staticmethod
        def segmented(*args, **kwargs):
            return None
        @staticmethod
        def golden_ratio(*args, **kwargs):
            return None
        @staticmethod
        def seeded(*args, **kwargs):
            return None
        @staticmethod
        def listed(*args, **kwargs):
            return None
    
    class Camera:
        KEEP = "keep"


# %% [Classes]
class ColorMapHelper:
    """
    Helper class for creating and visualizing objects with colormaps using build123d and ocp_vscode.
    
    This class simplifies the process of creating grids of objects with various colormap
    strategies, making it easier to visualize data or create appealing demonstrations.
    Includes automatic OCP viewer configuration and camera management.
    """

    def __init__(
        self,
        grid_size: int = _P.DEFAULT_GRID_SIZE,
        spacing: float = _P.DEFAULT_SPACING,
        object_size: float = _P.DEFAULT_OBJECT_SIZE,
        auto_setup_port: bool = True,
        port: int = 3939,
        camera: str = None
    ):
        """
        Initialize the ColorMapHelper with optional viewer configuration.
        
        Args:
            grid_size:          Number of objects to create in the grid
            spacing:            Distance between objects
            object_size:        Size of each object
            auto_setup_port:    Automatically set OCP viewer port to avoid connection issues
            port:               Port for the OCP viewer (default: 3939)
            camera:             Camera mode (default: Camera.KEEP if available)
        """
        if not _P.OCP_VSCODE_AVAILABLE:
            raise ImportError("ocp_vscode is required for ColorMapHelper")
            
        self.grid_size:         int = grid_size
        self.spacing:           float = spacing
        self.object_size:       float = object_size
        self.port:              int = port
        self.camera:            str = camera if camera is not None else (Camera.KEEP if _P.OCP_VSCODE_AVAILABLE else "keep")
        self._objects:          List[Any] = []
        self._current_colormap: Optional[Any] = None
        
        # Set up OCP viewer port to avoid connection issues
        if auto_setup_port and _P.OCP_VSCODE_AVAILABLE:
            try:
                set_port(self.port)
            except Exception:
                # Silently continue if port setting fails
                pass # TODO: check if this is a good idea at least an warning should be helpful!

    def _show_with_config(self, *objects, colors=None, **kwargs) -> None:
        """
        Show objects with the configured camera settings.
        
        Args:
            *objects:   Objects to show
            colors:     Colormap to use
            **kwargs:   Additional arguments for show()
        """
        # Apply default camera setting if not specified
        if 'camera' not in kwargs and _P.OCP_VSCODE_AVAILABLE:
            kwargs['camera'] = self.camera
            
        if colors is not None:
            show(*objects, colors=colors, **kwargs)
        else:
            show(*objects, **kwargs)

    def create_sphere_grid(
        self, 
        rows: int = 1, 
        cols: Optional[int] = None
    ) -> List[Any]:
        """
        Create a grid of spheres.
        
        Args:
            rows:   Number of rows in the grid
            cols:   Number of columns in the grid (defaults to grid_size if None)
            
        Returns:
            List of sphere objects positioned in a grid
        """
        if cols is None:
            cols = self.grid_size
            
        sphere = Sphere(self.object_size)
        locations = GridLocations(
            x_spacing=self.spacing,
            y_spacing=self.spacing,
            x_count=cols,
            y_count=rows
        )
        
        self._objects = [
            copy.copy(sphere).move(loc) 
            for loc in locations
        ]
        
        return self._objects

    def create_box_grid(
        self, 
        rows: int = 1, 
        cols: Optional[int] = None
    ) -> List[Any]:
        """
        Create a grid of boxes.
        
        Args:
            rows:   Number of rows in the grid
            cols:   Number of columns in the grid (defaults to grid_size if None)
            
        Returns:
            List of box objects positioned in a grid
        """
        if cols is None:
            cols = self.grid_size
            
        locations = [
            Pos(self.spacing * i, self.spacing * j, 0) 
            for i in range(cols) 
            for j in range(rows)
        ]
        
        self._objects = [
            loc * Box(self.object_size, self.object_size, self.object_size)
            for loc in locations
        ]
        
        return self._objects

    def show_with_preset(
        self, 
        preset_name: str,
        alpha: float = 1.0,
        reverse: bool = False,
        segments: Optional[int] = None
    ) -> None:
        """
        Show objects with a preset colormap.
        
        Args:
            preset_name:    Name of the preset colormap (see PRESET_COLORMAPS)
            alpha:          Transparency value (0.0 to 1.0)
            reverse:        Whether to reverse the colormap
            segments:       Number of color segments (uses golden ratio if None)
        """
        if not self._objects:
            self.create_sphere_grid()
            
        if preset_name not in  _P.PRESET_COLORMAPS:
            raise ValueError(f"Unknown preset: {preset_name}. Available: {list(_P.PRESET_COLORMAPS.keys())}")

        colormap_name, colormap_type =  _P.PRESET_COLORMAPS[preset_name]
        
        if segments is not None:
            if colormap_type == 'listed':
                colormap = ColorMap.listed(segments, colormap_name, alpha=alpha, reverse=reverse)
            else:
                colormap = ColorMap.segmented(segments, colormap_name, alpha=alpha, reverse=reverse)
        else:
            colormap = ColorMap.golden_ratio(colormap_name, alpha=alpha, reverse=reverse)
            
        self._current_colormap = colormap
        self._show_with_config(*self._objects, colors=colormap)

    def show_with_tab20(
        self, 
        alpha: float = 0.8, 
        reverse: bool = False
    ) -> None:
        """
        Show objects with the tab20 colormap.
        
        Args:
            alpha:      Transparency value (0.0 to 1.0)
            reverse:    Whether to reverse the colormap
        """
        if not self._objects:
            self.create_sphere_grid()
            
        colormap = ColorMap.tab20(alpha=alpha, reverse=reverse)
        self._current_colormap = colormap
        self._show_with_config(*self._objects, colors=colormap)

    def show_with_segmented(
        self,
        segments: int,
        colormap_name: str = 'hsv',
        alpha: float = 1.0,
        reverse: bool = False
    ) -> None:
        """
        Show objects with a segmented colormap.
        
        Args:
            segments:       Number of color segments
            colormap_name:  Name of the colormap
            alpha:          Transparency value (0.0 to 1.0)
            reverse:        Whether to reverse the colormap
        """
        if not self._objects:
            self.create_sphere_grid()
            
        # Try segmented first, fall back to listed if it fails
        try:
            colormap = ColorMap.segmented(segments, colormap_name, alpha=alpha, reverse=reverse)
        except ValueError:
            # If segmented fails, try listed
            colormap = ColorMap.listed(segments, colormap_name, alpha=alpha, reverse=reverse)
            
        self._current_colormap = colormap
        self._show_with_config(*self._objects, colors=colormap)

    def show_with_smart_colormap(
        self,
        segments: int,
        colormap_name: str = 'hsv',
        alpha: float = 1.0,
        reverse: bool = False
    ) -> None:
        """
        Show objects with a colormap, automatically choosing between segmented and listed.
        
        Args:
            segments:       Number of color segments
            colormap_name:  Name of the colormap
            alpha:          Transparency value (0.0 to 1.0)
            reverse:        Whether to reverse the colormap
        """
        if not self._objects:
            self.create_sphere_grid()
            
        # Try segmented first, fall back to listed if it fails
        try:
            colormap = ColorMap.segmented(segments, colormap_name, alpha=alpha, reverse=reverse)
        except ValueError:
            try:
                colormap = ColorMap.listed(segments, colormap_name, alpha=alpha, reverse=reverse)
            except ValueError:
                # If both fail, fall back to golden ratio
                colormap = ColorMap.golden_ratio(colormap_name, alpha=alpha, reverse=reverse)
            
        self._current_colormap = colormap
        self._show_with_config(*self._objects, colors=colormap)

    def show_with_golden_ratio(
        self,
        colormap_name: str = 'hsv',
        alpha: float = 1.0,
        reverse: bool = False
    ) -> None:
        """
        Show objects with golden ratio color distribution.
        
        Args:
            colormap_name:  Name of the colormap
            alpha:          Transparency value (0.0 to 1.0)
            reverse:        Whether to reverse the colormap
        """
        if not self._objects:
            self.create_sphere_grid()
            
        colormap = ColorMap.golden_ratio(colormap_name, alpha=alpha, reverse=reverse)
        self._current_colormap = colormap
        self._show_with_config(*self._objects, colors=colormap)

    def show_with_seeded_random(
        self,
        seed: int,
        colormap_name: str = 'hsv',
        alpha: float = 1.0,
        lower: int = 0,
        upper: int = 100,
        brightness: float = 1.0
    ) -> None:
        """
        Show objects with seeded random colors.
        
        Args:
            seed:           Random seed for reproducible colors
            colormap_name:  Name of the colormap
            alpha:          Transparency value (0.0 to 1.0)
            lower:          Lower bound for color range
            upper:          Upper bound for color range
            brightness:     Brightness multiplier
        """
        if not self._objects:
            self.create_sphere_grid()
            
        colormap = ColorMap.seeded(
            seed, 
            colormap_name, 
            alpha=alpha, 
            lower=lower, 
            upper=upper, 
            brightness=brightness
        )
        self._current_colormap = colormap
        self._show_with_config(*self._objects, colors=colormap)

    def show_with_custom_colors(
        self, 
        colors: List[str]
    ) -> None:
        """
        Show objects with custom list of colors.
        
        Args:
            colors: List of color names or hex values
        """
        if not self._objects:
            self.create_sphere_grid()
            
        colormap = ColorMap.listed(colors=colors)
        self._current_colormap = colormap
        self._show_with_config(*self._objects, colors=colormap)

    def set_global_colormap(
        self, 
        colormap_type: str = 'golden_ratio',
        colormap_name: str = 'mpl:Blues',
        alpha: float = 0.8,
        **kwargs
    ) -> None:
        """
        Set a global colormap that affects all subsequent show operations.
        
        Args:
            colormap_type:  Type of colormap ('golden_ratio', 'segmented', 'tab20', 'seeded')
            colormap_name:  Name of the colormap
            alpha:          Transparency value (0.0 to 1.0)
            **kwargs:       Additional arguments specific to colormap type
        """
        if colormap_type == 'golden_ratio':
            colormap = ColorMap.golden_ratio(colormap_name, alpha=alpha, **kwargs)
        elif colormap_type == 'segmented':
            segments = kwargs.get('segments', 20)
            colormap = ColorMap.segmented(segments, colormap_name, alpha=alpha, **kwargs)
        elif colormap_type == 'tab20':
            colormap = ColorMap.tab20(alpha=alpha, **kwargs)
        elif colormap_type == 'seeded':
            seed = kwargs.get('seed', 42)
            colormap = ColorMap.seeded(seed, colormap_name, alpha=alpha, **kwargs)
        else:
            raise ValueError(f"Unknown colormap type: {colormap_type}")
            
        set_colormap(colormap)
        self._current_colormap = colormap

    def show_simple(self) -> None:
        """
        Show objects with the current global colormap or a default one.
        """
        if not self._objects:
            self.create_sphere_grid()
            
        self._show_with_config(*self._objects)

    def reset_visualization(self) -> None:
        """
        Reset the visualization system to default state.
        """
        reset_show()
        self._current_colormap = None

    def get_available_presets(self) -> List[str]:
        """
        Get list of available colormap presets.
        
        Returns:
            List of preset names
        """
        return list(PRESET_COLORMAPS.keys())

    def demo_all_presets(self) -> None:
        """
        Demonstrate all available preset colormaps.
        """
        if not self._objects:
            self.create_sphere_grid()
            
        print("Demonstrating all available colormap presets:")
        print("=" * 50)
        
        for preset in self.get_available_presets():
            print(f"Showing preset: {preset}")
            self.show_with_preset(preset)
            input("Press Enter to continue to next preset...")

    @property
    def objects(self) -> List[Any]:
        """Get the current list of objects."""
        return self._objects

    @property
    def current_colormap(self) -> Optional[Any]:
        """Get the current colormap."""
        return self._current_colormap
