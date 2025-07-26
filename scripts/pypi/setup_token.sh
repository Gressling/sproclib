#!/bin/bash
# Setup script for PyPI API token

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔑 PyPI API Token Setup${NC}"
echo "======================="

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOKEN_FILE="$SCRIPT_DIR/api-token.txt"

echo ""
echo -e "${YELLOW}📋 Steps to get your PyPI API token:${NC}"
echo ""
echo "1. 🌐 Go to: https://pypi.org/manage/account/token/"
echo "2. 📝 Click 'Add API token'"
echo "3. 🏷️  Name: 'sproclib-upload' (or any name)"
echo "4. 🎯 Scope: 'Entire account' or 'sproclib' project"
echo "5. ✅ Click 'Add token'"
echo "6. 📋 Copy the token (starts with 'pypi-')"
echo ""

# Check if token file already exists
if [[ -f "$TOKEN_FILE" ]]; then
    echo -e "${YELLOW}⚠️  Token file already exists at: $TOKEN_FILE${NC}"
    read -p "Do you want to replace it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}Setup cancelled. Existing token file preserved.${NC}"
        exit 0
    fi
fi

echo -e "${BLUE}📝 Enter your PyPI API token:${NC}"
echo -e "${YELLOW}   (Token will be hidden as you type)${NC}"
read -s -p "Token: " token
echo ""

# Validate token format
if [[ ! "$token" =~ ^pypi- ]]; then
    echo -e "${RED}❌ Invalid token format. PyPI tokens should start with 'pypi-'${NC}"
    echo -e "${YELLOW}💡 Make sure you copied the complete token from PyPI${NC}"
    exit 1
fi

# Save token to file
echo "$token" > "$TOKEN_FILE"

# Verify file was created
if [[ -f "$TOKEN_FILE" ]]; then
    echo -e "${GREEN}✅ Token saved successfully to: $TOKEN_FILE${NC}"
    echo -e "${GREEN}🔒 File is protected by .gitignore${NC}"
    echo ""
    echo -e "${BLUE}🚀 You can now use the upload scripts:${NC}"
    echo "   ./scripts/pypi/build_and_upload.sh --upload"
    echo "   ./scripts/pypi/upload_only.sh"
else
    echo -e "${RED}❌ Failed to save token file${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}🔐 Security reminder:${NC}"
echo "• Keep your token private and secure"
echo "• Never share or commit tokens to git"
echo "• Regenerate if compromised"
echo "• Token file is already in .gitignore"
