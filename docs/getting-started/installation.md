# Installation

## Requirements

Noah123d requires:

- **Python 3.10+** (3.12+ recommended)

## Installation methods

### 📦 PyPI installation (Recommended)

Install the latest stable release from PyPI:

```bash
pip install noah123d
```

### 🚀 Development installation

For the latest features and development version:

```bash
# Clone the repository
git clone https://github.com/42sol-eu/noah123d.git
cd noah123d

# Install with poetry (recommended)
poetry install

# Or install with pip
pip install -e .
```

### 🐍 Virtual environment

We recommend using a virtual environment:



=== "poetry"

    ```bash
    # Clone and install with poetry
    git clone https://github.com/42sol-eu/noah123d.git
    cd noah123d
    poetry install
    
    # Activate poetry shell
    poetry shell
    ```

=== "venv"

    ```bash
    # Create virtual environment
    python -m venv noah123d-env
    
    # Activate (Windows)
    noah123d-env\Scripts\activate
    
    # Activate (Linux/macOS)
    source noah123d-env/bin/activate
    
    # Install noah123d
    pip install noah123d
    ```

=== "conda"

    ```bash
    # Create conda environment
    conda create -n noah123d python=3.12
    conda activate noah123d
    
    # Install noah123d
    pip install noah123d
    ```

## Dependencies

Noah123d automatically installs these dependencies:

- **[numpy-stl](https://pypi.org/project/numpy-stl/)** `^3.2.0` - STL file processing
- **[rich](https://pypi.org/project/rich/)** `^14.1.0` - Beautiful console output
- **[click](https://pypi.org/project/click/)** `^8.2.1` - Command line interface

### Development dependencies

For development and testing:

- **[pytest](https://pypi.org/project/pytest/)** `^8.4.1` - Testing framework
- **[ruff](https://pypi.org/project/ruff/)** `^0.0.292` - Linter
- **[mkdocs](https://pypi.org/project/mkdocs/)** `^1.5.3` - Documentation generator

## Verification

Verify your installation:

### Command line

```bash
# Check if noah123d CLI is available
noah --help

# Get version information
noah --version
```

### Python import

```python
# Test basic import
import noah123d
print(noah123d.__version__)

# Test core functions
from noah123d import stl_to_3mf, stl_to_3mf_grid, analyze_3mf
print("✅ Noah123d installed successfully!")
```

### Quick test

```python
from noah123d import STLConverter

# Create converter instance
converter = STLConverter()
print(f"STLConverter ready: {converter is not None}")

# Test STL info function
from noah123d import get_stl_info
print("✅ All core functions available!")
```

## Platform support

Noah123d is tested on:

- **Windows** 10/11 (x64)
- **macOS** 12+ (Intel & Apple Silicon)
- **Linux** (Ubuntu 20.04+, CentOS 8+)

## Troubleshooting

### Common issues

#### ImportError: No module named 'stl'

```bash
# The numpy-stl dependency wasn't installed properly
pip install --upgrade numpy-stl
```

#### Permission errors (Windows)

```bash
# Run as administrator or use --user flag
pip install --user noah123d
```

#### Python version issues

```bash
# Check Python version
python --version

# Upgrade if needed (Windows)
python -m pip install --upgrade python

# Use specific Python version
python3.12 -m pip install noah123d
```

### Getting help

If you encounter issues:

1. **Check the version**: `pip show noah123d`
2. **Update dependencies**: `pip install --upgrade noah123d`
3. **Create an issue**: [GitHub issues](https://github.com/42sol-eu/noah123d/issues)
4. **Join discussions**: [GitHub discussions](https://github.com/42sol-eu/noah123d/discussions)

## Next steps

After installation:

1. **[Quick start](quickstart.md)** - run your first conversion
2. **[Basic usage](basic-usage.md)** - learn core concepts
3. **[Grid layouts](../user-guide/grid-layouts.md)** - explore advanced features
