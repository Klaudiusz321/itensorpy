#!/usr/bin/env python
"""
Build a wheel file using an older version of setuptools.

This script:
1. Creates a temporary virtual environment
2. Installs an older version of setuptools known to work with license fields
3. Builds the wheel in this environment
4. Checks the wheel with twine

Usage:
    python scripts/build_with_old_setuptools.py
"""

import os
import subprocess
import sys
import tempfile
import venv
from pathlib import Path

def create_venv(venv_path):
    """Create a virtual environment at the specified path."""
    print(f"Creating virtual environment at {venv_path}...")
    venv.create(venv_path, with_pip=True)

def get_venv_python(venv_path):
    """Get the path to the Python executable in the virtual environment."""
    if sys.platform == 'win32':
        return os.path.join(venv_path, 'Scripts', 'python.exe')
    return os.path.join(venv_path, 'bin', 'python')

def build_with_old_setuptools():
    """Build a wheel using an older version of setuptools."""
    # Create a temporary directory for the virtual environment
    with tempfile.TemporaryDirectory() as temp_dir:
        venv_path = os.path.join(temp_dir, 'venv')
        create_venv(venv_path)
        
        python_exe = get_venv_python(venv_path)
        
        # Install older setuptools version
        print("Installing older setuptools version...")
        subprocess.run([python_exe, "-m", "pip", "install", "setuptools==65.5.0", "wheel", "twine"], check=True)
        
        # Clean previous build artifacts
        for path in ["build", "dist", "src/itensorpy.egg-info"]:
            if os.path.exists(path):
                if os.path.isdir(path):
                    import shutil
                    shutil.rmtree(path)
                else:
                    os.remove(path)
        
        # Build the wheel
        print("\nBuilding wheel with setuptools 65.5.0...")
        subprocess.run([python_exe, "setup.py", "bdist_wheel"], check=True)
        
        # Check the wheel with twine
        print("\nChecking wheel with twine...")
        result = subprocess.run([python_exe, "-m", "twine", "check", "dist/*"], capture_output=True, text=True)
        print(result.stdout)
        
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        
        print("\nWheel built successfully with older setuptools!")
        return True

if __name__ == "__main__":
    success = build_with_old_setuptools()
    
    if success:
        print("\nTo upload to Test PyPI:")
        print("python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*")
        print("\nTo upload to PyPI:")
        print("python -m twine upload dist/*")
    else:
        print("\nWheel building failed!") 