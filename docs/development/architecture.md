# Development architecture

## Overview

The development architecture of the noah123d library is designed to facilitate the conversion and manipulation of 3D models, particularly focusing on the 3MF file format. The architecture is modular, with distinct components handling specific aspects of the workflow.

## Core components

- [`Archive3mf`](../reference/archive3mf.md): Handles the 3MF file zip archive, including reading and writing 3MF files.
- [`Directory`](../reference/directory.md): Manages directories inside the archive.
- [`Model`](../reference/model.md): Represents the 3D model structure, including parts and assemblies.



> [!Important]
> Models inside a 3mf file are not STL files. Therefore the package supports different conversion functions provided via [`numpy-stl`](https://github.com/stl-utils/numpy-stl).

## Toolbox:


- [`Analysis`](../reference/analyzer.md): Analyzes 3MF files, extracting metadata, geometry information, and validating file integrity.
- [`STLConverter`](../user-guide/stl-conversion.md): Converts STL files to 3MF format, handling validation and metadata generation.
- [`MultiAssembly`](../reference/multi-assembly.md): Manages multiple STL files, creating assemblies with specified layouts and configurations.
- [`GridLayout`](../reference/grid-layouts.md): Provides functions for arranging multiple 3D objects in a grid layout, calculating optimal rows and columns based on object dimensions and spacing. TODO: only one model?
