#!/bin/bash
# ===========================================================            echo "  --clean          Clean Python build artifacts before building (dist/, *.egg-info, Python's build/ only)"============
# SPROCLIB PyPI Build and Upload Script (Unix/ma    # Python creates a build/ directory during packaging, but we use scripts/ for our scripts
    # We can distinguish them: Python's build/ has lib/, our scripts/ has README.md
    if [[ -d "build" ]] && [[ ! -f "scripts/README.md" ]] && [[ -d "build/lib" ]]; then
        echo -e "${YELLOW}   Removing Python build artifacts...${NC}"
        rm -rf build/# ========================================================================
# This script builds the package and provides upload commands for PyPI
#
# Usage: ./build_and_upload.sh [options]
# Options:
#   --test-upload    Automatically upload to TestPyPI after build
#   --upload         Automatically upload to PyPI after build
#   --clean          Clean Python build artifacts before building (dist/, *.egg-info, Python's build/ only)
# ========================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script options
AUTO_TEST_UPLOAD=false
AUTO_UPLOAD=false
CLEAN_FIRST=false

# Function to run command with error handling
run_command() {
    local cmd="$1"
    local description="$2"
    
    echo -e "\n${BLUE}📦 $description...${NC}"
    
    if ! eval "$cmd"; then
        echo -e "${RED}❌ Error: $description failed${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Success: $description completed${NC}"
}

# Function to check if command exists
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}❌ Error: $1 is not installed${NC}"
        echo -e "${YELLOW}💡 Install with: pip install $1${NC}"
        exit 1
    fi
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --test-upload)
            AUTO_TEST_UPLOAD=true
            shift
            ;;
        --upload)
            AUTO_UPLOAD=true
            shift
            ;;
        --clean)
            CLEAN_FIRST=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --test-upload    Automatically upload to TestPyPI after build"
            echo "  --upload         Automatically upload to PyPI after build"
            echo "  --clean          Clean Python build artifacts before building (dist/, *.egg-info, Python's scripts/ only)"
            echo "  -h, --help       Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo -e "${CYAN}🚀 SPROCLIB PyPI Build and Upload Script${NC}"
echo "========================================"

# Get the directory where this script is located and go to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}📁 Working directory: $PROJECT_ROOT${NC}"

# Check if we're in a virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    if [[ -f ".venv/bin/activate" ]]; then
        echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
        source ".venv/bin/activate"
    else
        echo -e "${YELLOW}⚠️  Warning: No virtual environment detected${NC}"
        echo -e "${YELLOW}   Consider using: python -m venv .venv && source .venv/bin/activate${NC}"
    fi
fi

# Check required tools
echo -e "\n${BLUE}🔍 Checking required tools...${NC}"
check_command "python"

# Check for build and twine
if ! python -m build --help &> /dev/null; then
    echo -e "${YELLOW}⚠️  Installing build module...${NC}"
    pip install build
fi

if ! python -m twine --help &> /dev/null; then
    echo -e "${YELLOW}⚠️  Installing twine module...${NC}"
    pip install twine
fi

# Clean previous builds if requested
if [[ "$CLEAN_FIRST" == true ]]; then
    echo -e "\n${BLUE}🧹 Cleaning previous builds...${NC}"
    
    # Remove dist directory
    if [[ -d "dist" ]]; then
        echo -e "${YELLOW}   Removing dist/...${NC}"
        rm -rf dist/
    fi
    
    # Remove *.egg-info directories
    if ls *.egg-info 1> /dev/null 2>&1; then
        echo -e "${YELLOW}   Removing *.egg-info...${NC}"
        rm -rf *.egg-info/
    fi
    
    # Only remove Python's build directory, not our scripts/ directory
    # Python creates a scripts/ directory during packaging, but we use scripts/ for our scripts
    # We can distinguish them: Python's scripts/ has lib/, our scripts/ has README.md
    if [[ -d "build" ]] && [[ ! -f "scripts/README.md" ]] && [[ -d "scripts/lib" ]]; then
        echo -e "${YELLOW}   Removing Python build artifacts...${NC}"
        rm -rf scripts/
    fi
    
    echo -e "${GREEN}   ✓ Cleanup completed${NC}"
fi

# Build the package
run_command "python -m build" "Building package"

# Check the distribution
run_command "python -m twine check dist/*" "Checking distribution"

echo -e "\n${GREEN}✅ Package built successfully!${NC}"
echo -e "${BLUE}📂 Distribution files:${NC}"
ls -la dist/

# Handle automatic uploads
if [[ "$AUTO_TEST_UPLOAD" == true ]]; then
    echo -e "\n${YELLOW}🚀 Uploading to TestPyPI...${NC}"
    run_command "python -m twine upload --repository testpypi dist/*" "Uploading to TestPyPI"
    echo -e "${GREEN}✅ Uploaded to TestPyPI successfully!${NC}"
    echo -e "${BLUE}🌐 View at: https://test.pypi.org/project/sproclib/${NC}"
elif [[ "$AUTO_UPLOAD" == true ]]; then
    echo -e "\n${RED}⚠️  WARNING: You are about to upload to production PyPI!${NC}"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_command "python -m twine upload dist/*" "Uploading to PyPI"
        echo -e "${GREEN}✅ Uploaded to PyPI successfully!${NC}"
        echo -e "${BLUE}🌐 View at: https://pypi.org/project/sproclib/${NC}"
    else
        echo -e "${YELLOW}Upload cancelled${NC}"
    fi
else
    # Provide upload commands
    echo -e "\n${CYAN}📤 Upload Commands:${NC}"
    echo ""
    echo -e "${YELLOW}To upload to TestPyPI (recommended first):${NC}"
    echo "python -m twine upload --repository testpypi dist/*"
    echo ""
    echo -e "${YELLOW}To upload to PyPI:${NC}"
    echo "python -m twine upload dist/*"
    echo ""
    echo -e "${YELLOW}Or use this script with automatic upload:${NC}"
    echo "$0 --test-upload    # Upload to TestPyPI"
    echo "$0 --upload         # Upload to PyPI"
fi

echo ""
echo -e "${BLUE}📋 Prerequisites checklist:${NC}"
echo "1. ✅ build and twine installed"
echo "2. 📝 PyPI account created (https://pypi.org/)"
echo "3. 📝 TestPyPI account created (https://test.pypi.org/)"
echo "4. 🔑 Credentials configured in ~/.pypirc or environment"

echo ""
echo -e "${BLUE}🔧 Credential setup example:${NC}"
echo "Create ~/.pypirc with:"
echo ""
echo "[distutils]"
echo "index-servers = pypi testpypi"
echo ""
echo "[pypi]"
echo "username = __token__"
echo "password = pypi-your-api-token-here"
echo ""
echo "[testpypi]"
echo "repository = https://test.pypi.org/legacy/"
echo "username = __token__"
echo "password = pypi-your-testpypi-token-here"

echo ""
echo -e "${GREEN}🎉 Build script completed successfully!${NC}"
