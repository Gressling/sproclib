#!/bin/bash
# Local Sphinx Documentation Build Script for SPROCLIB
# Usage: ./sphinx.sh [clean]

echo "🔧 SPROCLIB Documentation Builder"
echo "========================================"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if we're in a virtual environment, if not, try to activate one
if [[ -z "$VIRTUAL_ENV" ]]; then
    if [[ -f "../.venv/bin/activate" ]]; then
        echo "🔧 Activating virtual environment..."
        source "../.venv/bin/activate"
    fi
fi

if [[ "$1" == "clean" ]]; then
    echo "🧹 Cleaning existing build directory..."
    if [[ -d "build" ]]; then
        rm -rf "build"
        echo "   ✓ Build directory cleaned"
    else
        echo "   ✓ No build directory to clean"
    fi
fi

echo "📖 Building documentation..."
echo "   Source: source"
echo "   Output: build/html"
echo ""

# Check if sphinx-build is available
if ! command -v sphinx-build &> /dev/null; then
    echo "❌ sphinx-build command not found!"
    echo "Installing documentation dependencies..."
    pip install -r requirements-docs.txt
    echo ""
fi

sphinx-build -b html -E source build/html
BUILD_EXIT_CODE=$?

if [[ $BUILD_EXIT_CODE -eq 0 ]]; then
    echo ""
    echo "✅ Documentation build completed successfully!"
    echo "📂 Output directory: build/html"
    echo "🌐 Open in browser: file://$PWD/build/html/index.html"
    echo ""
    echo "🚀 Opening documentation in your default browser..."
    open "build/html/index.html"
else
    echo ""
    echo "❌ Build failed with return code $BUILD_EXIT_CODE"
    echo "Make sure Sphinx is installed: pip install -r requirements-docs.txt"
    read -p "Press any key to continue..."
fi
