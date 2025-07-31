# Documentation

This directory contains the complete documentation for Noah123d, built with MkDocs and Material theme.

## MkDocs cheat sheet  

```shell
poetry install --with docs
poetry run mkdocs serve
poetry run mkdocs build
poetry run mkdocs gh-deploy
`` 

## Structure

```
docs/
├── assets/                 # Static assets (CSS, JS, images)
│   ├── css/
│   │   └── extra.css      # Custom styling
│   └── js/
│       └── extra.js       # Custom JavaScript
├── getting-started/        # Installation and quick start guides
│   ├── installation.md
│   ├── quickstart.md
│   └── basic-usage.md
├── user-guide/            # Detailed user documentation
│   ├── stl-conversion.md
│   ├── grid-layouts.md
│   ├── 3mf-analysis.md
│   └── batch-processing.md
├── reference/             # API reference documentation
│   ├── index.md
│   ├── converters.md
│   ├── archive3mf.md
│   ├── model.md
│   ├── directory.md
│   └── analyzer.md
├── examples/              # Example usage documentation
│   ├── simple-conversion.md
│   ├── grid-layouts.md
│   ├── advanced-usage.md
│   └── batch-processing.md
├── development/           # Development and contribution guides
│   ├── contributing.md
│   ├── architecture.md
│   └── testing.md
├── index.md              # Main documentation homepage
└── changelog.md          # Release notes and changelog
```

## Building documentation

### Prerequisites

Install documentation dependencies:

```bash
# Using Poetry (recommended)
poetry install --with docs

# Or using pip
pip install mkdocs mkdocs-material mkdocstrings[python] mkdocs-autorefs
```

### Local development

Serve documentation locally with auto-reload:

```bash
# Using Poetry
poetry run mkdocs serve

# Or directly
mkdocs serve
```

The documentation will be available at http://localhost:8000

### Building for production

Build static documentation:

```bash
# Using Poetry
poetry run mkdocs build

# Or directly
mkdocs build
```

Output will be generated in the `site/` directory.

## Writing documentation

### Guidelines

1. **Use clear, concise language**
2. **Include practical examples**
3. **Keep code examples up to date**
4. **Use consistent formatting**
5. **Link between related sections**

### Markdown extensions

The documentation uses several Markdown extensions:

- **Admonitions**: `!!! note`, `!!! warning`, `!!! tip`
- **Code highlighting**: Triple backticks with language
- **Tabs**: `=== "Tab Title"`
- **Mermaid diagrams**: `mermaid` code blocks
- **Math**: LaTeX-style math expressions

### API documentation

API docs are auto-generated from docstrings using mkdocstrings:

```markdown
::: noah123d.STLConverter
    options:
        show_source: false
        show_signature_annotations: true
```

### Examples

Include working code examples:

```python
from noah123d import stl_to_3mf_grid

# This example should actually work
success = stl_to_3mf_grid(
    stl_path="part.stl",
    output_path="grid.3mf",
    count=4,
    grid_cols=2
)
```

## Deployment

Documentation is automatically deployed to GitHub Pages via GitHub Actions when changes are pushed to the main branch.

### Manual deployment

To deploy manually:

```bash
poetry run mkdocs gh-deploy
```

## Configuration

Documentation configuration is in `mkdocs.yml` at the project root.

Key configuration sections:
- **nav**: Site navigation structure
- **theme**: Material theme settings
- **plugins**: Enabled plugins and their settings
- **markdown_extensions**: Enabled Markdown extensions

## Contributing

To contribute to the documentation:

1. Follow the [Contributing guide](development/contributing.md)
2. Make changes to the relevant `.md` files
3. Test locally with `mkdocs serve`
4. Submit a pull request

## Troubleshooting

### Common issues

**Build fails with import errors**:
```bash
# Make sure the package is installed in development mode
poetry install -e .
```

**Missing dependencies**:
```bash
# Install all documentation dependencies
poetry install --with docs
```

**Links not working**:
- Check that relative paths are correct
- Use `mkdocs serve` to test locally
- Verify all referenced files exist

### Getting help

- Check existing documentation
- Search issues in the repository
- Ask in GitHub Discussions
- Create a new issue if needed
