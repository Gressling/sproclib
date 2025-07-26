# PyPI Package Management

This directory contains tools for building, testing, and uploading the SPROCLIB package to PyPI (Python Package Index).

## Files

- **`build_and_upload.py`** - Cross-platform Python script for package building
- **`pypi.bat`** - Windows batch script with enhanced PyPI features

## Usage

### Cross-Platform Build Script

```bash
python build/pypi/build_and_upload.py
```

This script will:
1. Clean previous build artifacts
2. Build the package using `python -m build`
3. Check the distribution with `twine check`
4. Provide commands for uploading to PyPI

### Windows Enhanced Script

```cmd
build\pypi\pypi.bat
```

The Windows batch script includes additional features:
- Automatic dependency installation
- Enhanced error handling
- `.pypirc` configuration assistance
- Color-coded output

## Prerequisites

Install the required build tools:

```bash
pip install build twine
```

## PyPI Account Setup

1. Create accounts on:
   - **PyPI**: https://pypi.org/account/register/
   - **TestPyPI**: https://test.pypi.org/account/register/ (for testing)

2. Generate API tokens:
   - Go to Account Settings → API tokens
   - Create tokens for PyPI and TestPyPI

3. Configure credentials in `~/.pypirc`:
   ```ini
   [distutils]
   index-servers = pypi testpypi

   [pypi]
   username = __token__
   password = pypi-your-api-token-here

   [testpypi]
   repository = https://test.pypi.org/legacy/
   username = __token__
   password = pypi-your-testpypi-token-here
   ```

## Workflow

### Testing Workflow

1. **Build the package**:
   ```bash
   python build/pypi/build_and_upload.py
   ```

2. **Upload to TestPyPI**:
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```

3. **Test installation**:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ sproclib
   ```

4. **Verify the package works correctly**

### Production Release

1. **Upload to PyPI**:
   ```bash
   python -m twine upload dist/*
   ```

2. **Verify on PyPI**: https://pypi.org/project/sproclib/

3. **Test installation from PyPI**:
   ```bash
   pip install sproclib
   ```

## Troubleshooting

### Common Issues

**Build fails with missing dependencies:**
```bash
pip install build twine setuptools wheel
```

**Upload fails with authentication error:**
- Check your API tokens in `~/.pypirc`
- Ensure you're using `__token__` as username

**Version already exists error:**
- PyPI doesn't allow re-uploading the same version
- Increment the version number using build tools

**Package name conflicts:**
- Check if the package name is available on PyPI
- Consider using a different name in `pyproject.toml`

### Manual Commands

If the scripts don't work, use these manual commands:

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build package
python -m build

# Check distribution
python -m twine check dist/*

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*
```

## Security Best Practices

1. **Use API tokens** instead of passwords
2. **Store tokens securely** in `~/.pypirc` with proper permissions
3. **Test on TestPyPI first** before production uploads
4. **Use virtual environments** for building
5. **Verify package contents** before uploading

## Integration

These scripts integrate with:
- **Version management**: Use `build/manage_version/` to set versions before building
- **Documentation**: Use `build/readthedocs/` to build docs before releasing
- **CI/CD**: Scripts can be called from GitHub Actions or other CI systems

## See Also

- **Version Management**: `../manage_version/README.md`
- **Documentation Building**: `../readthedocs/README.md`
- **Main Build Tools**: `../README.md`
