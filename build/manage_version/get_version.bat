@echo off
REM ========================================================================
REM SPROCLIB Version Check Script (Windows)
REM ========================================================================
REM This script checks and displays the version numbers across all project 
REM files and compares them for consistency.
REM
REM Usage: get_version.bat
REM ========================================================================

setlocal enabledelayedexpansion

echo.
echo 🔍 Current SPROCLIB Version Status
echo ==================================
echo.
echo 📋 Version Information:
echo.

REM Table header
echo Source               Version    Status
echo --------------------------------------------------------

REM Get Git tag version
set GIT_VERSION=
set GIT_TAG=
for /f "tokens=*" %%i in ('git tag --sort=-v:refname 2^>nul') do (
    set GIT_TAG=%%i
    goto :got_tag
)
:got_tag
if defined GIT_TAG (
    REM Remove 'v' prefix if present
    set GIT_VERSION=!GIT_TAG:v=!
    echo Git Tag ^(Latest^)     !GIT_TAG!      ✅ Current Release
) else (
    echo Git Tag ^(Latest^)     N/A        ❌ No tags found
)

REM Get pyproject.toml version
set PYPROJECT_VERSION=
if exist "pyproject.toml" (
    for /f "tokens=3 delims= " %%i in ('findstr "^version = " pyproject.toml 2^>nul') do (
        set PYPROJECT_VERSION=%%i
        REM Remove quotes
        set PYPROJECT_VERSION=!PYPROJECT_VERSION:"=!
    )
    if defined PYPROJECT_VERSION (
        if "!PYPROJECT_VERSION!"=="!GIT_VERSION!" (
            echo pyproject.toml       !PYPROJECT_VERSION!      ✅ Matches git tag
        ) else if defined GIT_VERSION (
            REM Simple version comparison - if different, assume ahead
            echo pyproject.toml       !PYPROJECT_VERSION!      ⚠️ Ahead of release
        ) else (
            echo pyproject.toml       !PYPROJECT_VERSION!      ❌ Version mismatch
        )
    ) else (
        echo pyproject.toml       N/A        ❌ Not found
    )
) else (
    echo pyproject.toml       N/A        ❌ File not found
)

REM Get __init__.py version
set INIT_VERSION=
if exist "sproclib\__init__.py" (
    for /f "tokens=3 delims= " %%i in ('findstr "__version__ = " sproclib\__init__.py 2^>nul') do (
        set INIT_VERSION=%%i
        REM Remove quotes
        set INIT_VERSION=!INIT_VERSION:"=!
    )
    if defined INIT_VERSION (
        if "!INIT_VERSION!"=="!GIT_VERSION!" (
            echo __init__.py          !INIT_VERSION!      ✅ Matches git tag
        ) else if defined GIT_VERSION (
            REM Check if version is less than git version
            if "!INIT_VERSION!" LSS "!GIT_VERSION!" (
                echo __init__.py          !INIT_VERSION!      ❌ Outdated
            ) else (
                echo __init__.py          !INIT_VERSION!      ⚠️ Ahead of release
            )
        ) else (
            echo __init__.py          !INIT_VERSION!      ❌ Version mismatch
        )
    ) else (
        echo __init__.py          N/A        ❌ Not found
    )
) else (
    echo __init__.py          N/A        ❌ File not found
)

REM Get setup.py version
set SETUP_VERSION=
if exist "setup.py" (
    for /f "tokens=1 delims=," %%i in ('findstr "version=" setup.py 2^>nul') do (
        set TEMP_LINE=%%i
        for /f "tokens=2 delims==" %%j in ("!TEMP_LINE!") do (
            set SETUP_VERSION=%%j
            REM Remove quotes and spaces
            set SETUP_VERSION=!SETUP_VERSION:"=!
            set SETUP_VERSION=!SETUP_VERSION: =!
        )
    )
    if defined SETUP_VERSION (
        if "!SETUP_VERSION!"=="!GIT_VERSION!" (
            echo setup.py             !SETUP_VERSION!      ✅ Matches git tag
        ) else if defined GIT_VERSION (
            REM Check if version is less than git version
            if "!SETUP_VERSION!" LSS "!GIT_VERSION!" (
                echo setup.py             !SETUP_VERSION!      ❌ Outdated
            ) else (
                echo setup.py             !SETUP_VERSION!      ⚠️ Ahead of release
            )
        ) else (
            echo setup.py             !SETUP_VERSION!      ❌ Version mismatch
        )
    ) else (
        echo setup.py             N/A        ❌ Not found
    )
) else (
    echo setup.py             N/A        ❌ File not found
)

echo.
echo 📊 Summary:

REM Count issues (simplified)
set ISSUES=0
if defined GIT_VERSION (
    if defined PYPROJECT_VERSION (
        if not "!PYPROJECT_VERSION!"=="!GIT_VERSION!" set /a ISSUES+=1
    )
    if defined INIT_VERSION (
        if not "!INIT_VERSION!"=="!GIT_VERSION!" set /a ISSUES+=1
    )
    if defined SETUP_VERSION (
        if not "!SETUP_VERSION!"=="!GIT_VERSION!" set /a ISSUES+=1
    )
)

if !ISSUES! EQU 0 (
    echo ✅ All versions are consistent
) else (
    echo ⚠️  Found !ISSUES! version inconsistencies
    echo.
    echo 💡 Recommendations:
    echo    • Use build\manage_version\set_version.bat to update all versions
    if defined GIT_TAG echo    • Current release version appears to be: !GIT_TAG!
)

echo.
echo 🛠️  Available commands:
echo    • Update versions: build\manage_version\set_version.bat ^<version^>
echo    • Check again: build\manage_version\get_version.bat
echo.

endlocal
