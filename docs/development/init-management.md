# __init__.py Management Tools

This document describes the comprehensive set of tools for managing Python `__init__.py` files in the noah123d project.

## Overview

The project includes three interconnected tools for managing Python package imports:

1. **`a7d/update_init.py`** - Manages individual package/directory `__init__.py` files
2. **`a7d/collect_init.py`** - Aggregates main package `__init__.py` from subdirectories
3. **COG Integration** - Automated generation using Code Generator comments

## Tool 1: update_init.py

Updates `__init__.py` files for individual packages by scanning Python files and extracting classes, functions, and variables.

### Usage

```bash
# Update a single directory's __init__.py
python a7d/update_init.py src/noah123d/core

# Update all subdirectories recursively
python a7d/update_init.py --all src/noah123d

# Include private members (starting with _)
python a7d/update_init.py --include-private src/noah123d/core

# Remove stale entries that no longer exist
python a7d/update_init.py --cleanup src/noah123d/core

# Group __all__ entries by source file
python a7d/update_init.py --group-by-file src/noah123d/core
```

### Features

- **AST-based parsing**: Safely extracts Python symbols without executing code
- **Multi-line `__all__` handling**: Properly parses existing `__all__` declarations
- **Duplicate consolidation**: Removes duplicate imports and entries
- **Privacy awareness**: Filters private members (starting with `_`) by default
- **Source attribution**: Adds comments showing which file each symbol comes from
- **File-based grouping**: Organizes `__all__` entries by source file with section headers
- **Cleanup validation**: Removes entries for symbols that no longer exist
- **Black formatting**: Automatically formats output with Black code formatter

## Tool 2: collect_init.py

Aggregates the main package `__init__.py` by combining exports from subdirectories and main directory files.

### Usage

```bash
# Generate main package __init__.py
python a7d/collect_init.py src/noah123d

# Update subdirectories first, then aggregate
python a7d/collect_init.py --update-first src/noah123d

# Include private members and group by file
python a7d/collect_init.py --update-first --include-private --group-by-file src/noah123d
```

### Features

- **Subdirectory integration**: Imports from subpackage `__init__.py` files
- **Main directory scanning**: Includes classes/functions from files in the main directory
- **Automatic updates**: `--update-first` runs `update_init.py` on subdirectories first
- **Hierarchical organization**: Separates main directory and subpackage exports
- **All update_init.py features**: Inherits all features from the underlying tool

## Tool 4: COG Automation Runner

A unified script that discovers and runs all COG automation in a project with professional table-style output.

### Usage

```bash
# Run COG generation on all files in a folder
./a7d/run_cog.py src/noah123d

# Check if files need regeneration (don't modify)
./a7d/run_cog.py src/noah123d --check

# Generate without checksum protection (not recommended)
./a7d/run_cog.py src/noah123d --no-checksum

# Show detailed output with file information
./a7d/run_cog.py src/noah123d --verbose

# Check with diff output to see what would change
./a7d/run_cog.py src/noah123d --check --diff
```

### Features

- **Auto-discovery**: Finds all files with COG markers recursively
- **Table output**: Professional table format with step numbers, icons, and descriptions
- **File-specific tables**: Each file gets its own processing table
- **Summary reporting**: Overall statistics in a summary table
- **Checksum protection**: Integrated with COG's checksum safety features
- **Verbose mode**: Detailed information about file types and processing steps
- **Icon legend**: Clear legend explaining all status icons (F=File, G=Generate, ?=Check, +=Success, !=Change, W=Warning, X=Error, S=Summary)

### Output Format

Each file is processed in its own table showing:
1. **Step 1**: File discovery with metadata
2. **Step 2**: Processing (generation or checking)
3. **Step 3**: Results with status
4. **Details**: Additional information in verbose mode

The tool provides a professional interface for managing all COG automation across the project.

