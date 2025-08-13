# Context-Aware Functions in Noah123d

## Overview

Noah123d now supports context-aware functions that eliminate the need to use context object names when working within context managers. This makes the code cleaner and more intuitive.

## Before and After

### Before (Traditional Instance Methods)

```python
from noah123d import Archive
from noah123d import ThreeD
from noah123d import Model

with Archive("output.3mf", 'w') as archive:
    with ThreeD() as threed:
        # Need to use context object name
        threed.add_thumbnail("thumb.png", b"fake_png_data")
        threed.create_model_file("shapes.model", "<model>content</model>")
        
        with Model("shapes.model") as model:
            # Need to use context object name
            vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
            triangles = [[0, 1, 2]]
            obj_id = model.add_object(vertices, triangles)
            count = model.get_object_count()
```

### After (Context-Aware Functions)

```python
from noah123d.archive import Archive, add_file, list_contents, is_writable
from noah123d.directories import ThreeD, add_thumbnail, create_model_file
from noah123d import Model, add_object, get_object_count

with Archive("output.3mf", 'w') as archive:
    # No need for context object name!
    add_file("readme.txt", "Archive created with noah123d")
    
    with ThreeD() as threed:
        # No need for context object name!
        add_thumbnail("thumb.png", b"fake_png_data")
        create_model_file("shapes.model", "<model>content</model>")
        
        with Model("shapes.model") as model:
            # No need for context object name!
            vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
            triangles = [[0, 1, 2]]
            obj_id = add_object(vertices, triangles)
            count = get_object_count()
            
    # Check results without context object name!
    files = list_contents()
    writable = is_writable()
```

## Available Context-Aware Functions

### Archive Functions (Archive)

```python
from noah123d.archive import (
    add_file,                # Add file to archive
    extract_file,            # Extract file from archive
    list_contents,           # List all files in archive
    get_temp_path,           # Get temporary directory path
    is_writable,             # Check if archive is writable
)

with Archive("example.3mf", 'w') as archive:
    add_file("data.txt", "some content")
    add_file("binary.bin", b"binary data")
    
    contents = list_contents()
    writable = is_writable()
    temp_path = get_temp_path()
    
    # Extract files (works in write mode too)
    content = extract_file("data.txt")
```

### Directory Functions (ThreeD)

```python
from noah123d.directories import (
    add_thumbnail,           # Add thumbnail image
    create_model_file,       # Create .model file
    list_model_files,        # List all .model files
)

with ThreeD() as threed:
    add_thumbnail("preview.png", b"png_data")
    create_model_file("shapes.model", "<model>...</model>")
    models = list_model_files()
```

### Directory Functions (Metadata)

```python
from noah123d.directories import (
    add_conversion_info,     # Add conversion metadata
    add_properties,          # Add XML properties
    add_custom_metadata,     # Add custom metadata file
)

from noah123d.directories import Metadata

with Metadata() as metadata:
    add_conversion_info("source.stl", "noah123d", 2)
    add_properties({"version": "1.0", "author": "User"})
    add_custom_metadata("info.txt", "Custom information")
```

### Directory Functions (Textures)

```python
from noah123d.directories import (
    add_texture,             # Add texture image
    list_texture_files,      # List texture files
    get_texture_metadata,    # Get texture metadata
)

from noah123d.directories import Textures

with Textures() as textures:
    add_texture("wood.jpg", b"jpg_data", "color")
    texture_files = list_texture_files()
    metadata = get_texture_metadata("wood.jpg")
```

### Generic Directory Functions

```python
from noah123d.directories import (
    create_file,             # Create any file
    read_file,               # Read file content
    delete_file,             # Delete file
    list_files,              # List files
    list_subdirectories,     # List subdirectories
)

# Works with any directory context
with ThreeD() as threed:
    create_file("custom.txt", "custom content")
    content = read_file("custom.txt")
    files = list_files()
```

### Model Functions

