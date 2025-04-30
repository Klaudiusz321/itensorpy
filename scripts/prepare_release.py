#!/usr/bin/env python
"""
Prepare the package for release by running checks and building distribution files.

This script:
1. Runs the automated linting fixes
2. Runs tests
3. Builds the package
4. Validates the package
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a shell command and exit if it fails."""
    print(f"\n{description}...")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Error: {description} failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    print(f"{description} completed successfully")

# Create output directory
os.makedirs("dist", exist_ok=True)

# Step 1: Fix linting issues
run_command("python scripts/fix_linting.py", "Fixing linting issues")

# Step 2: Run tests
run_command("pytest", "Running tests")

# Step 3: Install build dependencies if needed
run_command("pip install --upgrade build wheel twine", "Installing build dependencies")

# Step 4: Build package
run_command("python -m build", "Building package")

# Step 5: Check with twine
run_command("twine check dist/*", "Checking distribution files")

print("\nAll checks passed! The package is ready for release.")
print("\nTo upload to Test PyPI:")
print("twine upload --repository-url https://test.pypi.org/legacy/ dist/*")
print("\nTo upload to PyPI:")
print("twine upload dist/*") 