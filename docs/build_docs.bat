@echo off
REM Local Sphinx Documentation Build Script for SPROCLIB
REM Usage: build_docs.bat [clean]

echo 🔧 SPROCLIB Documentation Builder
echo ========================================

cd /d "%~dp0"

if "%1"=="clean" (
    echo 🧹 Cleaning existing build directory...
    if exist "build" rmdir /s /q "build"
    echo    ✓ Build directory cleaned
)

echo 📖 Building documentation...
echo    Source: source
echo    Output: build\html
echo.

sphinx-build -b html -E source build\html

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ Documentation build completed successfully!
    echo 📂 Output directory: build\html
    echo 🌐 Open in browser: file:///%CD%\build\html\index.html
    echo.
    echo 🚀 Opening documentation in your default browser...
    start "" "build\html\index.html"
) else (
    echo.
    echo ❌ Build failed with return code %ERRORLEVEL%
    echo Make sure Sphinx is installed: pip install -r requirements-docs.txt
    pause
)