```python
from noah123d import (
    add_object,              # Add 3D object
    add_object_from_stl,     # Add object from STL
    remove_object,           # Remove object by ID
    get_object,              # Get object by ID
    list_objects,            # List all object IDs
    get_object_count,        # Get number of objects
    clear_objects,           # Remove all objects
    load_stl_with_info,      # Load STL with console output
    analyze_model_content,   # Analyze and display model info
    add_conversion_metadata, # Add conversion metadata
)

with Model("shapes.model") as model:
    # Add objects
    obj_id1 = add_object([[0,0,0], [1,0,0], [0,1,0]], [[0,1,2]])
    obj_id2 = add_object_from_stl("input.stl")
    
    # Query objects
    count = get_object_count()
    objects = list_objects()
    obj_data = get_object(obj_id1)
    
    # Remove objects
    removed = remove_object(obj_id1)
    clear_objects()  # Remove all
    
    # Analysis
    analyze_model_content()
```

## Error Handling

Context-aware functions provide helpful error messages when used incorrectly:

```python
# Using outside any context
add_file("test.txt", "content")
# RuntimeError: add_file() must be called within an Archive context manager

add_thumbnail("thumb.png", b"data")
# RuntimeError: add_thumbnail() must be called within a directory context manager

add_object([[0,0,0]], [[0]])
# RuntimeError: add_object() must be called within a Model context manager

# Using in wrong context type
with Metadata() as metadata:
    add_thumbnail("thumb.png", b"data")  
# TypeError: add_thumbnail() can only be used within a ThreeD context

# Using model functions outside model context
with ThreeD() as threed:
    add_object([[0,0,0]], [[0]])
# RuntimeError: add_object() must be called within a Model context manager
```

## Mixed Usage

You can mix context-aware functions with traditional instance methods:

```python
with Archive("mixed.3mf", 'w') as archive:
    with ThreeD() as threed:
        with Model("mixed.model") as model:
            # Archive: Context function
            add_file("info.txt", "Mixed usage example")
            
            # Archive: Instance method
            archive.add_file("info2.txt", "Another file")
            
            # Directory: Context function
            add_thumbnail("thumb.png", b"thumbnail")
            
            # Directory: Instance method
            threed.create_model_file("backup.model", "<model/>")
            
            # Model: Context function
            obj1 = add_object(vertices, triangles)
            
            # Model: Instance method  
            obj2 = model.add_object(vertices, triangles)
            
            # All methods work on the same contexts
            assert list_contents() == archive.list_contents()
            assert get_object_count() == model.get_object_count() == 2
            assert is_writable() == archive.is_writable()
```

## Benefits

1. **Cleaner Code**: No need to repeat context object names
2. **Less Typing**: Shorter function calls
3. **Consistency**: All functions follow the same pattern
4. **Safety**: Runtime checks ensure functions are used in correct contexts
5. **Backward Compatibility**: Instance methods still work as before

## Import Patterns

```python
# Import specific functions you need
from noah123d import add_file, list_contents, is_writable
from noah123d import add_thumbnail, create_model_file
from noah123d import add_object, get_object_count

# Or import everything if you prefer
from noah123d.archive import *
from noah123d.directories import *
from noah123d import *
```

## Complete Example

```python
from pathlib import Path
from noah123d.archive import Archive, add_file, list_contents, is_writable
from noah123d.directories import ThreeD, add_thumbnail
from noah123d import Model, add_object, get_object_count, analyze_model_content

def create_sample_3mf():
    with Archive("sample.3mf", 'w') as archive:
        # Add files without context object name
        add_file("readme.txt", "Created with context functions")
        add_file("metadata.json", '{"version": "1.0"}')
        
        with ThreeD() as threed:
            # Add thumbnail without context object name
            add_thumbnail("preview.png", b"fake_png_data")
            
            with Model("shapes.model") as model:
                # Add objects without context object name
                triangle_vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
                triangle_faces = [[0, 1, 2]]
                obj_id = add_object(triangle_vertices, triangle_faces, "triangle")
                
                # Check results without context object name
                count = get_object_count()
                print(f"Added {count} objects")
                
                # Analyze without context object name
                analyze_model_content()
        
        # Check archive without context object name
        files = list_contents()
        writable = is_writable()
        print(f"Archive has {len(files)} files, writable: {writable}")

if __name__ == "__main__":
    create_sample_3mf()
```

This approach makes Noah123d code more readable and reduces repetitive context object references while maintaining full backward compatibility.
