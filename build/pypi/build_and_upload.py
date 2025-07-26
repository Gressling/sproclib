#!/usr/bin/env python3
"""
Script to build and upload package to PyPI
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {description} failed")
        print(f"STDERR: {result.stderr}")
        sys.exit(1)
    
    print(f"Success: {description} completed")
    return result.stdout

def main():
    # Clean previous builds
    run_command("rmdir /s /q build dist *.egg-info 2>nul || echo 'Nothing to clean'", "Cleaning previous builds")
    
    # Build the package
    run_command("python -m build", "Building package")
    
    # Check the distribution
    run_command("python -m twine check dist/*", "Checking distribution")
    
    # Upload to TestPyPI first (recommended)
    print("\nTo upload to TestPyPI:")
    print("python -m twine upload --repository testpypi dist/*")
    
    print("\nTo upload to PyPI:")
    print("python -m twine upload dist/*")
    
    print("\nMake sure you have:")
    print("1. pip install build twine")
    print("2. Created accounts on PyPI and TestPyPI")
    print("3. Configured your credentials")

if __name__ == "__main__":
    main()
