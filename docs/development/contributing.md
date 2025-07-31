# Contributing to Noah123d

Thank you for your interest in contributing to `noah123d`! This document provides guidelines for contributing to the project.

## Introduction 
### Definition

Contribution is the act of implementing features added to a release of the package.
Multiple bug-fixes, extensive documentation and extensions of tests over a longer period of time will be deemed the same as implementing new features.

### Process 

Before you commit of implementing a new feature be sure that the authors understand the purpose of the feature and had the opportunity to understand the integration into the package.

Please be aware that the maintenance of more complex features or dependencies to other packages might be the reason, why the authors hesitate to accept your contribution.   
Remember that it is always an option to create you own package on top of this package to share your great ideas with the world, as we did with `noah123d`. It is also possible and likely that parts of the library will be integrated into `build123d` as the authors of this package deem them to fit into their toolset. 


### Recognition

Contributors are recognized in:
- `CONTRIBUTORS.md` file
- Release notes
- Documentation acknowledgments

## Getting started

### Contribution and licensing

- This project is an open source project developed under the [MIT License](https://opensource.org/licenses/MIT) - your work will therefore be under the same license as long as it is part of this package.

> [!Note]
> If you think you contributed much to this package, feel free to contact the owners to name you as one of the authors. 

> [!Important]
> Licensing is done by the owner on a release bases and may change during the process of development, if you contributed to the project you will be informed about any license change and will automatically get a at least 3 year usage of the package without any restrictions.
> **If you do not agree with this possibility please do not contribute to the project but fork it.**

If you have any further questions, feel free to raise an issue or join our discussions on opened issues on GitHub.

### Development setup

> [!Note]
> You will need a free github accout for contributing

1. **Fork the repository**:
   - Go to the [Noah123d GitHub page](https://github.com/42sol-eu/noah123d) and click on the "Fork" button.
2. **Clone the repository**:
   ```bash
   git clone https://github.com/{your-accont}/noah123d.git
   cd noah123d
   ```
3. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python -
   which poetry
   poetry --version
   ```
   You should see a version output of `>2.0.0`
4. **Install dependencies**:
   ```bash
   poetry install --with dev,docs
   ```
5. **Activate the virtual environment**:
   ```bash
   poetry self add poetry-plugin-shell
   poetry shell
   ```
6. **Run tests to verify setup**:
   ```bash
   pytest
   ```

### Development environment

We recommend using VS Code with these extensions:
- Python
- Pylance
- Python Docstring Generator

## Types of contributions

### Documentation updates

Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add examples or use cases
- Improve API documentation
- Translate documentation (future)

### Code contributions (new features and bug fixes)

## Development workflow

### 1. create a branch

```bash
git checkout -b feature/your-feature-name
# Or
git checkout -b fix/issue-number-description
```

### 2. make changes

- Follow the [coding standards](#coding-standards)
- Add tests for new functionality
- Update documentation as needed
- Keep commits small and focused

### 3. test changes

Run the full test suite:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=noah123d

# Run specific test file
pytest tests/test_converters.py

# Run tests in verbose mode
pytest -v
```

### 4. documentation

Build and test documentation:

```bash
# Install docs dependencies
poetry install --with docs

# Serve docs locally
mkdocs serve

# Build docs
mkdocs build
```

### 5. submit pull request

1. Push your branch to your fork
2. Create a pull request with:
   - Clear title and description
   - Reference to related issues
   - Description of changes made
   - Any breaking changes noted
