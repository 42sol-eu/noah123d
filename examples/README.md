# Noah123D Examples

This directory contains comprehensive examples demonstrating how to use the Noah123D library for creating and managing 3MF archives.

## Examples Overview

### 1. `example_3mf.py` - Basic Usage
**Purpose**: Demonstrates fundamental usage of Archive3mf, Directory, and Model classes.

**Key Features**:
- Creating a simple 3MF archive
- Adding basic geometric shapes (cube)
- Using context managers properly
- Reading back created archives
- Basic metadata management

**Best for**: Getting started with Noah123D, understanding the basic API.

### 2. `example_batch_processing.py` - Complex Multi-Model Assembly
**Purpose**: Shows advanced features for creating complex 3MF files with multiple models.

**Key Features**:
- Multiple models in a single archive (cylinder, pyramid, assembly)
- Complex geometry generation (procedural shapes)
- Rich metadata with JSON files
- Directory structure organization
- Model composition and transformation

**Best for**: Creating complex assemblies, understanding model relationships, advanced metadata.

### 3. `example_advanced_usage.py` - Advanced Context Management
**Purpose**: Demonstrates advanced context manager usage, error handling, and batch processing.

**Key Features**:
- Error handling and recovery patterns
- Nested context manager usage
- Parent context awareness
- Batch processing multiple archives
- Safe resource management
- Complex directory hierarchies

**Best for**: Production-ready code, error handling, batch operations, advanced patterns.

## Running the Examples

Make sure you have the Noah123D package installed:

```bash
# Install the package in development mode
poetry install

# Run individual examples
poetry run python examples/example_3mf.py
poetry run python examples/example_batch_processing.py
poetry run python examples/example_advanced_usage.py
```

## Example Output Files

Each example creates 3MF archive files:

- `example_3mf.py` → `arc.3mf`
- `example_batch_processing.py` → `complex_assembly.3mf`
- `example_advanced_usage.py` → `safe_operations.3mf`, `nested_context.3mf`, and batch files

## Key Concepts Demonstrated

### Context Managers
All examples show proper usage of Python context managers (`with` statements) for:
- Automatic resource cleanup
- Parent-child context relationships using `contextvars`
- Error handling and recovery

### Archive Structure
Examples demonstrate creating organized 3MF archives with:
- `3D/` directory for model files
- `Metadata/` directory for additional information
- `Textures/` directory for texture resources (when applicable)

### Model Management
- Creating geometric shapes programmatically
- Managing multiple objects within models
- Model composition and transformation

### Error Handling
- Safe operations with try/catch blocks
- Graceful error recovery
- Resource cleanup on failure

### Metadata Management
- JSON-based metadata files
- Build information tracking
- Material definitions
- Validation and verification data

## Best Practices Shown

1. **Always use context managers** - Ensures proper resource cleanup
2. **Validate input data** - Check vertices and triangles before creating objects
3. **Organize archive structure** - Use logical directory hierarchies
4. **Include metadata** - Document your 3MF files with build information
5. **Handle errors gracefully** - Provide fallbacks and cleanup on failure
6. **Use meaningful names** - Name your objects and files descriptively

## Common Patterns

### Basic Archive Creation
```python
with Archive3mf(output_path, 'w') as archive:
    with Directory('3D') as models_dir:
        with Model() as model:
            obj_id = model.add_object(vertices, triangles, name="MyObject")
```

### Reading Archives
```python
with Archive3mf(input_path, 'r') as archive:
    contents = archive.list_contents()
    with Directory('3D') as models_dir:
        with Model() as model:
            objects = model.list_objects()
```

### Error Handling
```python
try:
    with Archive3mf(path, 'w') as archive:
        # ... operations ...
except Exception as e:
    print(f"Error: {e}")
    # cleanup if needed
```

## Next Steps

After running these examples:

1. Try modifying the geometric shapes
2. Add your own metadata fields
3. Experiment with different directory structures
4. Create your own shape generation functions
5. Integrate with STL file loading using `numpy-stl`

For more advanced usage, see the test files in the `tests/` directory.
