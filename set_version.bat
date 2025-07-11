@echo off
REM ========================================================================
REM SPROCLIB Version Update Script
REM ========================================================================
REM This script updates the version number across all project files and
REM creates a git tag for the new version.
REM
REM Usage: set_version.bat <version>
REM Example: set_version.bat 2.0.5
REM ========================================================================

setlocal enabledelayedexpansion

REM Check if version argument is provided
if "%~1"=="" (
    echo ERROR: Version number required
    echo Usage: set_version.bat ^<version^>
    echo Example: set_version.bat 2.0.5
    exit /b 1
)

set NEW_VERSION=%~1
echo.
echo ========================================================================
echo SPROCLIB Version Update Script
echo ========================================================================
echo Updating version to: %NEW_VERSION%
echo.

REM Validate version format (basic check for x.y.z pattern)
echo %NEW_VERSION% | findstr "." >nul
if errorlevel 1 (
    echo ERROR: Invalid version format. Expected format: x.y.z
    echo Example: 2.0.5
    exit /b 1
)
REM Simple check for dots - must contain at least one dot
echo %NEW_VERSION% | findstr "\." >nul
if errorlevel 1 (
    echo ERROR: Invalid version format. Expected format: x.y.z
    echo Example: 2.0.5
    exit /b 1
)

REM Check if we're in a git repository
git status >nul 2>&1
if errorlevel 1 (
    echo ERROR: Not in a git repository
    exit /b 1
)

REM Check for uncommitted changes
git diff --quiet
if errorlevel 1 (
    echo WARNING: You have uncommitted changes
    set /p confirm="Continue anyway? (y/N): "
    if /i not "!confirm!"=="y" (
        echo Aborted
        exit /b 1
    )
)

echo Step 1: Updating pyproject.toml...
powershell -Command "(Get-Content 'pyproject.toml') -replace 'version = \"[^\"]*\"', 'version = \"%NEW_VERSION%\"' | Set-Content 'pyproject.toml'"
if errorlevel 1 (
    echo ERROR: Failed to update pyproject.toml
    exit /b 1
)
echo   ✓ pyproject.toml updated

echo Step 2: Updating setup.py...
powershell -Command "(Get-Content 'setup.py') -replace 'version=\"[^\"]*\"', 'version=\"%NEW_VERSION%\"' | Set-Content 'setup.py'"
if errorlevel 1 (
    echo ERROR: Failed to update setup.py
    exit /b 1
)
echo   ✓ setup.py updated

echo Step 3: Updating main package __init__.py...
powershell -Command "(Get-Content 'sproclib\\__init__.py') -replace '__version__ = \"[^\"]*\"', '__version__ = \"%NEW_VERSION%\"' | Set-Content 'sproclib\\__init__.py'"
if errorlevel 1 (
    echo ERROR: Failed to update sproclib/__init__.py
    exit /b 1
)
powershell -Command "(Get-Content 'sproclib\\__init__.py') -replace 'Version: [^\"]*', 'Version: %NEW_VERSION%' | Set-Content 'sproclib\\__init__.py'"
echo   ✓ sproclib/__init__.py updated

echo Step 4: Updating plant module __init__.py...
powershell -Command "(Get-Content 'sproclib\\unit\\plant\\__init__.py') -replace '__version__ = ''[^'']*''', '__version__ = ''%NEW_VERSION%''' | Set-Content 'sproclib\\unit\\plant\\__init__.py'"
if errorlevel 1 (
    echo ERROR: Failed to update sproclib/unit/plant/__init__.py
    exit /b 1
)
echo   ✓ sproclib/unit/plant/__init__.py updated

echo Step 5: Updating Sphinx documentation...
powershell -Command "(Get-Content 'docs\\source\\conf.py') -replace 'release = ''[^'']*''', 'release = ''%NEW_VERSION%''' | Set-Content 'docs\\source\\conf.py'"
if errorlevel 1 (
    echo ERROR: Failed to update docs/source/conf.py release
    exit /b 1
)
powershell -Command "(Get-Content 'docs\\source\\conf.py') -replace 'version = ''[^'']*''', 'version = ''%NEW_VERSION%''' | Set-Content 'docs\\source\\conf.py'"
if errorlevel 1 (
    echo ERROR: Failed to update docs/source/conf.py version
    exit /b 1
)
echo   ✓ Sphinx documentation updated

echo Step 6: Checking for other version references...
findstr /r /s "__version__.*=.*[\"'][0-9]" sproclib\*.py >nul 2>&1
if not errorlevel 1 (
    echo   Found additional version references in Python files
    findstr /r /s "__version__.*=.*[\"'][0-9]" sproclib\*.py
)

echo.
echo Step 7: Git operations...
echo   Adding changes to git...
git add pyproject.toml setup.py sproclib\__init__.py sproclib\unit\plant\__init__.py docs\source\conf.py
if errorlevel 1 (
    echo ERROR: Failed to add files to git
    exit /b 1
)

echo   Creating commit...
git commit -m "Update version to %NEW_VERSION%"
if errorlevel 1 (
    echo ERROR: Failed to create commit
    exit /b 1
)

echo   Creating git tag...
git tag -a "v%NEW_VERSION%" -m "Release version %NEW_VERSION%"
if errorlevel 1 (
    echo ERROR: Failed to create git tag
    exit /b 1
)

echo.
echo ========================================================================
echo SUCCESS: Version updated to %NEW_VERSION%
echo ========================================================================
echo.
echo Updated files:
echo   • pyproject.toml
echo   • setup.py  
echo   • sproclib/__init__.py
echo   • sproclib/unit/plant/__init__.py
echo   • docs/source/conf.py
echo.
echo Git operations completed:
echo   • Committed changes
echo   • Created tag: v%NEW_VERSION%
echo.
echo Next steps:
echo   • Review changes: git show
echo   • Push changes: git push origin main
echo   • Push tags: git push origin v%NEW_VERSION%
echo   • Build documentation: python docs\build_docs.py
echo   • Upload to PyPI: python build_and_upload.py
echo.
echo ========================================================================

endlocal
