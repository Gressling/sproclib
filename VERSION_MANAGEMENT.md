# SPROCLIB Version Management Guide

This document describes the versioning procedure for SPROCLIB, including automated tools and best practices for managing version numbers across the project.

## Overview

SPROCLIB uses [Semantic Versioning (SemVer)](https://semver.org/) with the format `MAJOR.MINOR.PATCH`:

- **MAJOR** version when you make incompatible API changes
- **MINOR** version when you add functionality in a backwards compatible manner  
- **PATCH** version when you make backwards compatible bug fixes

## Automated Version Management

### Quick Start

To update the version across all project files and create a git tag:

```bash
# Using batch script (Windows)
.\set_version.bat 2.1.0

# Using PowerShell script (recommended)
.\set_version.ps1 2.1.0
```

### What Gets Updated

The version management scripts automatically update version numbers in:

- `pyproject.toml` - Main project configuration
- `setup.py` - Legacy setup file  
- `sproclib/__init__.py` - Main package version and docstring
- `sproclib/unit/plant/__init__.py` - Plant module version
- `docs/source/conf.py` - Sphinx documentation (both `release` and `version`)

### Git Operations

The scripts also handle git operations:
- ✅ Creates a commit with all version changes
- ✅ Creates an annotated git tag (e.g., `v2.1.0`)
- ✅ Validates git repository status
- ⚠️ Warns about uncommitted changes

## Available Tools

### 1. `set_version.bat` (Windows Batch)
- **Platform**: Windows only
- **Encoding**: UTF-8 without BOM (prevents TOML parsing issues)
- **Features**: Full validation and error handling

**Usage:**
```cmd
set_version.bat <version>
```

**Example:**
```cmd
set_version.bat 2.1.0
```

### 2. `set_version.ps1` (PowerShell)
- **Platform**: Cross-platform (Windows, Linux, macOS with PowerShell Core)
- **Features**: Better error handling, colored output, more robust
- **Recommended**: Use this for better reliability

**Usage:**
```powershell
.\set_version.ps1 <version>
```

**Example:**
```powershell
.\set_version.ps1 2.1.0
```

## Version Update Workflow

### Step-by-Step Process

1. **Prepare for Release**
   ```bash
   # Ensure you're on the main branch
   git checkout main
   git pull origin main
   
   # Ensure all changes are committed
   git status
   ```

2. **Run Version Update Script**
   ```bash
   # Choose your preferred method
   .\set_version.ps1 2.1.0
   # OR
   .\set_version.bat 2.1.0
   ```

3. **Review Changes**
   ```bash
   # Review the automated changes
   git show
   
   # Check that all files were updated correctly
   git diff HEAD~1
   ```

4. **Push Changes**
   ```bash
   # Push the commit
   git push origin main
   
   # Push the tag
   git push origin v2.1.0
   ```

5. **Build Documentation**
   ```bash
   python docs\build_docs.py
   ```

6. **Release to PyPI**
   ```bash
   .\pypi.bat
   ```

### What the Scripts Do

#### Safety Checks
- ✅ Validates version format (x.y.z pattern)
- ✅ Checks if you're in a git repository
- ✅ Warns about uncommitted changes
- ✅ Provides option to continue or abort

#### File Updates
- ✅ Uses regex patterns to find and replace version strings
- ✅ Handles different quote styles (`"` and `'`)
- ✅ Updates both version variables and docstring comments
- ✅ Preserves file encoding (UTF-8 without BOM)

#### Git Integration
- ✅ Stages all modified files
- ✅ Creates descriptive commit message
- ✅ Creates annotated tag with release message
- ✅ Provides next steps for pushing

## Version Number Guidelines

### When to Increment

| Change Type | Version Component | Examples |
|-------------|------------------|----------|
| Breaking API changes | **MAJOR** | Remove public methods, change function signatures |
| New features (backward compatible) | **MINOR** | Add new classes, methods, optional parameters |
| Bug fixes (backward compatible) | **PATCH** | Fix calculations, resolve crashes, documentation updates |

### Examples

```bash
# Bug fix release
.\set_version.ps1 2.0.1

# New feature release  
.\set_version.ps1 2.1.0

# Breaking change release
.\set_version.ps1 3.0.0
```

## File Locations

The scripts update version information in these key files:

### Primary Configuration
- **`pyproject.toml`**: `version = "2.1.0"`
- **`setup.py`**: `version="2.1.0"`

### Package Files
- **`sproclib/__init__.py`**: 
  - `__version__ = "2.1.0"`
  - Docstring: `Version: 2.1.0`
- **`sproclib/unit/plant/__init__.py`**: `__version__ = '2.1.0'`

### Documentation
- **`docs/source/conf.py`**:
  - `release = '2.1.0'`
  - `version = '2.1.0'`

## Troubleshooting

### Common Issues

#### Encoding Problems
If you see encoding errors or corrupted characters:
- Use the PowerShell script (`set_version.ps1`) instead of batch
- Check that files are saved as UTF-8 without BOM

#### Git Issues
```bash
# If tag already exists
git tag -d v2.1.0  # Delete local tag
git push origin :refs/tags/v2.1.0  # Delete remote tag

# If commit fails
git reset --soft HEAD~1  # Undo commit, keep changes
```

#### PowerShell Execution Policy
If PowerShell scripts are blocked:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Validation

After running the version update, verify the changes:

```bash
# Check all version references
findstr /r /s "__version__.*=" sproclib\*.py
findstr "version.*=" pyproject.toml setup.py
findstr "release.*=" docs\source\conf.py

# Verify git tag was created
git tag -l | findstr v2.1.0
```

## Integration with CI/CD

The version management scripts can be integrated into automated workflows:

```yaml
# Example GitHub Actions workflow
- name: Update Version
  run: .\set_version.ps1 ${{ github.event.inputs.version }}
  
- name: Build Documentation  
  run: python docs\build_docs.py
  
- name: Upload to PyPI
  run: .\pypi.bat
```

## Best Practices

1. **Always test before releasing**: Run tests after version update
2. **Use descriptive commit messages**: The scripts handle this automatically
3. **Keep CHANGELOG.md updated**: Document what changed in each version
4. **Tag consistently**: Always use the `v` prefix (e.g., `v2.1.0`)
5. **Review changes**: Use `git show` to verify all files were updated correctly
6. **Backup before major releases**: Ensure you can rollback if needed

## Release Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Run version update script
- [ ] Review automated changes
- [ ] Push commit and tag
- [ ] Build and verify documentation
- [ ] Upload to PyPI
- [ ] Verify PyPI listing shows correct version
- [ ] Update any dependent projects

---

## Quick Reference

| Task | Command |
|------|---------|
| Update version | `.\set_version.ps1 X.Y.Z` |
| Review changes | `git show` |
| Push changes | `git push origin main` |
| Push tag | `git push origin vX.Y.Z` |
| Build docs | `python docs\build_docs.py` |
| Upload to PyPI | `.\pypi.bat` |

For questions or issues with the versioning process, refer to this guide or check the script output for detailed error messages and next steps.
