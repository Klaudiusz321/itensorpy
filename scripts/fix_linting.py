#!/usr/bin/env python
"""
A script to fix common linting issues in the codebase.

This script addresses:
1. Trailing whitespace
2. Blank lines containing whitespace
3. No newlines at end of files
4. Missing whitespace around arithmetic operators
"""

import os
import re
import glob

# Function to fix common issues in a file
def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix trailing whitespace
    content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)
    
    # Fix blank lines containing whitespace
    content = re.sub(r'^[ \t]+$', '', content, flags=re.MULTILINE)
    
    # Add whitespace around arithmetic operators
    content = re.sub(r'([a-zA-Z0-9_])([+\-*/])([a-zA-Z0-9_])', r'\1 \2 \3', content)
    content = re.sub(r'([a-zA-Z0-9_])(<=|>=|==|!=)([a-zA-Z0-9_])', r'\1 \2 \3', content)
    
    # Ensure file ends with exactly one newline
    if not content.endswith('\n'):
        content += '\n'
    else:
        content = content.rstrip('\n') + '\n'
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed {file_path}")

# Find all Python files in the src directory
python_files = glob.glob('src/itensorpy/**/*.py', recursive=True)

# Create scripts directory if it doesn't exist
os.makedirs('scripts', exist_ok=True)

# Fix each file
for file_path in python_files:
    try:
        fix_file(file_path)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print(f"Fixed {len(python_files)} files.")
print("Note: This script makes basic fixes. You may still need to run 'black' for more thorough formatting.") 