Uses [COG (Code Generator)](https://nedbatchelder.com/code/cog/) for automated `__init__.py` generation via embedded comments.

### Installation

```bash
pip install cogapp
```

### Usage

```bash
# Regenerate a single __init__.py file
cog -r src/noah123d/core/__init__.py

# Regenerate with checksum protection (recommended)
cog -c -r src/noah123d/core/__init__.py

# Regenerate all __init__.py files with checksum protection
cog -c -r src/noah123d/**/__init__.py

# Check what would be generated without writing
cog -c -c src/noah123d/core/__init__.py

# Check if files need regeneration (with diff output)
cog --check --diff src/noah123d/**/__init__.py
```

### COG Checksum Protection

All `__init__.py` files now include checksum protection. When you run COG with the `-c` flag, it generates a checksum of the output content. If someone manually edits the generated content, COG will detect this and refuse to overwrite the manual changes:

```bash
# This will fail if manual edits were made:
cog -c -r src/noah123d/core/__init__.py
# Output: "Output has been edited! Delete old checksum to unprotect."
```

To override manual edits (use with caution):
1. Remove the checksum from the end marker: `# [[[end]]] (sum: Wdn7dQk6FR)` → `# [[[end]]]`
2. Run COG again to regenerate
3. The new checksum will be automatically added

### COG Helper Functions

The `a7d/cog_helpers.py` module provides two key functions:

1. **`generate_subpackage_imports_and_all(package_path, group_by_file=True)`**
   - For individual package `__init__.py` files
   - Uses `update_init.py` functionality

2. **`generate_main_package_imports_and_all(package_path, group_by_file=True, update_first=True)`**
   - For main package `__init__.py` files
   - Uses `collect_init.py` functionality

### COG Comments Structure

Each `__init__.py` file contains embedded COG comments:

```python
# [[[cog
# import sys
# from pathlib import Path
# sys.path.insert(0, str(Path(cog.inFile).parent.parent.parent.parent / "a7d"))
# from cog_helpers import generate_subpackage_imports_and_all
# content = generate_subpackage_imports_and_all(str(Path(cog.inFile).parent), group_by_file=True)
# cog.out(content)
# ]]]
# Generated imports and __all__ will appear here
# [[[end]]]
```

## File Organization with --group-by-file

When using `--group-by-file` option, the `__all__` list is organized by source file:

```python
__all__ = [
    # From src/noah123d/core/logging.py
    "Log",

    # From src/noah123d/core/constants.py
    "mm",
    "no",
    "yes",

    # From src/noah123d/core/model.py
    "BaseModel",

    # ... etc
]
```

## Integration with Build Systems

### Manual Workflow

1. Update individual packages:
   ```bash
   python a7d/update_init.py --all --group-by-file src/noah123d
   ```

2. Update main package:
   ```bash
   python a7d/collect_init.py --update-first --group-by-file src/noah123d
   ```

### Automated Workflow (COG)

1. One-time setup: Add COG comments to `__init__.py` files (already done)

2. Regenerate all files:
   ```bash
   cog -r src/noah123d/**/__init__.py
   ```

3. Integration with CI/CD:
   ```bash
   # Check if files are up to date
   cog -c src/noah123d/**/__init__.py
   
   # Fail build if regeneration needed
   cog -c src/noah123d/**/__init__.py || exit 1
   ```

## Best Practices

1. **Use COG for automation**: COG integration provides the cleanest automation
2. **Group by file**: Always use `--group-by-file` for better organization
3. **Update subdirectories first**: Use `--update-first` when updating main packages
4. **Include cleanup**: Use `--cleanup` periodically to remove stale entries
5. **Version control**: Commit both the COG comments and generated content
6. **CI integration**: Add COG checks to prevent drift between generated and committed content

## Troubleshooting

### Common Issues

1. **Import errors in COG**: Ensure `a7d/` directory is in the Python path
2. **Missing files**: Verify all source files exist before running tools
3. **Syntax errors**: Check that generated Python code is valid
4. **Path issues**: Use absolute paths when possible

### Debugging

```bash
# Test update_init.py directly
python a7d/update_init.py --help

# Test collect_init.py directly  
python a7d/collect_init.py --help

# Test COG without writing
cog -c src/noah123d/core/__init__.py

# Verbose COG output
cog -v -r src/noah123d/core/__init__.py
```

This comprehensive toolkit provides both manual control and automated generation for maintaining clean, organized `__init__.py` files across the entire project.
