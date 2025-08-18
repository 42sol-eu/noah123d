#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Collect and update main package __init__.py from subdirectories and main directory files.
----
file:
    name:        collect_init.py  
    uuid:        8a9f9244-9783-4db3-a037-690ebbc99b70
description:     Collect and update main package __init__.py from subdirectories and main directory files
authors:         felix@42sol.eu
project:
project:
    name:        a7d
    uuid:        2cc2a024-ae2a-4d2c-91c2-f41348980f7f
    url:         https://github.com/42sol-eu/a7d
"""
# %% [External imports]
import ast
import os
import subprocess
from click import (
    command,
    argument,
    option,
    Path,
    secho,
    echo,
    style,
)
#!md| [docs](https://github.com/42sol-eu/noah123d)
from pathlib import (
    Path as PathlibPath,
)
#!md| [docs](https://github.com/42sol-eu/noah123d)


# %% [Parameters]
class Parameter:
    init_file_name:     str = "__init__.py"

P = Parameter()

# %% [Functions]
def is_private_name(name: str) -> str:
    """Determine the privacy level of a Python name."""
    if name.startswith('__') and name.endswith('__'):
        return 'dunder'
    elif name.startswith('__'):
        return 'private'
    elif name.startswith('_'):
        return 'internal'
    else:
        return 'public'

def scan_python_file(file_path: PathlibPath, include_private: bool = False) -> list:
    """Scan a Python file and return top-level classes, functions, and global variables."""
    with open(file_path, "r", encoding="utf-8") as f:
        node = ast.parse(f.read(), filename=str(file_path))
    elements = []
    for n in node.body:
        if isinstance(n, ast.ClassDef):
            if include_private or not n.name.startswith('_'):
                elements.append(("class", n.name))
        elif isinstance(n, ast.FunctionDef):
            if include_private or not n.name.startswith('_'):
                elements.append(("function", n.name))
        elif isinstance(n, ast.Assign):
            for target in n.targets:
                if isinstance(target, ast.Name):
                    if include_private or not target.id.startswith('_'):
                        elements.append(("variable", target.id))
        elif isinstance(n, ast.AnnAssign):
            if isinstance(n.target, ast.Name):
                if include_private or not n.target.id.startswith('_'):
                    elements.append(("variable", n.target.id))
    return elements

def scan_subpackage_init(subdir_path: PathlibPath, relative_folder: PathlibPath) -> list:
    """Scan a subpackage's __init__.py and extract its __all__ list."""
    init_path = subdir_path / P.init_file_name
    if not init_path.exists():
        return []
    
    try:
        with open(init_path, "r", encoding="utf-8") as f:
            node = ast.parse(f.read(), filename=str(init_path))
        
        for n in node.body:
            if isinstance(n, ast.Assign):
                for target in n.targets:
                    if isinstance(target, ast.Name) and target.id == "__all__":
                        if isinstance(n.value, ast.List):
                            all_names = []
                            for elem in n.value.elts:
                                if isinstance(elem, ast.Constant) and isinstance(elem.value, str):
                                    all_names.append(elem.value)
                                elif hasattr(elem, 's'):  # For backward compatibility
                                    all_names.append(elem.s)
                            return [(subdir_path.name, name, str(relative_folder / subdir_path.name / P.init_file_name)) for name in all_names]
    except Exception as e:
        secho(f"Error reading {init_path}: {e}", fg="red")
    
    return []

def update_subdirectories(package_path: PathlibPath, include_private: bool = False, group_by_file: bool = False):
    """Run update_init.py on all subdirectories containing Python files."""
    secho("Updating subdirectories first...", fg="blue")
    
    # Get the path to update_init.py script
    current_dir = PathlibPath(__file__).parent
    update_script = current_dir / "update_init.py"
    
    if not update_script.exists():
        secho(f"Warning: update_init.py not found at {update_script}", fg="yellow")
        return
    
    # Find all subdirectories with Python files
    subdirs_to_update = []
    for subdir in package_path.iterdir():
        if subdir.is_dir() and subdir.name != "__pycache__":
            # Check if this directory contains Python files
            has_python_files = any(
                file.suffix == ".py" and file.name != "__init__.py" 
                for file in subdir.iterdir() 
                if file.is_file()
            )
            if has_python_files:
                subdirs_to_update.append(subdir)
    
    # Update each subdirectory
    for subdir in subdirs_to_update:
        secho(f"  Updating {subdir.name}/", fg="cyan")
        cmd = ["python", str(update_script), str(subdir.absolute()), "--all"]
        if include_private:
            cmd.append("--include-private")
        if group_by_file:
            cmd.append("--group-by-file")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                secho(f"    Warning: Failed to update {subdir.name}/: {result.stderr.strip()}", fg="yellow")
            else:
                secho(f"    ✓ Updated {subdir.name}/", fg="green")
        except Exception as e:
            secho(f"    Error updating {subdir.name}/: {e}", fg="red")
    
    if subdirs_to_update:
        secho(f"Updated {len(subdirs_to_update)} subdirectories\n", fg="blue")
    else:
        secho("No subdirectories with Python files found to update\n", fg="yellow")

