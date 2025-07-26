# Version Management Scripts

This directory contains scripts for managing and checking SPROCLIB version information across all project files.

## Available Scripts

### Version Checking Scripts
- **`get_version.sh`** - macOS/Unix shell script for checking version status
- **`get_version.bat`** - Windows batch script for checking version status  
- **`get_version.ps1`** - Windows PowerShell script for checking version status (recommended for Windows)

### Version Setting Scripts
- **`set_version.sh`** - macOS/Unix shell script for updating all version numbers
- **`set_version.ps1`** - PowerShell script for updating all version numbers  
- **`set_version.bat`** - Windows batch script for updating all version numbers

## Usage

### Check Current Version Status
```bash
# macOS/Unix
./scripts/manage_version/get_version.sh

# Windows (Command Prompt)
build\manage_version\get_version.bat

# Windows (PowerShell)
.\build\manage_version\get_version.ps1
```

### Update Version Numbers
```bash
# macOS/Unix
./scripts/manage_version/set_version.sh 2.0.5

# Windows (PowerShell - recommended)
.\build\manage_version\set_version.ps1 2.0.5

# Windows (Command Prompt)
build\manage_version\set_version.bat 2.0.5
```

**Note:** All set_version scripts automatically:
- Update version numbers in all project files
- Create a git commit with the changes
- Create a git tag for the new version
- Push the commit and tag to the remote repository

## Output Format

The version checking scripts display a formatted table showing:

```
🔍 Current SPROCLIB Version Status
==================================

📋 Version Information:

Source               Version    Status              
--------------------------------------------------------
Git Tag (Latest)     v2.0.4     ✅ Current Release 
pyproject.toml       2.1.0      ⚠️ Ahead of release
__init__.py          2.0.4      ✅ Matches git tag 
setup.py             2.0.0      ❌ Outdated        
```

## Status Indicators

- **✅ Current Release** - Git tag represents the latest official release
- **✅ Matches git tag** - Version matches the current git tag
- **⚠️ Ahead of release** - Version is newer than the current git tag (prepared for next release)
- **❌ Outdated** - Version is older than the current git tag
- **❌ Version mismatch** - Version doesn't match expected pattern
- **❌ File not found** - Required file is missing
- **❌ Not found** - Version information not found in file

## Files Checked

The scripts check version information in:
1. **Git Tags** - Latest semantic version tag
2. **pyproject.toml** - Modern Python project configuration
3. **sproclib/__init__.py** - Package version variable
4. **setup.py** - Legacy setuptools configuration

## Best Practices

1. **Use the version setting scripts** to maintain consistency across all files
2. **Check version status** before creating releases
3. **Resolve inconsistencies** before publishing to PyPI
4. **Follow semantic versioning** (MAJOR.MINOR.PATCH) for version numbers
