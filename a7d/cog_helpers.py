#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
COG helpers for automated __init__.py generation.
----
file:
    name:        cog_helpers.py  
    uuid:        5c49da26-c349-4165-9515-c59c3d2ca3d5
description:     COG helpers for automated __init__.py generation
authors:         felix@42sol.eu
project:
    name:        a7d
    uuid:        2cc2a024-ae2a-4d2c-91c2-f41348980f7f
    url:         https://github.com/42sol-eu/a7d
"""

# %% [External imports]
import sys
from pathlib import Path

# %% [Local imports]
from update_init import (
    scan_python_file,
    update_init_file,
    is_private_name,
)
from collect_init import generate_main_init

# %% [Functions]
def generate_subpackage_imports_and_all(directory_path: str, include_private: bool = False, group_by_file: bool = True) -> str:
    """
    Generate import statements and __all__ list for a subpackage directory.
    Returns the content as a string for COG to insert.
    
    Args:
        directory_path: Path to the directory containing Python files
        include_private: Whether to include private names (starting with _)
        group_by_file: Whether to group __all__ entries by source file
        
    Returns:
        String containing import statements and __all__ list
    """
    from pathlib import Path as PathlibPath
    
    folder_path = PathlibPath(directory_path)
    
    # Scan all Python files in the directory
    py_files = [f for f in folder_path.iterdir() if f.suffix == ".py" and f.name != "__init__.py"]
    
    if not py_files:
        return "# No Python files found to import"
    
    all_available_names = set()
    all_elements = []
    element_sources = {}
    element_order = []
    import_by_module = {}
    
    # Get relative path for comments
    try:
        relative_folder = folder_path.relative_to(PathlibPath.cwd())
    except ValueError:
        relative_folder = folder_path
    
    # Scan files and collect elements
    for file_path in py_files:
        elements = scan_python_file(file_path, include_private)
        if elements:
            for typ, name in elements:
                all_available_names.add(name)
                all_elements.append((typ, name))
                element_sources[name] = str(relative_folder / file_path.name)
                element_order.append((name, str(relative_folder / file_path.name)))
                
                # Group imports by module
                module = f".{file_path.stem}"
                if module not in import_by_module:
                    import_by_module[module] = []
                import_by_module[module].append(name)
    
    if not all_elements:
        return "# No elements found to import"
    
    # Generate import statements
    import_lines = []
    for module in sorted(import_by_module.keys()):
        names = sorted(import_by_module[module])
        if len(names) == 1:
            import_lines.append(f"from {module} import {names[0]}")
        elif len(names) <= 3:
            import_lines.append(f"from {module} import {', '.join(names)}")
        else:
            names_str = ",\n    ".join(names)
            import_lines.append(f"from {module} import (\n    {names_str},\n)")
    
    # Generate __all__ list
    all_names = [name for _, name in all_elements]
    
    if group_by_file and element_order:
        # Group by source file
        file_groups = {}
        for name, source_path in element_order:
            if source_path not in file_groups:
                file_groups[source_path] = []
            file_groups[source_path].append(name)
        
        all_lines = ['__all__ = [']
        files_list = list(dict.fromkeys(source_path for _, source_path in element_order))
        
        for i, source_path in enumerate(files_list):
            if source_path in file_groups and file_groups[source_path]:
                all_lines.append(f"    # From {source_path}")
                sorted_elements = sorted(file_groups[source_path], key=str.lower)
                for name in sorted_elements:
                    all_lines.append(f'    "{name}",')
                if i < len(files_list) - 1:
                    all_lines.append("")
        
        all_lines.append("]")
    else:
        # Alphabetical sorting
        all_names = sorted(set(all_names), key=str.lower)
        if len(all_names) <= 3:
            all_lines = [f"__all__ = {all_names}"]
        else:
            all_lines = ['__all__ = [']
            for name in all_names:
                if name in element_sources:
                    all_lines.append(f'    "{name}",  # {element_sources[name]}')
                else:
                    all_lines.append(f'    "{name}",')
            all_lines.append("]")
    
    # Combine imports and __all__
    result_lines = import_lines + [""] + all_lines
    return "\n".join(result_lines)


def generate_main_package_imports_and_all(package_path: str, include_private: bool = False, group_by_file: bool = True, update_first: bool = True) -> str:
    """
    Generate import statements and __all__ list for the main package.
    Returns the content as a string for COG to insert.
    
    Args:
        package_path: Path to the package directory
        include_private: Whether to include private names (starting with _)
        group_by_file: Whether to group __all__ entries by source file
        update_first: Whether to update subdirectories first
        
    Returns:
        String containing import statements and __all__ list
    """
    # This is more complex - for now, let's use a simplified approach
    # that calls the existing function and then reads the result
    from pathlib import Path as PathlibPath
    import tempfile
    import shutil
    
    package_dir = PathlibPath(package_path)
    
    # Create a temporary copy to work with
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_package = PathlibPath(temp_dir) / package_dir.name
        shutil.copytree(package_dir, temp_package)
        
        # Generate the content
        generate_main_init(temp_package, include_private, cleanup=True, group_by_file=group_by_file, update_first=update_first)
        
        # Read the generated __init__.py and extract imports and __all__
        init_file = temp_package / "__init__.py"
        if init_file.exists():
            content = init_file.read_text(encoding="utf-8")
            lines = content.splitlines()
            
            # Find the start of imports and __all__
            start_idx = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('from .') or line.strip().startswith('__all__'):
                    start_idx = i
                    break
            
            # Extract the relevant content
            relevant_lines = []
            for line in lines[start_idx:]:
                if line.strip() == "" and not relevant_lines:
                    continue  # Skip leading empty lines
                relevant_lines.append(line)
            
            return "\n".join(relevant_lines)
    
    return "# Failed to generate content"
