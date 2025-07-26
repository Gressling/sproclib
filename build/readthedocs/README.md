# ReadTheDocs Documentation Tools

This directory contains tools for building and deploying documentation using Sphinx and ReadTheDocs.io.

## Files

- **`sphinx.sh`** - Unix/macOS script for building Sphinx documentation
- **`sphinx.bat`** - Windows script for building Sphinx documentation  
- **`test_rtd_config.py`** - Script to test ReadTheDocs configuration
- **`README.md`** - This documentation file

**Note:** The `.readthedocs.yaml` configuration file is located in the project root directory, where ReadTheDocs.io expects to find it.

## Usage

### Local Documentation Building

**macOS/Linux:**
```bash
./build/readthedocs/sphinx.sh
```

**Windows:**
```cmd
build\readthedocs\sphinx.bat
```

Both scripts will:
1. Activate virtual environment if available
2. Install documentation dependencies
3. Build HTML documentation with Sphinx
4. Open the documentation in your default browser

### Build Options

The Sphinx scripts support a `clean` option to remove previous builds:

```bash
# Clean and rebuild
./build/readthedocs/sphinx.sh clean

# Windows
build\readthedocs\sphinx.bat clean
```

### ReadTheDocs Configuration Testing

Test the ReadTheDocs configuration before deploying:

```bash
python build/readthedocs/test_rtd_config.py
```

This will validate:
- YAML syntax
- Required configuration fields
- Python and dependency specifications
- Build configuration

## ReadTheDocs.io Setup

### Configuration File

The `.readthedocs.yaml` file (located in the project root) configures:
- **Build environment** (Ubuntu version, Python version)
- **Python dependencies** (requirements files)
- **Sphinx configuration** (source directory, output formats)
- **Build process** (pre-build commands)

Example configuration structure:
```yaml
version: 2
build:
  os: ubuntu-22.04
  tools:
    python: "3.11"
python:
  install:
    - requirements: docs/requirements-docs.txt
    - method: pip
      path: .
sphinx:
  configuration: docs/source/conf.py
formats:
  - pdf
  - epub
```

### Project Setup on ReadTheDocs

1. **Connect Repository**:
   - Go to https://readthedocs.org/
   - Import your GitHub repository
   - Select the branch to build from

2. **Configure Build**:
   - ReadTheDocs will automatically detect `.readthedocs.yaml`
   - Builds will trigger on git pushes
   - Configure webhook if needed

3. **Custom Domain** (optional):
   - Set up custom domain in project settings
   - Configure DNS records as instructed

## Prerequisites

### Local Development

Install documentation dependencies:

```bash
# Install from requirements file
pip install -r docs/requirements-docs.txt

# Or install individual packages
pip install sphinx furo sphinx-autodoc-typehints
```

### Required Project Structure

```
docs/
├── source/
│   ├── conf.py              # Sphinx configuration
│   ├── index.rst            # Main documentation page
│   └── ...                  # Other RST files
├── requirements-docs.txt    # Documentation dependencies
└── ...
```

## Sphinx Configuration

Key configuration in `docs/source/conf.py`:

```python
# Project information
project = 'SPROCLIB'
author = 'Thorsten Gressling'
release = '2.0.4'

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

# Theme
html_theme = 'furo'
```

## Documentation Workflow

### Development Workflow

1. **Edit documentation files** in `docs/source/`
2. **Build locally** to test changes:
   ```bash
   ./build/readthedocs/sphinx.sh
   ```
3. **Review output** in browser
4. **Commit and push** changes
5. **ReadTheDocs builds automatically**

### Release Workflow

1. **Update version** in documentation:
   ```bash
   # Version management scripts update docs/source/conf.py
   ./build/manage_version/set_version.ps1 2.0.5
   ```

2. **Build and test locally**:
   ```bash
   ./build/readthedocs/sphinx.sh clean
   ```

3. **Commit documentation updates**

4. **Create release tag** (triggers RTD build)

5. **Verify on ReadTheDocs.io**

## Troubleshooting

### Common Build Issues

**Missing dependencies:**
```bash
pip install -r docs/requirements-docs.txt
```

**Import errors in autodoc:**
- Ensure the package is installable
- Check Python path in `conf.py`
- Verify all dependencies are listed

**Theme not found:**
```bash
pip install furo  # or your chosen theme
```

### ReadTheDocs Build Failures

**Check build logs** on ReadTheDocs.io:
1. Go to project dashboard
2. Click on "Builds" tab
3. Review failed build logs

**Common fixes:**
- Update `.readthedocs.yaml` Python version
- Add missing dependencies to requirements file
- Fix import paths in documentation

### Configuration Validation

Run the configuration tester:
```bash
python build/readthedocs/test_rtd_config.py
```

This will report:
- ✅ Valid configuration elements
- ❌ Missing or invalid settings
- ⚠️ Warnings about deprecated options

## Advanced Features

### PDF Generation

Enable PDF output in `.readthedocs.yaml`:
```yaml
formats:
  - htmlzip
  - pdf
  - epub
```

### Versioned Documentation

ReadTheDocs automatically creates versions for:
- Git branches
- Git tags
- Latest commit

Configure version handling in project settings.

### Custom Build Commands

Add pre-build commands in `.readthedocs.yaml`:
```yaml
build:
  jobs:
    pre_build:
      - echo "Running custom pre-build commands"
      - python scripts/generate_api_docs.py
```

## Integration

### With Other Build Tools

- **Version Management**: Documentation version automatically updated by version scripts
- **PyPI Publishing**: Documentation should be updated before package releases
- **CI/CD**: Documentation builds can be tested in GitHub Actions

### GitHub Actions Example

```yaml
- name: Test Documentation Build
  run: ./build/readthedocs/sphinx.sh

- name: Test RTD Configuration  
  run: python build/readthedocs/test_rtd_config.py
```

## Best Practices

1. **Test builds locally** before pushing
2. **Use semantic versioning** in documentation
3. **Keep dependencies minimal** and pinned
4. **Write clear docstrings** for autodoc
5. **Organize content logically** with good navigation
6. **Use consistent RST formatting**
7. **Include examples and tutorials**

## See Also

- **Sphinx Documentation**: https://www.sphinx-doc.org/
- **ReadTheDocs Guide**: https://docs.readthedocs.io/
- **reStructuredText Primer**: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
- **Version Management**: `../manage_version/README.md`
- **Main Build Tools**: `../README.md`
