#!/bin/bash
# ========================================================================
# SPROCLIB Version Check Script (macOS/Unix)
# ========================================================================
# This script checks and displays the version numbers across all project 
# files and compares them for consistency.
#
# Usage: ./get_version.sh
# ========================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "🔍 Current SPROCLIB Version Status"
echo "=================================="
echo ""
echo "📋 Version Information:"
echo ""

# Table header
printf "%-20s %-10s %-20s\n" "Source" "Version" "Status"
echo "--------------------------------------------------------"

# Get Git tag version
if git tag --sort=-v:refname | head -1 > /dev/null 2>&1; then
    GIT_TAG=$(git tag --sort=-v:refname | head -1)
    if [[ -n "$GIT_TAG" ]]; then
        GIT_VERSION=${GIT_TAG#v}  # Remove 'v' prefix if present
        printf "%-20s %-10s ${GREEN}%-20s${NC}\n" "Git Tag (Latest)" "$GIT_TAG" "✅ Current Release"
    else
        printf "%-20s %-10s ${RED}%-20s${NC}\n" "Git Tag (Latest)" "N/A" "❌ No tags found"
        GIT_VERSION=""
    fi
else
    printf "%-20s %-10s ${RED}%-20s${NC}\n" "Git Tag (Latest)" "N/A" "❌ Not a git repo"
    GIT_VERSION=""
fi

# Get pyproject.toml version
if [[ -f "pyproject.toml" ]]; then
    PYPROJECT_VERSION=$(grep -E '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
    if [[ -n "$PYPROJECT_VERSION" ]]; then
        if [[ "$PYPROJECT_VERSION" == "$GIT_VERSION" ]]; then
            printf "%-20s %-10s ${GREEN}%-20s${NC}\n" "pyproject.toml" "$PYPROJECT_VERSION" "✅ Matches git tag"
        elif [[ "$PYPROJECT_VERSION" > "$GIT_VERSION" ]] && [[ -n "$GIT_VERSION" ]]; then
            printf "%-20s %-10s ${YELLOW}%-20s${NC}\n" "pyproject.toml" "$PYPROJECT_VERSION" "⚠️ Ahead of release"
        else
            printf "%-20s %-10s ${RED}%-20s${NC}\n" "pyproject.toml" "$PYPROJECT_VERSION" "❌ Version mismatch"
        fi
    else
        printf "%-20s %-10s ${RED}%-20s${NC}\n" "pyproject.toml" "N/A" "❌ Not found"
    fi
else
    printf "%-20s %-10s ${RED}%-20s${NC}\n" "pyproject.toml" "N/A" "❌ File not found"
fi

# Get __init__.py version
if [[ -f "sproclib/__init__.py" ]]; then
    INIT_VERSION=$(grep -E '^__version__ = ' sproclib/__init__.py | sed 's/__version__ = "\(.*\)"/\1/')
    if [[ -n "$INIT_VERSION" ]]; then
        if [[ "$INIT_VERSION" == "$GIT_VERSION" ]]; then
            printf "%-20s %-10s ${GREEN}%-20s${NC}\n" "__init__.py" "$INIT_VERSION" "✅ Matches git tag"
        elif [[ "$INIT_VERSION" > "$GIT_VERSION" ]] && [[ -n "$GIT_VERSION" ]]; then
            printf "%-20s %-10s ${YELLOW}%-20s${NC}\n" "__init__.py" "$INIT_VERSION" "⚠️ Ahead of release"
        elif [[ "$INIT_VERSION" < "$GIT_VERSION" ]] && [[ -n "$GIT_VERSION" ]]; then
            printf "%-20s %-10s ${RED}%-20s${NC}\n" "__init__.py" "$INIT_VERSION" "❌ Outdated"
        else
            printf "%-20s %-10s ${RED}%-20s${NC}\n" "__init__.py" "$INIT_VERSION" "❌ Version mismatch"
        fi
    else
        printf "%-20s %-10s ${RED}%-20s${NC}\n" "__init__.py" "N/A" "❌ Not found"
    fi
else
    printf "%-20s %-10s ${RED}%-20s${NC}\n" "__init__.py" "N/A" "❌ File not found"
fi

# Get setup.py version
if [[ -f "setup.py" ]]; then
    SETUP_VERSION=$(grep -E 'version=' setup.py | sed 's/.*version="\(.*\)".*/\1/')
    if [[ -n "$SETUP_VERSION" ]]; then
        if [[ "$SETUP_VERSION" == "$GIT_VERSION" ]]; then
            printf "%-20s %-10s ${GREEN}%-20s${NC}\n" "setup.py" "$SETUP_VERSION" "✅ Matches git tag"
        elif [[ "$SETUP_VERSION" > "$GIT_VERSION" ]] && [[ -n "$GIT_VERSION" ]]; then
            printf "%-20s %-10s ${YELLOW}%-20s${NC}\n" "setup.py" "$SETUP_VERSION" "⚠️ Ahead of release"
        elif [[ "$SETUP_VERSION" < "$GIT_VERSION" ]] && [[ -n "$GIT_VERSION" ]]; then
            printf "%-20s %-10s ${RED}%-20s${NC}\n" "setup.py" "$SETUP_VERSION" "❌ Outdated"
        else
            printf "%-20s %-10s ${RED}%-20s${NC}\n" "setup.py" "$SETUP_VERSION" "❌ Version mismatch"
        fi
    else
        printf "%-20s %-10s ${RED}%-20s${NC}\n" "setup.py" "N/A" "❌ Not found"
    fi
else
    printf "%-20s %-10s ${RED}%-20s${NC}\n" "setup.py" "N/A" "❌ File not found"
fi

echo ""
echo "📊 Summary:"

# Count issues
ISSUES=0
TOTAL=0

if [[ -n "$GIT_VERSION" ]]; then
    TOTAL=$((TOTAL + 1))
    if [[ "$PYPROJECT_VERSION" != "$GIT_VERSION" ]] && [[ -n "$PYPROJECT_VERSION" ]]; then
        ISSUES=$((ISSUES + 1))
    fi
    TOTAL=$((TOTAL + 1))
    if [[ "$INIT_VERSION" != "$GIT_VERSION" ]] && [[ -n "$INIT_VERSION" ]]; then
        ISSUES=$((ISSUES + 1))
    fi
    TOTAL=$((TOTAL + 1))
    if [[ "$SETUP_VERSION" != "$GIT_VERSION" ]] && [[ -n "$SETUP_VERSION" ]]; then
        ISSUES=$((ISSUES + 1))
    fi
    TOTAL=$((TOTAL + 1))
fi

if [[ $ISSUES -eq 0 ]]; then
    echo -e "${GREEN}✅ All versions are consistent${NC}"
else
    echo -e "${YELLOW}⚠️  Found $ISSUES version inconsistencies out of $TOTAL files${NC}"
    echo ""
    echo -e "${BLUE}💡 Recommendations:${NC}"
    echo "   • Use build/manage_version/set_version.sh to update all versions"
    echo "   • Current release version appears to be: $GIT_TAG"
fi

echo ""
echo "🛠️  Available commands:"
echo "   • Update versions: build/manage_version/set_version.sh <version>"
echo "   • Check again: build/manage_version/get_version.sh"
echo ""
