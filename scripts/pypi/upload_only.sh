#!/bin/bash
# ========================================================================
# SPROCLIB Upload Only Script
# This script uploads already built packages using the API token
# ========================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get the directory where this script is located and go to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

# Function to get API token from file
get_api_token() {
    local token_file="$SCRIPT_DIR/api-token.txt"
    if [[ -f "$token_file" ]]; then
        local token=$(cat "$token_file" | tr -d '\n\r' | xargs)
        if [[ -n "$token" ]]; then
            echo "$token"
            return 0
        fi
    fi
    return 1
}

# Function to setup authentication
setup_auth() {
    local api_token
    if api_token=$(get_api_token); then
        echo -e "${GREEN}🔑 Using API token from api-token.txt${NC}"
        export TWINE_USERNAME="__token__"
        export TWINE_PASSWORD="$api_token"
        return 0
    else
        echo -e "${RED}❌ No API token found in api-token.txt${NC}"
        echo -e "${YELLOW}💡 To set up your API token:${NC}"
        echo -e "${YELLOW}   1. Create PyPI account: https://pypi.org/account/register/${NC}"
        echo -e "${YELLOW}   2. Generate token: https://pypi.org/manage/account/token/${NC}"
        echo -e "${YELLOW}   3. Save token: echo 'pypi-your-token-here' > scripts/pypi/api-token.txt${NC}"
        echo -e "${YELLOW}   4. See: scripts/pypi/README_TOKEN_SETUP.md for detailed instructions${NC}"
        return 1
    fi
}

echo -e "${CYAN}🚀 SPROCLIB Upload Script${NC}"
echo "=========================="

# Check if we're in a virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    if [[ -f ".venv/bin/activate" ]]; then
        echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
        source ".venv/bin/activate"
    else
        echo -e "${YELLOW}⚠️  No virtual environment found. Consider creating one.${NC}"
    fi
fi

# Check if dist directory exists
if [[ ! -d "dist" ]]; then
    echo -e "${RED}❌ No dist/ directory found. Please build the package first.${NC}"
    echo -e "${YELLOW}💡 Run: ./scripts/pypi/build_and_upload.sh${NC}"
    exit 1
fi

# Check if there are files to upload
if [[ -z "$(ls -A dist/)" ]]; then
    echo -e "${RED}❌ No files found in dist/ directory.${NC}"
    echo -e "${YELLOW}💡 Run: ./scripts/pypi/build_and_upload.sh${NC}"
    exit 1
fi

echo -e "${BLUE}📂 Files to upload:${NC}"
ls -la dist/

echo ""
echo "Upload options:"
echo "1. Upload to TestPyPI (recommended first)"
echo "2. Upload to PyPI (production)"
echo "3. Cancel"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo -e "\n${YELLOW}🚀 Uploading to TestPyPI...${NC}"
        if setup_auth; then
            if python3 -m twine upload --repository testpypi dist/*; then
                echo -e "${GREEN}✅ Uploaded to TestPyPI successfully!${NC}"
                echo -e "${BLUE}🌐 View at: https://test.pypi.org/project/sproclib/${NC}"
            else
                echo -e "${RED}❌ Upload to TestPyPI failed!${NC}"
                exit 1
            fi
        else
            exit 1
        fi
        ;;
    2)
        echo -e "\n${RED}⚠️  WARNING: You are about to upload to production PyPI!${NC}"
        read -p "Are you sure? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "\n${YELLOW}🚀 Uploading to PyPI...${NC}"
            if setup_auth; then
                if python3 -m twine upload dist/*; then
                    echo -e "${GREEN}✅ Uploaded to PyPI successfully!${NC}"
                    echo -e "${BLUE}🌐 View at: https://pypi.org/project/sproclib/${NC}"
                else
                    echo -e "${RED}❌ Upload to PyPI failed!${NC}"
                    exit 1
                fi
            else
                exit 1
            fi
        else
            echo -e "${YELLOW}Upload cancelled${NC}"
        fi
        ;;
    3)
        echo -e "${YELLOW}Upload cancelled${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}❌ Invalid choice${NC}"
        exit 1
        ;;
esac

echo -e "\n${GREEN}🎉 Upload completed successfully!${NC}"
