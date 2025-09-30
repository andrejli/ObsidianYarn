# Tests

This directory contains test files for the ObsidianYarn project.

## Test Files

- `test_obsidian_yarn.py` - Main test suite with pytest
- `test_plan` - Sample plan file for testing
- `test.md` - Sample markdown file for testing

## Running Tests

From the project root directory:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_obsidian_yarn.py -v

# Run with coverage (if coverage is installed)
python -m pytest tests/ --cov=. --cov-report=html
```

## Test Structure

The tests cover:
- Plan file reading and parsing
- Template processing
- File indexing and duplicate detection
- Markdown file detection
- Core functionality validation

All tests use relative paths and proper imports to work from the tests directory.