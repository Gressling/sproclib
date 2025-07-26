#!/bin/bash
# ========================================================================
# SPROCLIB PyPI Build and Upload Script (Unix/macOS)
# ========================================================================
# Interactive script for building and uploading packages to PyPI
# 
# This script provides a step-by-step process for:
# 1. Installing required tools
# 2. Cleaning previous builds  
# 3. Building the package
# 4. Checking the distribution
# 5. Interactive upload to TestPyPI or PyPI
# ========================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${CYAN}================================${NC}"
echo -e "${CYAN}SPROCLIB PyPI Build and Upload${NC}"
echo -e "${CYAN}================================${NC}"
echo ""

# Get the directory where this script is located and go to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}Working directory: $PROJECT_ROOT${NC}"
echo ""

# Check if .pypirc exists in project directory and copy to user home
if [[ -f ".pypirc" ]]; then
    echo -e "${YELLOW}Found .pypirc in project directory, copying to user home...${NC}"
    cp ".pypirc" "$HOME/.pypirc"
    echo -e "${GREEN}.pypirc copied to $HOME/.pypirc${NC}"
    echo ""
fi

# Check if required tools are installed
echo -e "${BLUE}Checking required tools...${NC}"

if ! python -c "import build" 2>/dev/null; then
    echo -e "${YELLOW}Installing 'build' package...${NC}"
    pip install build
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}Error: Failed to install 'build' package${NC}"
        exit 1
    fi
fi

if ! python -c "import twine" 2>/dev/null; then
    echo -e "${YELLOW}Installing 'twine' package...${NC}"
    pip install twine
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}Error: Failed to install 'twine' package${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✓ Required tools are available${NC}"
echo ""

# Step 1: Clean previous builds
echo -e "${BOLD}[1/5] Cleaning previous builds...${NC}"

# Remove Python's build directory (but protect our scripts/ directory)
if [[ -d "build" ]] && [[ ! -f "scripts/README.md" ]] && [[ -d "build/lib" ]]; then
    rm -rf build/
    echo -e "${GREEN}Removed Python build directory${NC}"
fi

if [[ -d "dist" ]]; then
    rm -rf dist/
    echo -e "${GREEN}Removed dist directory${NC}"
fi

# Clean all .egg-info directories
for egg_info in *.egg-info; do
    if [[ -d "$egg_info" ]]; then
        rm -rf "$egg_info"
        echo -e "${GREEN}Removed $egg_info${NC}"
    fi
done

echo -e "${GREEN}✓ Cleanup completed${NC}"
echo ""

# Step 2: Build package
echo -e "${BOLD}[2/5] Building package...${NC}"
if ! python -m build; then
    echo -e "${RED}Error: Build failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Package built successfully${NC}"
echo ""

# Step 3: Check distribution
echo -e "${BOLD}[3/5] Checking distribution...${NC}"
if ! python -m twine check dist/*; then
    echo -e "${RED}Error: Distribution check failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Distribution check passed${NC}"
echo ""

# Step 4: Show distribution files
echo -e "${BLUE}📦 Built distribution files:${NC}"
ls -la dist/
echo ""

# Step 5: Upload options
echo -e "${BOLD}[4/5] Upload options:${NC}"
echo -e "${CYAN}1. Upload to TestPyPI (recommended first)${NC}"
echo -e "${CYAN}2. Upload to PyPI (production)${NC}"
echo -e "${CYAN}3. Skip upload${NC}"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo -e "${BOLD}[5/5] Uploading to TestPyPI...${NC}"
        if python -m twine upload --repository testpypi dist/*; then
            echo ""
            echo -e "${GREEN}========================================${NC}"
            echo -e "${GREEN}SUCCESS! Package uploaded to TestPyPI${NC}"
            echo -e "${GREEN}========================================${NC}"
            echo ""
            echo -e "${BLUE}Test your package at: ${YELLOW}https://test.pypi.org/project/sproclib/${NC}"
            echo ""
            echo -e "${BLUE}Test installation command:${NC}"
            echo -e "${YELLOW}pip install --index-url https://test.pypi.org/simple/ sproclib${NC}"
        else
            echo -e "${RED}Error: TestPyPI upload failed!${NC}"
            echo -e "${YELLOW}Make sure you have TestPyPI credentials configured in ~/.pypirc${NC}"
            exit 1
        fi
        ;;
    2)
        echo ""
        echo -e "${BOLD}[5/5] Uploading to PyPI...${NC}"
        if python -m twine upload dist/*; then
            echo ""
            echo -e "${GREEN}========================================${NC}"
            echo -e "${GREEN}SUCCESS! Package uploaded to PyPI${NC}"
            echo -e "${GREEN}========================================${NC}"
            echo ""
            echo -e "${BLUE}Your package is now available at:${NC}"
            echo -e "${YELLOW}https://pypi.org/project/sproclib/${NC}"
            echo ""
            echo -e "${BLUE}Installation command:${NC}"
            echo -e "${YELLOW}pip install sproclib${NC}"
        else
            echo -e "${RED}Error: PyPI upload failed!${NC}"
            echo ""
            echo -e "${YELLOW}Common causes:${NC}"
            echo -e "${YELLOW}• Version already exists (you need to bump version)${NC}"
            echo -e "${YELLOW}• Authentication issues (check credentials in ~/.pypirc)${NC}"
            echo ""
            echo -e "${BLUE}To fix version conflict:${NC}"
            echo -e "${YELLOW}1. Update version using: ./scripts/manage_version/set_version.sh <new_version>${NC}"
            echo -e "${YELLOW}2. Re-run this script${NC}"
            exit 1
        fi
        ;;
    3)
        echo ""
        echo -e "${YELLOW}Upload skipped. Files are ready in dist/ folder.${NC}"
        echo ""
        echo -e "${BLUE}Manual upload commands:${NC}"
        echo -e "${YELLOW}  TestPyPI: python -m twine upload --repository testpypi dist/*${NC}"
        echo -e "${YELLOW}  PyPI:     python -m twine upload dist/*${NC}"
        ;;
    *)
        echo -e "${RED}Invalid choice. Upload skipped.${NC}"
        echo ""
        echo -e "${BLUE}Manual upload commands:${NC}"
        echo -e "${YELLOW}  TestPyPI: python -m twine upload --repository testpypi dist/*${NC}"
        echo -e "${YELLOW}  PyPI:     python -m twine upload dist/*${NC}"
        ;;
esac

echo ""
echo -e "${CYAN}🎉 Build process completed!${NC}"
echo ""
echo -e "${BLUE}📋 Useful commands:${NC}"
echo -e "${YELLOW}• Check version status: ./scripts/manage_version/get_version.sh${NC}"
echo -e "${YELLOW}• Update version: ./scripts/manage_version/set_version.sh <version>${NC}"
echo -e "${YELLOW}• Build documentation: ./scripts/readthedocs/sphinx.sh${NC}"
