# Changelog

All notable changes to Noah123d will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation with MkDocs
- Grid layout system with intelligent spacing
- 3MF file analysis capabilities
- Rich console output formatting
- CLI interface for all functions
- Batch processing capabilities

## [2025.0.1] - 2025-07-29

### Added
- Initial release of Noah123d
- STL to 3MF conversion functionality
- Core Archive3mf, Directory, and Model classes
- Basic grid layout support
- STL file analysis and validation
- Performance optimizations for large files

### Features
- **STL Conversion**: Convert binary and ASCII STL files to 3MF format
- **Grid Layouts**: Create rectangular grids with automatic spacing
- **3MF Analysis**: Extract model information and statistics
- **High Performance**: Process 80,000+ triangles/second
- **Rich Metadata**: Detailed conversion statistics and model info

### Technical Details
- Python 3.10+ support
- numpy-stl integration for STL processing
- Rich library for beautiful console output
- Click framework for CLI interface
- Comprehensive type hints and documentation

### Performance
- Optimized grid generation with geometry reuse
- Memory-efficient handling of large models
- Vectorized position calculations
- Multi-threaded processing where applicable

### Examples Included
- Basic STL conversion examples
- Grid layout demonstrations
- 3MF analysis workflows
- Advanced usage patterns
- Batch processing scripts

## [Future Releases]

### Planned Features
- Hexagonal and circular grid patterns
- Multi-material 3MF support
- Advanced object transformations (rotation, scaling)
- Integration with popular 3D printing slicers
- Web interface for grid configuration
- Support for additional 3D formats (OBJ, PLY)

### Performance Improvements
- GPU acceleration for large grids
- Streaming processing for massive files
- Advanced memory management
- Parallel grid generation

---

## Release Notes Format

Each release includes:
- **Added**: New features and capabilities
- **Changed**: Modifications to existing functionality  
- **Deprecated**: Features planned for removal
- **Removed**: Features removed in this release
- **Fixed**: Bug fixes and corrections
- **Security**: Security-related changes

## Version Numbering

Noah123d uses [Calendar Versioning](https://calver.org/) with the format:
- **YYYY.MINOR.PATCH** (e.g., 2025.0.1)
- **YYYY**: Year of release
- **MINOR**: Feature releases within the year
- **PATCH**: Bug fixes and small improvements

## Support

For questions about releases:
- **Issues**: [GitHub Issues](https://github.com/42sol-eu/noah123d/issues)
- **Discussions**: [GitHub Discussions](https://github.com/42sol-eu/noah123d/discussions)
- **Documentation**: [Read the Docs](https://noah123d.readthedocs.io/)
