@ECHO OFF

pushd %~dp0

REM SPROCLIB Documentation Builder - Semantic Plant Design Core

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=source
set BUILDDIR=build
set PYTHON=python

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.https://www.sphinx-doc.org/
	exit /b 1
)

if "%1" == "" goto build
if "%1" == "help" goto help

REM Default Sphinx commands for any other arguments
%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:build
echo Building SPROCLIB Documentation
echo ================================
echo.
echo Cleaning previous build...
rmdir /s /q %BUILDDIR% 2>nul
rmdir /s /q %SOURCEDIR%\examples 2>nul

echo Building documentation...
if exist clean_and_build.py (
    %PYTHON% clean_and_build.py
    if errorlevel 1 (
        echo Python build script failed, falling back to direct Sphinx build
        %SPHINXBUILD% -b html -E %SOURCEDIR% %BUILDDIR%\html %SPHINXOPTS% %O%
    )
) else (
    echo clean_and_build.py not found, using direct Sphinx build
    %SPHINXBUILD% -b html -E %SOURCEDIR% %BUILDDIR%\html %SPHINXOPTS% %O%
)

echo.
echo SPROCLIB Documentation Build Complete!
echo Documentation ready at: %BUILDDIR%\html\index.html
goto end

:help
echo SPROCLIB Documentation Builder
echo ==============================
echo.
echo Usage: make [target]
echo.
echo Default (no target): Complete documentation build
echo.
echo Available targets:
echo   help        - Show this help
echo   html        - Build HTML documentation only
echo   pdf         - Build PDF documentation
echo   linkcheck   - Check for broken links
echo   clean       - Clean build directory
echo   clean-all   - Clean all artifacts including generated files
echo   quick       - Quick HTML build without cleaning
echo   semantic    - Complete build with semantic plant design focus
echo.
echo Standard Sphinx targets:
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:end
popd
