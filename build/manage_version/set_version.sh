#!/bin/bash
# ========================================================================
# SPROCLIB Version Update Script (macOS/Unix)
# ========================================================================
# This script updates the version number across all project files and
# creates a git tag for the new version.
#
# Usage: ./set_version.sh <version>
# Example: ./set_version.sh 2.0.5
# ========================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if version argument is provided
if [ -z "$1" ]; then
    echo -e "${RED}ERROR: Version number required${NC}"
    echo "Usage: $0 <version>"
    echo "Example: $0 2.0.5"
    exit 1
fi

NEW_VERSION="$1"
echo ""
echo -e "${BLUE}========================================================================${NC}"
echo -e "${BLUE}SPROCLIB Version Update Script${NC}"
echo -e "${BLUE}========================================================================${NC}"
echo -e "${YELLOW}Updating version to: $NEW_VERSION${NC}"
echo ""

# Validate version format (basic check for x.y.z pattern)
if [[ ! "$NEW_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}ERROR: Invalid version format. Expected format: x.y.z${NC}"
    echo "Example: 2.0.5"
    exit 1
fi

# Check if we're in a git repository
if ! git status > /dev/null 2>&1; then
    echo -e "${RED}ERROR: Not in a git repository${NC}"
    exit 1
fi

# Check for uncommitted changes
if ! git diff --quiet; then
    echo -e "${YELLOW}WARNING: You have uncommitted changes${NC}"
    read -p "Continue anyway? (y/N): " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "Aborted"
        exit 1
    fi
fi

echo -e "${BLUE}Step 1: Updating pyproject.toml...${NC}"
if [ -f "pyproject.toml" ]; then
    if sed -i.bak "s/version = \"[^\"]*\"/version = \"$NEW_VERSION\"/" pyproject.toml; then
        echo -e "${GREEN}   ✓ pyproject.toml updated${NC}"
        rm -f pyproject.toml.bak
    else
        echo -e "${RED}ERROR: Failed to update pyproject.toml${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}   ⚠ pyproject.toml not found${NC}"
fi

echo -e "${BLUE}Step 2: Updating setup.py...${NC}"
if [ -f "setup.py" ]; then
    if sed -i.bak "s/version=\"[^\"]*\"/version=\"$NEW_VERSION\"/" setup.py; then
        echo -e "${GREEN}   ✓ setup.py updated${NC}"
        rm -f setup.py.bak
    else
        echo -e "${RED}ERROR: Failed to update setup.py${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}   ⚠ setup.py not found${NC}"
fi

echo -e "${BLUE}Step 3: Updating main package __init__.py...${NC}"
if [ -f "sproclib/__init__.py" ]; then
    # Update both __version__ variable and docstring version
    if sed -i.bak -e "s/__version__ = \"[^\"]*\"/__version__ = \"$NEW_VERSION\"/" \
                  -e "s/Version: [^\\n]*/Version: $NEW_VERSION/" sproclib/__init__.py; then
        echo -e "${GREEN}   ✓ sproclib/__init__.py updated${NC}"
        rm -f sproclib/__init__.py.bak
    else
        echo -e "${RED}ERROR: Failed to update sproclib/__init__.py${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}   ⚠ sproclib/__init__.py not found${NC}"
fi

echo -e "${BLUE}Step 4: Updating Sphinx documentation...${NC}"
if [ -f "docs/source/conf.py" ]; then
    if sed -i.bak -e "s/release = '[^']*'/release = '$NEW_VERSION'/" \
                  -e "s/version = '[^']*'/version = '$NEW_VERSION'/" docs/source/conf.py; then
        echo -e "${GREEN}   ✓ Sphinx documentation updated${NC}"
        rm -f docs/source/conf.py.bak
    else
        echo -e "${RED}ERROR: Failed to update docs/source/conf.py${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}   ⚠ docs/source/conf.py not found${NC}"
fi

echo -e "${BLUE}Step 5: Checking for other version references...${NC}"
if find sproclib/ -name "*.py" -exec grep -l "__version__.*=" {} \; 2>/dev/null | grep -v __pycache__ | head -5; then
    echo -e "${YELLOW}   Found additional version references in Python files${NC}"
fi

echo ""
echo -e "${BLUE}Step 6: Git operations...${NC}"
echo -e "${BLUE}   Adding changes to git...${NC}"
if git add pyproject.toml setup.py sproclib/__init__.py docs/source/conf.py 2>/dev/null; then
    echo -e "${GREEN}   ✓ Files added to git${NC}"
else
    echo -e "${RED}ERROR: Failed to add files to git${NC}"
    exit 1
fi

echo -e "${BLUE}   Creating commit...${NC}"
if git commit -m "Update version to $NEW_VERSION"; then
    echo -e "${GREEN}   ✓ Commit created${NC}"
else
    echo -e "${RED}ERROR: Failed to create commit${NC}"
    exit 1
fi

echo -e "${BLUE}   Creating git tag...${NC}"
if git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION"; then
    echo -e "${GREEN}   ✓ Tag created${NC}"
else
    echo -e "${RED}ERROR: Failed to create git tag${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}========================================================================${NC}"
echo -e "${GREEN}SUCCESS: Version updated to $NEW_VERSION${NC}"
echo -e "${GREEN}========================================================================${NC}"
echo ""
echo -e "${YELLOW}Updated files:${NC}"
echo "   - pyproject.toml"
echo "   - setup.py"
echo "   - sproclib/__init__.py"
echo "   - docs/source/conf.py"
echo ""
echo -e "${YELLOW}Git operations completed:${NC}"
echo "   - Committed changes"
echo "   - Created tag: v$NEW_VERSION"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "   - Review changes: git show"
echo "   - Push changes: git push origin main"
echo "   - Push tags: git push origin v$NEW_VERSION"
echo "   - Build documentation: ./build/readthedocs/sphinx.sh"
echo "   - Upload to PyPI: python build/pypi/build_and_upload.py"
echo ""
echo -e "${GREEN}========================================================================${NC}"
