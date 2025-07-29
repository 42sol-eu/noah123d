# Installation

## Requirements

Noah123d requires:

- **Python 3.10+** (3.12+ recommended)
- **Git** (for development installation)

## Installation Methods

### 📦 PyPI Installation (Recommended)

Install the latest stable release from PyPI:

```bash
pip install noah123d
```

### 🚀 Development Installation

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

### 🐍 Virtual Environment

We recommend using a virtual environment:

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

=== "poetry"

    ```bash
    # Clone and install with poetry
    git clone https://github.com/42sol-eu/noah123d.git
    cd noah123d
    poetry install
    
    # Activate poetry shell
    poetry shell
    ```

## Dependencies

Noah123d automatically installs these dependencies:

- **[numpy-stl](https://pypi.org/project/numpy-stl/)** `^3.2.0` - STL file processing
- **[rich](https://pypi.org/project/rich/)** `^14.1.0` - Beautiful console output
- **[click](https://pypi.org/project/click/)** `^8.2.1` - Command line interface

### Development Dependencies

For development and testing:

- **[pytest](https://pypi.org/project/pytest/)** `^8.4.1` - Testing framework

## Verification

Verify your installation:

### Command Line

```bash
# Check if noah123d CLI is available
noah --help

# Get version information
noah --version
```

### Python Import

```python
# Test basic import
import noah123d
print(noah123d.__version__)

# Test core functions
from noah123d import stl_to_3mf, stl_to_3mf_grid, analyze_3mf
print("✅ Noah123d installed successfully!")
```

### Quick Test

```python
from noah123d import STLConverter

# Create converter instance
converter = STLConverter()
print(f"STLConverter ready: {converter is not None}")

# Test STL info function
from noah123d import get_stl_info
print("✅ All core functions available!")
```

## Platform Support

Noah123d is tested on:

- **Windows** 10/11 (x64)
- **macOS** 12+ (Intel & Apple Silicon)
- **Linux** (Ubuntu 20.04+, CentOS 8+)

## Troubleshooting

### Common Issues

#### ImportError: No module named 'stl'

```bash
# The numpy-stl dependency wasn't installed properly
pip install --upgrade numpy-stl
```

#### Permission Errors (Windows)

```bash
# Run as administrator or use --user flag
pip install --user noah123d
```

#### Python Version Issues

```bash
# Check Python version
python --version

# Upgrade if needed (Windows)
python -m pip install --upgrade python

# Use specific Python version
python3.12 -m pip install noah123d
```

### Getting Help

If you encounter issues:

1. **Check the version**: `pip show noah123d`
2. **Update dependencies**: `pip install --upgrade noah123d`
3. **Create an issue**: [GitHub Issues](https://github.com/42sol-eu/noah123d/issues)
4. **Join discussions**: [GitHub Discussions](https://github.com/42sol-eu/noah123d/discussions)

## Next Steps

After installation:

1. **[Quick Start](quickstart.md)** - Run your first conversion
2. **[Basic Usage](basic-usage.md)** - Learn core concepts
3. **[Grid Layouts](../user-guide/grid-layouts.md)** - Explore advanced features
