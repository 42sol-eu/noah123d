# -*- coding: utf-8 -*-
"""
Analyze a 3MF assembly file and print summary statistics using rich output.
----
file:
    name:       analyze_assembly.py
    uuid:       77017a44-84ec-4fc2-bfd2-f7d294a8df04
author:         felix@42sol.eu
project:
    name:       noah123d
    uuid:       93fe70d7-2d29-4ebf-bf0e-51d75dbfda30
    url:        https://github.com/42sol-eu/noah123d
"""

# %% [External imports]
import sys  #!md| [docs](https://docs.python.org/3/library/sys.html)
from pathlib import (
    Path
)  #!md| [docs](https://docs.python.org/3/library/pathlib.html)

# %% [Local imports]
from noah123d.visual.console import Console  #!md| [docs](https://rich.readthedocs.io/en/stable/console.html)

# %% [Local imports]
from noah123d.threemf import (
    Archive, Directory, Model, Metadata 
) #!md| [docs](https://github.com/42sol-eu/noah123d)

# %% [Example]
def analyze_assembly(file_path: str):
    """Analyze the created 3MF assembly file."""
    console = Console()
    assembly_path = Path(file_path)

    if not assembly_path.exists():
        console.print_file_not_found(file_path)
        return

    console.print_file_info(file_path)

    try:
        with Archive(assembly_path, 'r') as archive:
            contents = archive.list_contents()
            console.print_content(contents)  # Should detect 'archive' context

            # Check for metadata
            metadata_files = [c for c in contents if 'Metadata' in c]
            console.print_content(metadata_files)  # Let it auto-detect based on content

            with Directory('3D') as models_dir:
                with Model() as model:
                    object_count = model.get_object_count()
                    console.print_model_analysis(object_count)

                    if object_count > 0:
                        total_vertices = 0
                        total_triangles = 0
                        actual_objects = 0
                        object_details = []

                        # Check a wider range of object IDs to find all objects
                        for i in range(1, max(20, object_count + 10)):
                            obj = model.get_object(i)
                            if obj:
                                vertices = len(obj.get('vertices', []))
                                triangles = len(obj.get('triangles', []))
                                total_vertices += vertices
                                total_triangles += triangles
                                actual_objects += 1
                                object_details.append({
                                    'id': i,
                                    'vertices': vertices,
                                    'triangles': triangles
                                })

                        console.print_object_table(object_details, "3D Objects in Assembly")
                        console.print_assembly_totals(object_count, actual_objects, total_vertices, total_triangles)

    except Exception as e:
        console.print_error(e)

# %% [Main]
if __name__ == "__main__":
    import sys
    analyze_assembly("./examples/ark_kit.3mf")
