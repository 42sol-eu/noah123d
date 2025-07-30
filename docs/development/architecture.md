# Development Architecture

## Main Setup


- `Archive3mf`: Handles the 3MF file format, including reading and writing 3MF files.
- `Directory`: Manages directories and file paths for input and output.
- `Model`: Represents the 3D model structure, including parts and assemblies.

> [!Important]
> Models inside a 3mf file are not STL files. Therefore the package supports different conversion functions.
> 