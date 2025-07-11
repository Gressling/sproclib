# ========================================================================
# SPROCLIB Version Update Script (PowerShell)
# ========================================================================
# This script updates the version number across all project files and
# creates a git tag for the new version.
#
# Usage: .\set_version.ps1 <version>
# Example: .\set_version.ps1 2.0.5
# ========================================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$Version
)

# Function to update version in a file with regex replacement
function Update-VersionInFile {
    param(
        [string]$FilePath,
        [string]$Pattern,
        [string]$Replacement
    )
    
    if (Test-Path $FilePath) {
        try {
            $content = Get-Content $FilePath -Raw
            $newContent = $content -replace $Pattern, $Replacement
            Set-Content -Path $FilePath -Value $newContent -NoNewline
            return $true
        }
        catch {
            Write-Error "Failed to update $FilePath`: $_"
            return $false
        }
    }
    else {
        Write-Warning "File not found: $FilePath"
        return $false
    }
}

# Validate version format
if ($Version -notmatch '^\d+\.\d+\.\d+$') {
    Write-Error "Invalid version format. Expected format: x.y.z (e.g., 2.0.5)"
    exit 1
}

Write-Host ""
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "SPROCLIB Version Update Script" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "Updating version to: $Version" -ForegroundColor Yellow
Write-Host ""

# Check if we're in a git repository
try {
    git status | Out-Null
}
catch {
    Write-Error "Not in a git repository"
    exit 1
}

# Check for uncommitted changes
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Warning "You have uncommitted changes:"
    Write-Host $gitStatus
    $confirm = Read-Host "Continue anyway? (y/N)"
    if ($confirm -ne "y" -and $confirm -ne "Y") {
        Write-Host "Aborted" -ForegroundColor Red
        exit 1
    }
}

$success = $true

# Update pyproject.toml
Write-Host "Step 1: Updating pyproject.toml..." -ForegroundColor Green
if (Update-VersionInFile -FilePath "pyproject.toml" -Pattern 'version = "[^"]*"' -Replacement "version = `"$Version`"") {
    Write-Host "  ✓ pyproject.toml updated" -ForegroundColor Green
} else {
    $success = $false
}

# Update setup.py
Write-Host "Step 2: Updating setup.py..." -ForegroundColor Green
if (Update-VersionInFile -FilePath "setup.py" -Pattern 'version="[^"]*"' -Replacement "version=`"$Version`"") {
    Write-Host "  ✓ setup.py updated" -ForegroundColor Green
} else {
    $success = $false
}

# Update main package __init__.py
Write-Host "Step 3: Updating main package __init__.py..." -ForegroundColor Green
$initFile = "sproclib\__init__.py"
if (Update-VersionInFile -FilePath $initFile -Pattern '__version__ = "[^"]*"' -Replacement "__version__ = `"$Version`"") {
    # Also update the docstring version
    Update-VersionInFile -FilePath $initFile -Pattern 'Version: [^\n]*' -Replacement "Version: $Version" | Out-Null
    Write-Host "  ✓ sproclib/__init__.py updated" -ForegroundColor Green
} else {
    $success = $false
}

# Update plant module __init__.py
Write-Host "Step 4: Updating plant module __init__.py..." -ForegroundColor Green
if (Update-VersionInFile -FilePath "sproclib\unit\plant\__init__.py" -Pattern "__version__ = '[^']*'" -Replacement "__version__ = '$Version'") {
    Write-Host "  ✓ sproclib/unit/plant/__init__.py updated" -ForegroundColor Green
} else {
    $success = $false
}

# Update Sphinx documentation
Write-Host "Step 5: Updating Sphinx documentation..." -ForegroundColor Green
$confFile = "docs\source\conf.py"
$sphinx1 = Update-VersionInFile -FilePath $confFile -Pattern "release = '[^']*'" -Replacement "release = '$Version'"
$sphinx2 = Update-VersionInFile -FilePath $confFile -Pattern "version = '[^']*'" -Replacement "version = '$Version'"
if ($sphinx1 -and $sphinx2) {
    Write-Host "  ✓ Sphinx documentation updated" -ForegroundColor Green
} else {
    $success = $false
}

# Check for other version references
Write-Host "Step 6: Checking for other version references..." -ForegroundColor Green
$otherVersions = Select-String -Path "sproclib\*.py" -Pattern "__version__.*=.*[`"'][0-9]" -Recurse
if ($otherVersions) {
    Write-Host "  Found additional version references:" -ForegroundColor Yellow
    $otherVersions | ForEach-Object { Write-Host "    $($_.Filename):$($_.LineNumber) - $($_.Line.Trim())" -ForegroundColor Yellow }
}

if (-not $success) {
    Write-Error "Some files failed to update. Please check the errors above."
    exit 1
}

# Git operations
Write-Host ""
Write-Host "Step 7: Git operations..." -ForegroundColor Green

Write-Host "  Adding changes to git..." -ForegroundColor Cyan
$filesToAdd = @(
    "pyproject.toml",
    "setup.py", 
    "sproclib\__init__.py",
    "sproclib\unit\plant\__init__.py",
    "docs\source\conf.py"
)

try {
    git add @filesToAdd
    Write-Host "  ✓ Files added to git" -ForegroundColor Green
    
    Write-Host "  Creating commit..." -ForegroundColor Cyan
    git commit -m "Update version to $Version"
    Write-Host "  ✓ Commit created" -ForegroundColor Green
    
    Write-Host "  Creating git tag..." -ForegroundColor Cyan
    git tag -a "v$Version" -m "Release version $Version"
    Write-Host "  ✓ Tag v$Version created" -ForegroundColor Green
}
catch {
    Write-Error "Git operations failed: $_"
    exit 1
}

# Success summary
Write-Host ""
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "SUCCESS: Version updated to $Version" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Updated files:" -ForegroundColor Yellow
Write-Host "  • pyproject.toml" -ForegroundColor White
Write-Host "  • setup.py" -ForegroundColor White
Write-Host "  • sproclib/__init__.py" -ForegroundColor White
Write-Host "  • sproclib/unit/plant/__init__.py" -ForegroundColor White
Write-Host "  • docs/source/conf.py" -ForegroundColor White
Write-Host ""
Write-Host "Git operations completed:" -ForegroundColor Yellow
Write-Host "  • Committed changes" -ForegroundColor White
Write-Host "  • Created tag: v$Version" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  • Review changes: git show" -ForegroundColor White
Write-Host "  • Push changes: git push origin main" -ForegroundColor White
Write-Host "  • Push tags: git push origin v$Version" -ForegroundColor White
Write-Host "  • Build documentation: python docs\build_docs.py" -ForegroundColor White
Write-Host "  • Upload to PyPI: python build_and_upload.py" -ForegroundColor White
Write-Host ""
Write-Host "========================================================================" -ForegroundColor Cyan
