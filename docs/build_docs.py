#!/usr/bin/env python3
"""
Local Sphinx Documentation Build Script for SPROCLIB

This script builds the documentation locally for testing and preview.
Usage: python build_docs.py [clean]

Arguments:
    clean    Remove existing build directory before building
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    """Build the documentation locally."""
    # Get script directory
    docs_dir = Path(__file__).parent
    source_dir = docs_dir / "source"
    build_dir = docs_dir / "build"
    html_dir = build_dir / "html"
    
    print("🔧 SPROCLIB Documentation Builder")
    print("=" * 40)
    
    # Check if we should clean first
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        print("🧹 Cleaning existing build directory...")
        if build_dir.exists():
            shutil.rmtree(build_dir)
            print("   ✓ Build directory cleaned")
    
    # Ensure build directory exists
    build_dir.mkdir(exist_ok=True)
    
    # Build command
    cmd = [
        "sphinx-build",
        "-b", "html",           # HTML builder
        "-E",                   # Don't use cached environment
        str(source_dir),        # Source directory
        str(html_dir)           # Output directory
    ]
    
    print(f"📖 Building documentation...")
    print(f"   Source: {source_dir}")
    print(f"   Output: {html_dir}")
    print()
    
    try:
        # Run sphinx-build
        result = subprocess.run(cmd, cwd=docs_dir, check=True)
        
        print()
        print("✅ Documentation build completed successfully!")
        print(f"📂 Output directory: {html_dir}")
        print(f"🌐 Open in browser: file:///{html_dir}/index.html")
        
        # Try to open in browser (Windows)
        if os.name == 'nt':
            try:
                os.startfile(str(html_dir / "index.html"))
                print("🚀 Opening documentation in your default browser...")
            except:
                pass
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with return code {e.returncode}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Error: sphinx-build not found. Please install Sphinx:")
        print("   pip install -r requirements-docs.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()
