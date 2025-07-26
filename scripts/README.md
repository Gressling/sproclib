# SPROCLIB Build Tools

This directory contains build, deployment, an### Build and Upload Tools

| **Platform** | **Script** | **Usage** |
|--------------|------------|-----------|
| **Cross-platform** | `build_and_upload.py` | `python scripts/pypi/build_and_upload.py` |
| **macOS/Linux** | `build_and_upload.sh` | `./scripts/pypi/build_and_upload.sh` |
| **Windows Enhanced** | `pypi.bat` | `build\pypi\pypi.bat` |ion management tools for the SPROCLIB project.

## Quick Start

### Three Main Actions

**1. Check/Set Version:**
```bash
# Check current version status
./scripts/manage_version/get_version.sh

# Update version for new release
./scripts/manage_version/set_version.ps1 2.0.5
```

**2. Build and Upload to PyPI:**
```bash
# Cross-platform Python script
python scripts/pypi/build_and_upload.py

# macOS/Linux shell script
./scripts/pypi/build_and_upload.sh

# Windows enhanced script
build\pypi\pypi.bat
```

**3. Documentation (ReadTheDocs):**
```bash
# Build documentation locally for testing
./scripts/readthedocs/sphinx.sh

# Note: ReadTheDocs builds automatically after git commits/pushes
# No manual action needed for production documentation
```

## Directory Structure

```
scripts/
├── README.md                     # This file - overview of all build tools
├── manage_version/               # Version management tools
│   ├── README.md                # Detailed version management documentation
│   ├── get_version.sh           # macOS/Unix version checker
│   ├── get_version.bat          # Windows batch version checker
│   ├── get_version.ps1          # Windows PowerShell version checker
│   ├── set_version.ps1          # PowerShell version updater
│   └── set_version.bat          # Windows batch version updater
├── pypi/                        # PyPI package build and upload tools
│   ├── build_and_upload.py     # Cross-platform PyPI build and upload script
│   └── pypi.bat                 # Windows-specific PyPI upload script
└── readthedocs/                 # ReadTheDocs and Sphinx documentation tools
    ├── README.md                # ReadTheDocs and Sphinx documentation
    ├── sphinx.sh                # Unix Sphinx build script
    ├── sphinx.bat               # Windows Sphinx build script
    └── test_rtd_config.py       # ReadTheDocs configuration tester
```

**Note:** The `readthedocs.yaml` configuration file is located in the project root directory (where ReadTheDocs expects it), not in the scripts/readthedocs/ subdirectory.

## Version Management Tools

### Cross-Platform Support

| **Platform** | **Script** | **Usage** |
|--------------|------------|-----------|
| **macOS/Linux** | `get_version.sh` | `./scripts/manage_version/get_version.sh` |
| **Windows CMD** | `get_version.bat` | `build\manage_version\get_version.bat` |
| **Windows PowerShell** | `get_version.ps1` | `.\build\manage_version\get_version.ps1` |

### Build and Upload Tools

| **Platform** | **Script** | **Usage** |
|--------------|------------|-----------|
| **Cross-platform** | `build_and_upload.py` | `python scripts/pypi/build_and_upload.py` |
| **Windows Enhanced** | `pypi.bat` | `build\pypi\pypi.bat` |

### Documentation Tools

| **Platform** | **Script** | **Usage** |
|--------------|------------|-----------|
| **macOS/Linux** | `sphinx.sh` | `./scripts/readthedocs/sphinx.sh` |
| **Windows** | `sphinx.bat` | `build\readthedocs\sphinx.bat` |
| **ReadTheDocs Config** | `readthedocs.yaml` | Located in project root |
| **RTD Tester** | `test_rtd_config.py` | `python scripts/readthedocs/test_rtd_config.py` |

### Version Checking

Check current version status across all project files:

```bash
# macOS/Linux
./scripts/manage_version/get_version.sh

# Windows Command Prompt
build\manage_version\get_version.bat

# Windows PowerShell (recommended)
.\build\manage_version\get_version.ps1
```

**Sample Output:**
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

### Version Updates

Update version numbers across all project files:

```bash
# PowerShell (recommended)
.\build\manage_version\set_version.ps1 2.0.5

# Windows batch
build\manage_version\set_version.bat 2.0.5
```

The version update scripts will:
- Update `pyproject.toml`
- Update `setup.py`
- Update `sproclib/__init__.py`
- Update documentation configuration
- Create git commit and tag
- Provide next steps for publishing

## Package Build and Distribution

### Build Script

Use the build scripts for package management:

**Cross-platform (recommended):**
```bash
python scripts/pypi/build_and_upload.py
```

