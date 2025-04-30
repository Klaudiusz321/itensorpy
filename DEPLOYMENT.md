# iTensorPy Deployment Guide

## Summary of Fixes

1. **Encoding Issues Fixed**: 
   - Added explicit UTF-8 encoding for README.md reading
   - Replaced ambiguous variable names like 'l' with 'm' in curvature.py
   - Fixed string formatting throughout the codebase

2. **Code Linting and Documentation**:
   - Created scripts/fix_linting.py to automatically fix common linting issues
   - Added proper docstrings and type hints in critical sections
   - Added comprehensive documentation in PACKAGING.md for future reference

3. **Package Structure**:
   - Created MANIFEST.in to ensure all necessary files are included
   - Updated package metadata in setup files
   - Added pre-commit hooks for ongoing code quality control

## Installation Options

### Direct Installation from GitHub

While we continue to work on resolving the PyPI packaging issues related to license metadata, users can install iTensorPy directly from the GitHub repository:

```bash
pip install git+https://github.com/yourusername/itensorpy.git
```

### Local Development Installation

For developers who want to work on iTensorPy:

```bash
git clone https://github.com/yourusername/itensorpy.git
cd itensorpy
pip install -e .
```

### Manual Installation

If you've downloaded a release:

1. Download the latest release from GitHub
2. Extract the files
3. Run `pip install -e .` in the extracted directory

## Potential PyPI Upload Instructions

There are a few remaining issues with the package metadata that need to be fixed before publishing to PyPI:

1. **License Metadata Issue**: The wheel file includes invalid license-file metadata fields. This appears to be an issue between the different ways setuptools and twine handle licenses.

2. **Solution Options**:
   - Use a temporary workaround with a custom setup.py that omits license fields
   - Wait for an update to setuptools/twine to resolve the incompatibility issue
   - Try using an older version of setuptools (e.g., 65.0.0) which was reported to handle licenses differently

3. **Other PyPI Preparation Steps**:
   - Change the GitHub URLs in setup files to match your actual repository
   - Update the author email to a valid contact
   - Run the final PyPI upload commands:
   
   ```bash
   # For TestPyPI
   python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
   
   # For production PyPI
   python -m twine upload dist/*
   ```

## Next Steps

1. Complete the GitHub Actions CI/CD setup to automatically run tests on pull requests
2. Fix the remaining license metadata issue using one of the options above
3. Add comprehensive documentation with examples on a documentation site
4. Include performance benchmarks in the documentation

The package is functionally ready for use but still has some packaging metadata challenges to overcome. 