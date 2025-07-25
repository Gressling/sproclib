@echo off
REM ========================================================================
REM SPROCLIB Version Update Script
REM ========================================================================
REM This script updates the version number across all project files,
REM creates a git tag for the new version, and pushes everything to remote.
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
powershell -Command "$utf8NoBom = New-Object System.Text.UTF8Encoding $false; [System.IO.File]::WriteAllText('pyproject.toml', ([System.IO.File]::ReadAllText('pyproject.toml') -replace 'version = \"[^\"]*\"', 'version = \"%NEW_VERSION%\"'), $utf8NoBom)"
if errorlevel 1 (
    echo ERROR: Failed to update pyproject.toml
    exit /b 1
)
echo   ✓ pyproject.toml updated

echo Step 2: Updating setup.py...
powershell -Command "$utf8NoBom = New-Object System.Text.UTF8Encoding $false; [System.IO.File]::WriteAllText('setup.py', ([System.IO.File]::ReadAllText('setup.py') -replace 'version=\"[^\"]*\"', 'version=\"%NEW_VERSION%\"'), $utf8NoBom)"
if errorlevel 1 (
    echo ERROR: Failed to update setup.py
    exit /b 1
)
echo   ✓ setup.py updated

echo Step 3: Updating main package __init__.py...
powershell -Command "$utf8NoBom = New-Object System.Text.UTF8Encoding $false; $file = 'sproclib\\__init__.py'; $content = [System.IO.File]::ReadAllText($file); $content = $content -replace '__version__ = \"[^\"]*\"', '__version__ = \"%NEW_VERSION%\"'; $content = $content -replace 'Version: [^\\r\\n]*', 'Version: %NEW_VERSION%'; [System.IO.File]::WriteAllText($file, $content, $utf8NoBom)"
if errorlevel 1 (
    echo ERROR: Failed to update sproclib/__init__.py
    exit /b 1
)
echo   ✓ sproclib/__init__.py updated

echo Step 4: Updating plant module __init__.py...
powershell -Command "$utf8NoBom = New-Object System.Text.UTF8Encoding $false; [System.IO.File]::WriteAllText('sproclib\\unit\\plant\\__init__.py', ([System.IO.File]::ReadAllText('sproclib\\unit\\plant\\__init__.py') -replace '__version__ = ''[^'']*''', '__version__ = ''%NEW_VERSION%'''), $utf8NoBom)"
if errorlevel 1 (
    echo ERROR: Failed to update sproclib/unit/plant/__init__.py
    exit /b 1
)
echo   ✓ sproclib/unit/plant/__init__.py updated

echo Step 5: Updating Sphinx documentation...
powershell -Command "$utf8NoBom = New-Object System.Text.UTF8Encoding $false; $file = 'docs\\source\\conf.py'; $content = [System.IO.File]::ReadAllText($file); $content = $content -replace 'release = ''[^'']*''', 'release = ''%NEW_VERSION%'''; $content = $content -replace 'version = ''[^'']*''', 'version = ''%NEW_VERSION%'''; [System.IO.File]::WriteAllText($file, $content, $utf8NoBom)"
if errorlevel 1 (
    echo ERROR: Failed to update docs/source/conf.py
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

echo   Pushing commit to remote...
git push origin main
if errorlevel 1 (
    echo ERROR: Failed to push commit to remote
    exit /b 1
)

echo   Pushing tag to remote...
git push origin "v%NEW_VERSION%"
if errorlevel 1 (
    echo ERROR: Failed to push tag to remote
    exit /b 1
)

echo.
echo ========================================================================
echo SUCCESS: Version updated to %NEW_VERSION%
echo ========================================================================
echo.
echo Updated files:
echo   - pyproject.toml
echo   - setup.py  
echo   - sproclib/__init__.py
echo   - sproclib/unit/plant/__init__.py
echo   - docs/source/conf.py
echo.
echo Git operations completed:
echo   - Committed changes
echo   - Created tag: v%NEW_VERSION%
echo   - Pushed commit to remote
echo   - Pushed tag to remote
echo.
echo Next steps:
echo   - Review changes: git show
echo   - Build documentation: python docs\build_docs.py
echo   - Upload to PyPI: python build_and_upload.py
echo.
echo ========================================================================

endlocal
