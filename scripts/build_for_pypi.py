#!/usr/bin/env python
"""
Build a wheel file that avoids the license-file metadata issue.

This script:
1. Creates temporary copies of our minimal configuration files
2. Builds the wheel with these minimal files
3. Restores the original files

Usage:
    python scripts/build_for_pypi.py
"""

import os
import shutil
import subprocess
import tempfile

def backup_file(filepath):
    """Backup a file if it exists."""
    if os.path.exists(filepath):
        backup_path = f"{filepath}.bak"
        shutil.copy2(filepath, backup_path)
        return True
    return False

def restore_file(filepath):
    """Restore a file from backup if the backup exists."""
    backup_path = f"{filepath}.bak"
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, filepath)
        os.remove(backup_path)
        return True
    return False

def build_wheel():
    """Build a wheel file with minimal configuration."""
    try:
        # Clean previous build artifacts
        for path in ["build", "dist", "src/itensorpy.egg-info"]:
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
        
        # Backup original files
        backup_file("setup.py")
        backup_file("MANIFEST.in")
        backup_file("pyproject.toml")
        
        # Copy minimal files
        shutil.copy2("setup.minimal.py", "setup.py")
        shutil.copy2("MANIFEST.minimal.in", "MANIFEST.in")
        shutil.copy2("pyproject.minimal.toml", "pyproject.toml")
        
        # Build the wheel
        print("Building wheel with minimal configuration...")
        subprocess.run(["python", "setup.py", "bdist_wheel"], check=True)
        
        # Check the wheel with twine
        print("\nChecking wheel with twine...")
        result = subprocess.run(["twine", "check", "dist/*"], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
            
        print("\nWheel built successfully and passes twine check!")
        return True
    
    except Exception as e:
        print(f"Error building wheel: {e}")
        return False
    
    finally:
        # Restore original files
        restore_file("setup.py")
        restore_file("MANIFEST.in")
        restore_file("pyproject.toml")

if __name__ == "__main__":
    # Ensure the minimal files exist
    if not os.path.exists("setup.minimal.py"):
        print("Error: setup.minimal.py not found")
        exit(1)
    if not os.path.exists("MANIFEST.minimal.in"):
        print("Error: MANIFEST.minimal.in not found")
        exit(1)
    if not os.path.exists("pyproject.minimal.toml"):
        print("Error: pyproject.minimal.toml not found")
        exit(1)
        
    # Build the wheel
    success = build_wheel()
    
    if success:
        print("\nTo upload to Test PyPI:")
        print("python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*")
        print("\nTo upload to PyPI:")
        print("python -m twine upload dist/*")
    else:
        print("\nWheel building failed!") 