def generate_main_init(package_path: PathlibPath, include_private: bool = False, cleanup: bool = True, group_by_file: bool = False, update_first: bool = False):
    """Generate or update the main package __init__.py file."""
    
    # Update subdirectories first if requested
    if update_first:
        update_subdirectories(package_path, include_private, group_by_file)
    
    # Get relative path for comments
    try:
        relative_package = package_path.relative_to(PathlibPath.cwd())
    except ValueError:
        relative_package = package_path
    
    secho(f"Collecting elements for main package {package_path.name}...", fg="cyan")
    if include_private:
        secho("Including private names (starting with _)", fg="yellow")
    else:
        secho("Excluding private names (starting with _) - use --include-private to include them", fg="yellow")
    
    if cleanup:
        secho("Cleanup mode: Will remove non-existing elements", fg="yellow")
    else:
        secho("Cleanup disabled: Will preserve existing entries", fg="yellow")
    
    if group_by_file:
        secho("Grouping __all__ by source file", fg="yellow")
    else:
        secho("Sorting __all__ alphabetically", fg="yellow")
    
    all_elements = []
    all_imports = []
    element_sources = {}
    element_order = []  # Track order for file-based grouping
    all_available_names = set()
    
    # 1. Scan Python files in the main package directory
    py_files = [f for f in package_path.iterdir() if f.suffix == ".py" and f.name != P.init_file_name]
    if py_files:
        secho(f"\nScanning Python files in main directory {package_path.name}/:", fg="cyan")
        for file_path in py_files:
            secho(f"  Scanning {file_path.name}...", fg="cyan")
            elements = scan_python_file(file_path, include_private)
            if elements:
                secho(f"  Found elements in {file_path.name}:", fg="yellow")
                for typ, name in elements:
                    privacy = is_private_name(name)
                    privacy_label = f" ({privacy})" if privacy != 'public' else ""
                    echo(f"    {typ}: {name}{privacy_label}")
                    
                    import_stmt = f"from .{file_path.stem} import {name}"
                    all_imports.append(import_stmt)
                    all_elements.append((typ, name))
                    all_available_names.add(name)
                    element_sources[name] = str(relative_package / file_path.name)
                    element_order.append((name, str(relative_package / file_path.name)))
    
    # 2. Scan subdirectories (subpackages)
    subdirs = [d for d in package_path.iterdir() if d.is_dir() and not d.name.startswith('_') and not d.name.startswith('.')]
    if subdirs:
        secho(f"\nScanning subpackages in {package_path.name}/:", fg="cyan")
        for subdir in subdirs:
            secho(f"  Scanning subpackage {subdir.name}/...", fg="cyan")
            subpackage_elements = scan_subpackage_init(subdir, relative_package)
            if subpackage_elements:
                secho(f"  Found exports from {subdir.name}/__init__.py:", fg="yellow")
                for subpackage_name, name, source_path in subpackage_elements:
                    # Skip private names unless explicitly included
                    if not include_private and name.startswith('_'):
                        continue
                    
                    privacy = is_private_name(name)
                    privacy_label = f" ({privacy})" if privacy != 'public' else ""
                    echo(f"    export: {name}{privacy_label}")
                    
                    import_stmt = f"from .{subpackage_name} import {name}"
                    all_imports.append(import_stmt)
                    all_elements.append(("export", name))
                    all_available_names.add(name)
                    # Track source for all exports
                    element_sources[name] = source_path
                    element_order.append((name, source_path))
    
    if not all_elements:
        secho("No elements found to import.", fg="red")
        return
    
    # 3. Read existing __init__.py if it exists
    init_path = package_path / P.init_file_name
    existing_all_names = []
    if init_path.exists():
        try:
            with open(init_path, "r", encoding="utf-8") as f:
                content = f.read()
            tree = ast.parse(content)
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "__all__":
                            if isinstance(node.value, ast.List):
                                for elem in node.value.elts:
                                    if isinstance(elem, ast.Constant) and isinstance(elem.value, str):
                                        existing_all_names.append(elem.value)
                                    elif hasattr(elem, 's'):
                                        existing_all_names.append(elem.s)
        except Exception as e:
            secho(f"Error reading existing {init_path}: {e}", fg="yellow")
    
    # 4. Consolidate imports by module
    import_by_module = {}
    for import_stmt in all_imports:
        if import_stmt.startswith("from ."):
            parts = import_stmt.split(" import ")
            if len(parts) == 2:
                module = parts[0].replace("from ", "")
                name = parts[1].strip()
                if module not in import_by_module:
                    import_by_module[module] = set()
                import_by_module[module].add(name)
    
    # 5. Generate import statements
    sorted_imports = []
    for module in sorted(import_by_module.keys()):
        names = sorted(import_by_module[module])
        if len(names) == 1:
            sorted_imports.append(f"from {module} import {names[0]}")
        elif len(names) <= 3:
            sorted_imports.append(f"from {module} import {', '.join(names)}")
        else:
            names_str = ",\n    ".join(names)
            sorted_imports.append(f"from {module} import (\n    {names_str},\n)")
    
    # Generate __all__ list
    if group_by_file:
        # Group by source file, maintaining file order
        file_groups = {}
        
        # Group elements by source file while preserving order
        for name, source_path in element_order:
            if source_path not in file_groups:
                file_groups[source_path] = []
            file_groups[source_path].append(name)
        
        # Create ordered list for __all__ with grouping
        all_names = []
        for source_path in dict.fromkeys(source_path for _, source_path in element_order):
            if file_groups[source_path]:
                # Add elements from this file, sorted alphabetically
                sorted_elements = sorted(file_groups[source_path], key=str.lower)
                all_names.extend(sorted_elements)
    else:
        # Sort alphabetically (case-insensitive)
        all_names = list(existing_all_names) if existing_all_names else []
        for typ, name in all_elements:
            if name not in all_names:
                all_names.append(name)
        
        # Cleanup: Remove names that no longer exist
        if cleanup:
            original_count = len(all_names)
            all_names = [name for name in all_names if name in all_available_names]
            removed_count = original_count - len(all_names)
            if removed_count > 0:
                secho(f"Removed {removed_count} non-existing elements from __all__", fg="yellow")
        
        all_names = sorted(set(all_names), key=str.lower)
    
    # 7. Generate the file content
    header = f'''# -*- coding: utf-8 -*-
"""
Main package for {package_path.name}.
----
file:
    name:       __init__.py
    uuid:       auto-generated
description:    Main package for {package_path.name}
authors:         felix@42sol.eu
project:
    name:       {package_path.name}
    uuid:       93fe70d7-2d29-4ebf-bf0e-51d75dbfda30
    url:        https://github.com/42sol-eu/{package_path.name}
"""

'''
#TODO: imporove UUID handling of project and of file itself.
    
    # 8. Write the file
    with open(init_path, "w", encoding="utf-8") as f:
        f.write(header)
        
        # Write imports
        for import_stmt in sorted_imports:
            f.write(import_stmt + "\n")
        
        f.write("\n")
        
        # Write __all__
        if group_by_file:
            # Write grouped __all__ with file comments
            f.write("__all__ = [\n")
            
            # Group by source file again for output
            file_groups = {}
            for name, source_path in element_order:
                if source_path not in file_groups:
                    file_groups[source_path] = []
                file_groups[source_path].append(name)
            
            # Write groups with headers
            for i, source_path in enumerate(dict.fromkeys(source_path for _, source_path in element_order)):
                if file_groups[source_path]:
                    # Add comment header for this file
                    relative_path = os.path.relpath(source_path, package_path.parent)
                    f.write(f"\n#\n    # from {relative_path}\n")
                    
                    # Add elements from this file, sorted alphabetically
                    sorted_elements = sorted(file_groups[source_path], key=str.lower)
                    for name in sorted_elements:
                        f.write(f'    "{name}",\n')
                    
                    # Add blank line between file groups (except for last)
                    files_list = list(dict.fromkeys(source_path for _, source_path in element_order))
                    if i < len(files_list) - 1:
                        f.write("\n")
            
            f.write("]\n")
        else:
            # Write standard __all__
            if len(all_names) <= 3:
                f.write(f"__all__ = {all_names}\n")
            else:
                f.write("__all__ = [\n")
                for name in all_names:
                    if name in element_sources:
                        f.write(f'    "{name}",  # {element_sources[name]}\n')
                    else:
                        f.write(f'    "{name}",\n')
                f.write("]\n")
    
    # 9. Format with black
    subprocess.run(["black", str(init_path)], check=False)
    
    secho(f"\nSuccessfully updated {init_path}", fg="green")
    secho(f"Total imports: {len(sorted_imports)}", fg="green")
    secho(f"Total exports in __all__: {len(all_names)}", fg="green")

# %% [Main]
@command()
@argument("package", type=Path(exists=True, file_okay=False, dir_okay=True))
@option(
    "--include-private",
    type=bool,
    is_flag=True,
    default=False,
    help="Include private names (starting with _) in the scan and __all__ list.",
)
@option(
    "--cleanup",
    type=bool,
    is_flag=True,
    default=True,
    help="Remove non-existing elements from __all__. Use --no-cleanup to disable.",
)
@option(
    "--group-by-file",
    type=bool,
    is_flag=True,
    default=False,
    help="Group __all__ entries by source file instead of alphabetical sorting.",
)
@option(
    "--update-first",
    type=bool,
    is_flag=True,
    default=False,
    help="Run update_init.py on all subdirectories with Python files before collecting main __init__.py.",
)
def cli(package, include_private, cleanup, group_by_file, update_first):
    """Collect and update main package __init__.py from subdirectories and main directory files."""
    package_path = PathlibPath(package)
    generate_main_init(package_path, include_private, cleanup, group_by_file, update_first)

if __name__ == "__main__":
    cli()