**Windows-specific with enhanced features:**
```cmd
build\pypi\pypi.bat
```

These scripts will:
1. Clean previous build artifacts
2. Build the package using `python -m build`
3. Check the distribution with `twine check`
4. Provide commands for uploading to PyPI

The Windows `pypi.bat` script includes additional features like automatic `.pypirc` handling and dependency installation.

## Documentation Building

### Sphinx Documentation

Build documentation locally for testing:

**macOS/Linux:**
```bash
./scripts/readthedocs/sphinx.sh
```

**Windows:**
```cmd
build\readthedocs\sphinx.bat
```

These scripts will:
1. Activate the virtual environment if available
2. Install documentation dependencies
3. Build HTML documentation
4. Open the documentation in your browser

### ReadTheDocs Configuration

The `readthedocs.yaml` file (located in the project root) configures how the documentation is built on ReadTheDocs.io. Test the configuration with:

```bash
python scripts/readthedocs/test_rtd_config.py
```

### Manual Build Process

```bash
# Install build dependencies
pip install build twine

# Clean previous builds
rm -rf scripts/ dist/ *.egg-info/

# Build the package
python -m build

# Check the distribution
python -m twine check dist/*

# Upload to TestPyPI (recommended first)
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*
```

## Prerequisites

### For Version Management
- Git repository with version tags
- Python project with `pyproject.toml`, `setup.py`, and `__init__.py`

### For Package Building
```bash
pip install build twine
```

### For PyPI Upload
- PyPI account (https://pypi.org/)
- TestPyPI account (https://test.pypi.org/) - recommended for testing
- Configured credentials (`.pypirc` or environment variables)

## Workflow Integration

### Development Workflow

1. **Check current versions** before making changes:
   ```bash
   ./scripts/manage_version/get_version.sh
   ```

2. **Make your code changes**

3. **Update version** when ready for release:
   ```bash
   ./scripts/manage_version/set_version.ps1 2.0.5
   ```

4. **Build and test** the package:
   ```bash
   python scripts/pypi/build_and_upload.py
   ```

5. **Build documentation** (optional):
   ```bash
   ./scripts/readthedocs/sphinx.sh
   ```

6. **Upload to TestPyPI** first:
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```

7. **Test installation** from TestPyPI:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ sproclib
   ```

8. **Upload to PyPI** when ready:
   ```bash
   python -m twine upload dist/*
   ```

### CI/CD Integration

These scripts can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Check Version Consistency
  run: ./scripts/manage_version/get_version.sh

- name: Build Package
  run: python scripts/pypi/build_and_upload.py

- name: Build Documentation
  run: ./scripts/readthedocs/sphinx.sh

- name: Upload to PyPI
  run: python -m twine upload dist/*
  env:
    TWINE_USERNAME: __token__
    TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

## Status Indicators

The version checking scripts use these status indicators:

- **✅ Current Release** - Git tag represents the latest official release
- **✅ Matches git tag** - Version matches the current git tag
- **⚠️ Ahead of release** - Version is newer than git tag (prepared for next release)
- **❌ Outdated** - Version is older than the current git tag
- **❌ Version mismatch** - Version doesn't match expected pattern
- **❌ File not found** - Required file is missing

## Files Tracked

Version management scripts monitor:
- **Git Tags** - Official release versions (e.g., `v2.0.4`)
- **pyproject.toml** - Modern Python project configuration
- **sproclib/__init__.py** - Package version variable
- **setup.py** - Legacy setuptools configuration
- **docs/source/conf.py** - Sphinx documentation version

## Troubleshooting

### Version Inconsistencies
Run the version checker to identify issues, then use the version setter to fix them:
```bash
./scripts/manage_version/get_version.sh
./scripts/manage_version/set_version.ps1 <correct_version>
```

### Build Failures
1. Ensure all dependencies are installed: `pip install build twine`
2. Check for syntax errors in source code
3. Verify `pyproject.toml` and `setup.py` are properly configured

### Upload Failures
1. Verify PyPI credentials are configured
2. Check that version number hasn't been used before
3. Ensure package name is available on PyPI

## Best Practices

1. **Always check version status** before releases
2. **Use semantic versioning** (MAJOR.MINOR.PATCH)
3. **Test on TestPyPI first** before uploading to PyPI
4. **Keep version numbers consistent** across all files
5. **Tag releases in git** for tracking
6. **Update documentation** when bumping versions

## Support

For more detailed information:
- Version management: See `manage_version/README.md`
- Python packaging: https://packaging.python.org/
- PyPI help: https://pypi.org/help/
