# iTensorPy Packaging Improvements

This document details the changes made to prepare the iTensorPy package for PyPI deployment.

## Key Fixes

### 1. Encoding Issues

- Fixed encoding issue in `setup.py` by explicitly specifying UTF-8 when reading the README file:
  ```python
  long_description=open("README.md", encoding="utf-8").read()
  ```
- Used UTF-8 encoding throughout the codebase to ensure consistent handling of characters
- Fixed variable naming in `curvature.py` to avoid name collisions and encoding issues

### 2. Linting and Code Style

- Created a `.flake8` configuration file to ignore less critical linting issues temporarily
- Added a `fix_linting.py` script to automatically address common linting problems:
  - Trailing whitespace
  - Blank lines containing whitespace
  - Missing whitespace around operators
  - Newline issues at end of files
- Properly documented imports and added `__all__` list in `__init__.py`
- Fixed ambiguous variable names (e.g., replaced `l` with `m` where needed)

### 3. Package Structure and Metadata

- Created `MANIFEST.in` to ensure all necessary files are included in the package
- Updated `setup.cfg` with comprehensive metadata
- Added pre-commit hooks configuration for ongoing code quality maintenance
- Added a release preparation script (`prepare_release.py`) to automate checks

## Testing Procedure

Before releasing to PyPI, we recommend:

1. Run the automated fixes: `python scripts/fix_linting.py`
2. Run the test suite: `pytest` 
3. Test build the package: `python -m build`
4. Validate the distribution files: `twine check dist/*`
5. Install locally from the built package for a final verification
6. Upload to Test PyPI first before the main PyPI repository

## Future Improvements

Some linting issues are still present and should be addressed in future releases:

- Cleanup of unused imports throughout the codebase
- Better docstring formatting
- Comprehensive implementation of type hints
- Use consistent naming conventions for all variables
- Apply a code formatter like Black to ensure consistent style

This initial set of fixes should resolve the critical deployment issues and provide a foundation for continued improvements. 