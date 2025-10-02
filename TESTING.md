# Testing Guide for LUNTRA Calculator MVP

This document provides comprehensive information about running tests in the LUNTRA Calculator MVP project.

## Test Structure

The test suite is organized into three main categories:

### Test Files
- **`test_app_logic.py`** - Unit tests for application logic and business rules
- **`test_formulas.py`** - Tests for financial calculation formulas and mathematical accuracy
- **`test_integration.py`** - End-to-end integration tests for complete workflows

### Test Markers

Tests are organized using pytest markers for easy filtering:

- `@pytest.mark.unit` - Unit tests for individual functions and classes
- `@pytest.mark.integration` - Integration tests for complete workflows  
- `@pytest.mark.formulas` - Tests for financial calculation formulas
- `@pytest.mark.house_hack` - Tests specific to House-Hack model
- `@pytest.mark.whole_unit` - Tests specific to Whole Unit model
- `@pytest.mark.ui` - Tests for Streamlit UI components (planned)
- `@pytest.mark.slow` - Tests that take longer to run (planned)

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests with short error summary
pytest --tb=short

# Run specific test file
pytest tests/test_formulas.py

# Run specific test function
pytest -k test_whole_unit_workflow_complete
```

### Using Test Markers

```bash
# Run all whole unit tests
pytest -m "whole_unit"

# Run all house-hack tests  
pytest -m "house_hack"

# Run all formula tests
pytest -m "formulas"

# Run all integration tests
pytest -m "integration"

# Combine markers (AND)
pytest -m "whole_unit and formulas"

# Combine markers (OR)
pytest -m "whole_unit or house_hack"
```

### Test Runner Script

Use the convenient test runner for common scenarios:

```bash
# Run all tests
python3 run_tests.py --all

# Run specific categories
python3 run_tests.py --whole-unit
python3 run_tests.py --house-hack
python3 run_tests.py --formulas
python3 run_tests.py --integration

# Run with coverage report
python3 run_tests.py --coverage

# Fast run (minimal output)
python3 run_tests.py --fast

# Verbose output
python3 run_tests.py --verbose
```

## Test Coverage

### Running with Coverage

```bash
# Basic coverage report
pytest --cov=calculator --cov=app

# Coverage with missing lines
pytest --cov=calculator --cov=app --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=calculator --cov=app --cov-report=html

# Using test runner
python3 run_tests.py --coverage
```

### Coverage Reports

HTML coverage reports are generated in the `htmlcov/` directory. Open `htmlcov/index.html` to view detailed coverage information.

## Test Configuration

The project uses `pytest.ini` for configuration with these settings:

- **Test Discovery**: Automatically finds tests in the `tests/` directory
- **Output Format**: Short traceback format with verbose output
- **Error Handling**: Stop after 3 failures with summary of all results
- **Markers**: Custom markers are registered to avoid warnings

## Writing Tests

### Test Organization

```python
import pytest

@pytest.mark.whole_unit
@pytest.mark.formulas
class TestWholeUnitCalculations:
    """Test whole unit specific calculations"""
    
    def test_cash_flow_calculation(self):
        """Test monthly cash flow calculation"""
        # Test implementation
        pass
```

### Test Categories

- **Unit Tests**: Test individual functions with known inputs/outputs
- **Integration Tests**: Test complete user workflows from input to result
- **Formula Tests**: Test mathematical accuracy of financial calculations
- **Edge Case Tests**: Test boundary conditions and error handling

### Best Practices

1. **Use descriptive test names** that explain what is being tested
2. **Include docstrings** that describe the test purpose
3. **Use appropriate markers** to categorize tests
4. **Test both success and failure scenarios**
5. **Include edge cases and boundary conditions**
6. **Keep tests independent** - each test should be able to run alone

## Common Test Scenarios

### House-Hack Model Tests
```bash
# Run all house-hack tests
pytest -m "house_hack"

# Run specific house-hack workflow
pytest -k test_house_hack_workflow_complete
```

### Whole Unit Model Tests
```bash
# Run all whole unit tests  
pytest -m "whole_unit"

# Run specific whole unit calculations
pytest tests/test_formulas.py::TestWholeUnitFormulas
```

### Formula Accuracy Tests
```bash
# Run all formula tests
pytest -m "formulas"

# Run specific formula category
pytest tests/test_formulas.py::TestBasicFinancialFormulas
```

## Debugging Tests

### Verbose Output
```bash
# Show detailed test output
pytest -v --tb=long

# Show all test output (including passed tests)
pytest -v -s
```

### Running Single Tests
```bash
# Run specific test method
pytest tests/test_formulas.py::TestBasicFinancialFormulas::test_monthly_mortgage_payment_formula

# Run with debugger on failure
pytest --pdb tests/test_app_logic.py
```

### Test Performance
```bash
# Show slowest tests
pytest --durations=10

# Profile test execution
pytest --profile
```

## Continuous Integration

The test suite is designed to run in CI environments with:

- Clear exit codes (0 for success, non-zero for failure)
- Machine-readable output formats
- Coverage reporting
- Parallel execution support (when needed)

## Troubleshooting

### Common Issues

1. **"No tests collected"** - Check that test files match naming pattern (`test_*.py`)
2. **Import errors** - Ensure the project directory is in Python path
3. **Marker warnings** - Verify markers are registered in `pytest.ini`
4. **Coverage not found** - Install `pytest-cov` package

### Getting Help

```bash
# Show pytest help
pytest --help

# Show available markers
pytest --markers

# Show test collection without running
pytest --collect-only
```