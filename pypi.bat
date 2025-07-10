@echo off
setlocal enabledelayedexpansion

echo ================================
echo SPROCLIB PyPI Build and Upload
echo ================================
echo.

REM Check if .pypirc exists in project directory and copy to user home
if exist ".pypirc" (
    echo Found .pypirc in project directory, copying to user home...
    copy ".pypirc" "%USERPROFILE%\.pypirc" >nul 2>&1
    echo .pypirc copied to %USERPROFILE%\.pypirc
    echo.
)

REM Check if required tools are installed
python -c "import build" 2>nul
if errorlevel 1 (
    echo Error: 'build' package not found. Installing...
    pip install build
)

python -c "import twine" 2>nul
if errorlevel 1 (
    echo Error: 'twine' package not found. Installing...
    pip install twine
)

echo.
echo [1/5] Cleaning previous builds...
if exist "build" (
    rmdir /s /q "build" 2>nul
    echo Removed build directory
)
if exist "dist" (
    rmdir /s /q "dist" 2>nul
    echo Removed dist directory
)
REM Clean all .egg-info directories
for /d %%i in (*.egg-info) do (
    if exist "%%i" (
        rmdir /s /q "%%i" 2>nul
        echo Removed %%i
    )
)
echo Done.

echo.
echo [2/5] Building package...
python -m build
if errorlevel 1 (
    echo Error: Build failed!
    pause
    exit /b 1
)
echo Done.

echo.
echo [3/5] Checking distribution...
python -m twine check dist/*
if errorlevel 1 (
    echo Error: Distribution check failed!
    pause
    exit /b 1
)
echo Done.

echo.
echo [4/5] Upload options:
echo 1. Upload to TestPyPI (recommended first)
echo 2. Upload to PyPI (production)
echo 3. Skip upload
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo [5/5] Uploading to TestPyPI...
    python -m twine upload --repository testpypi dist/*
    if errorlevel 1 (
        echo Error: TestPyPI upload failed!
        echo Make sure you have TestPyPI credentials configured.
    ) else (
        echo.
        echo Success! Package uploaded to TestPyPI.
        echo Test installation: pip install --index-url https://test.pypi.org/simple/ sproclib
    )
) else (
    if "%choice%"=="2" (
        echo.
        echo [5/5] Uploading to PyPI...
        python -m twine upload dist/*
        if errorlevel 1 (
            echo Error: PyPI upload failed!
            echo.
            echo Common causes:
            echo - Version already exists (you need to bump version in pyproject.toml)
            echo - Authentication issues (check credentials in %USERPROFILE%\.pypirc)
            echo.
            echo To fix version conflict:
            echo 1. Update version in pyproject.toml (e.g., 2.0.1, 2.1.0, etc.)
            echo 2. Re-run this script
        ) else (
            echo.
            echo ========================================
            echo SUCCESS! Package uploaded to PyPI
            echo ========================================
            echo.
            echo Your package is now available at:
            echo https://pypi.org/project/sproclib/
            echo.
            echo Installation command:
            echo pip install sproclib
        )
    ) else (
        echo.
        echo Upload skipped. Files are ready in dist/ folder.
        echo.
        echo Manual upload commands:
        echo   TestPyPI: python -m twine upload --repository testpypi dist/*
        echo   PyPI:     python -m twine upload dist/*
    )
)

echo.
echo Build process completed!
pause
