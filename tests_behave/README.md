# BDD Tests for Noah123d

This directory contains Behavior-Driven Development (BDD) tests for the Noah123d application using the `behave` framework.

## Structure

```
tests_behave/
├── behave.ini                 # Configuration file for behave
├── run_bdd_tests.py          # Utility script to run tests
├── README.md                 # This file
└── features/
    ├── environment.py        # Test environment setup and teardown
    ├── cli_basic.feature     # Basic CLI functionality tests
    ├── model_processing.feature # Model processing tests  
    ├── error_handling.feature   # Error handling tests
    └── steps/
        ├── cli_basic_steps.py      # Step definitions for CLI tests
        ├── model_processing_steps.py # Step definitions for model processing
        └── error_handling_steps.py   # Step definitions for error handling
```

## Running Tests

### Prerequisites

Make sure you have installed the development dependencies:

```bash
poetry install
```

### Basic Usage

```bash
# Run all BDD tests
cd tests_behave
python run_bdd_tests.py

# Or run behave directly
behave

# Run from project root
cd tests_behave && behave
```

### Advanced Usage

```bash
# Run specific feature file
python run_bdd_tests.py features/cli_basic.feature

# Run tests with specific tags
python run_bdd_tests.py --tags="not @slow"
python run_bdd_tests.py --tags="@integration"

# Run tests matching a name pattern
python run_bdd_tests.py --name="CLI"

# Dry run (show what would be executed)
python run_bdd_tests.py --dry-run

# Verbose output
python run_bdd_tests.py --verbose

# Different output formats
python run_bdd_tests.py --format=json
python run_bdd_tests.py --format=junit

# Don't capture output (useful for debugging)
python run_bdd_tests.py --no-capture
```

## Features Overview

### 1. CLI Basic Functionality (`cli_basic.feature`)

Tests the basic command-line interface functionality:
- Help display
- Version information
- No arguments behavior
- Invalid file handling

**Key scenarios:**
- Display help information
- Display version information  
- Run with no arguments
- Invalid model file handling

### 2. Model Processing (`model_processing.feature`)

Tests the STL model processing capabilities:
- Loading single and multiple models
- Processing directories
- Verbose output
- Model transformations

**Key scenarios:**
- Load single valid STL model
- Process multiple models
- Process models from directory
- Verbose model processing
- Model transformation validation

### 3. Error Handling (`error_handling.feature`)

Tests how the application handles various error conditions:
- Invalid files
- Missing directories
- Permission issues
- Corrupt data

**Key scenarios:**
- Invalid file handling (with examples)
- Invalid directory handling
- Permission denied scenarios
- Invalid mesh data handling

## Tags

The BDD tests use tags to categorize scenarios:

- `@slow` - Tests that take longer to run
- `@integration` - Integration tests that test multiple components
- `@skip` - Tests that should be skipped

## Writing New Tests

### 1. Create Feature Files

Feature files use Gherkin syntax and should be placed in the `features/` directory:

```gherkin
Feature: New Feature
  As a user
  I want some functionality
  So that I can achieve some goal

  Scenario: Basic scenario
    Given some precondition
    When I perform some action
    Then I should see some result
```

### 2. Implement Step Definitions

Step definitions (glue code) should be placed in the `features/steps/` directory:

```python
from behave import given, when, then

@given('some precondition')
def step_some_precondition(context):
    # Setup code
    pass

@when('I perform some action')
def step_perform_action(context):
    # Action code
    context.result = some_function()

@then('I should see some result')
def step_verify_result(context):
    # Assertion code
    assert context.result == expected_value
```

### 3. Use the Context Object

The `context` object is shared between steps and can store:
- Test data
- Command results
- Temporary files
- Configuration

## Best Practices

1. **Keep scenarios focused** - Each scenario should test one specific behavior
2. **Use descriptive names** - Scenario names should clearly describe what's being tested
3. **Leverage tags** - Use tags to organize and filter tests
4. **Clean up resources** - Use the environment.py file for setup/teardown
5. **Make steps reusable** - Write step definitions that can be reused across features
6. **Use examples** - Use scenario outlines with examples for data-driven tests

## Debugging

For debugging failing tests:

```bash
# Run with verbose output and no capture
python run_bdd_tests.py --verbose --no-capture

# Run specific failing scenario
python run_bdd_tests.py --name="specific scenario name"

# Add print statements in step definitions
def step_debug(context):
    print(f"Debug: {context.command_output}")
```

## Integration with Regular Tests

These BDD tests complement the regular unit tests in the `tests/` directory:

- **Unit tests** (`tests/`) - Test individual functions and classes
- **BDD tests** (`tests_behave/`) - Test user scenarios and behavior from the user's perspective

Both test suites should be run as part of your CI/CD pipeline.
