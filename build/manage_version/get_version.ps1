# ========================================================================
# SPROCLIB Version Check Script (PowerShell)
# ========================================================================
# This script checks and displays the version numbers across all project 
# files and compares them for consistency.
#
# Usage: .\get_version.ps1
# ========================================================================

Write-Host "`n🔍 Current SPROCLIB Version Status" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "`n📋 Version Information:`n" -ForegroundColor Yellow

# Table header
Write-Host "Source               Version    Status" -ForegroundColor White
Write-Host "--------------------------------------------------------" -ForegroundColor Gray

# Get Git tag version
$gitTag = ""
$gitVersion = ""
try {
    $gitTag = git tag --sort=-v:refname 2>$null | Select-Object -First 1
    if ($gitTag) {
        $gitVersion = $gitTag -replace '^v', ''  # Remove 'v' prefix if present
        Write-Host ("Git Tag (Latest)     {0,-10} " -f $gitTag) -NoNewline
        Write-Host "✅ Current Release" -ForegroundColor Green
    } else {
        Write-Host ("Git Tag (Latest)     {0,-10} " -f "N/A") -NoNewline
        Write-Host "❌ No tags found" -ForegroundColor Red
    }
} catch {
    Write-Host ("Git Tag (Latest)     {0,-10} " -f "N/A") -NoNewline
    Write-Host "❌ Not a git repo" -ForegroundColor Red
}

# Get pyproject.toml version
$pyprojectVersion = ""
if (Test-Path "pyproject.toml") {
    $content = Get-Content "pyproject.toml" | Where-Object { $_ -match '^version = ' }
    if ($content) {
        $pyprojectVersion = ($content -split '"')[1]
        Write-Host ("pyproject.toml       {0,-10} " -f $pyprojectVersion) -NoNewline
        if ($pyprojectVersion -eq $gitVersion) {
            Write-Host "✅ Matches git tag" -ForegroundColor Green
        } elseif ($gitVersion -and [version]$pyprojectVersion -gt [version]$gitVersion) {
            Write-Host "⚠️ Ahead of release" -ForegroundColor Yellow
        } else {
            Write-Host "❌ Version mismatch" -ForegroundColor Red
        }
    } else {
        Write-Host ("pyproject.toml       {0,-10} " -f "N/A") -NoNewline
        Write-Host "❌ Not found" -ForegroundColor Red
    }
} else {
    Write-Host ("pyproject.toml       {0,-10} " -f "N/A") -NoNewline
    Write-Host "❌ File not found" -ForegroundColor Red
}

# Get __init__.py version
$initVersion = ""
if (Test-Path "sproclib\__init__.py") {
    $content = Get-Content "sproclib\__init__.py" | Where-Object { $_ -match '^__version__ = ' }
    if ($content) {
        $initVersion = ($content -split '"')[1]
        Write-Host ("__init__.py          {0,-10} " -f $initVersion) -NoNewline
        if ($initVersion -eq $gitVersion) {
            Write-Host "✅ Matches git tag" -ForegroundColor Green
        } elseif ($gitVersion -and [version]$initVersion -gt [version]$gitVersion) {
            Write-Host "⚠️ Ahead of release" -ForegroundColor Yellow
        } elseif ($gitVersion -and [version]$initVersion -lt [version]$gitVersion) {
            Write-Host "❌ Outdated" -ForegroundColor Red
        } else {
            Write-Host "❌ Version mismatch" -ForegroundColor Red
        }
    } else {
        Write-Host ("__init__.py          {0,-10} " -f "N/A") -NoNewline
        Write-Host "❌ Not found" -ForegroundColor Red
    }
} else {
    Write-Host ("__init__.py          {0,-10} " -f "N/A") -NoNewline
    Write-Host "❌ File not found" -ForegroundColor Red
}

# Get setup.py version
$setupVersion = ""
if (Test-Path "setup.py") {
    $content = Get-Content "setup.py" | Where-Object { $_ -match 'version=' }
    if ($content) {
        $setupVersion = ($content -split '"')[1]
        Write-Host ("setup.py             {0,-10} " -f $setupVersion) -NoNewline
        if ($setupVersion -eq $gitVersion) {
            Write-Host "✅ Matches git tag" -ForegroundColor Green
        } elseif ($gitVersion -and [version]$setupVersion -gt [version]$gitVersion) {
            Write-Host "⚠️ Ahead of release" -ForegroundColor Yellow
        } elseif ($gitVersion -and [version]$setupVersion -lt [version]$gitVersion) {
            Write-Host "❌ Outdated" -ForegroundColor Red
        } else {
            Write-Host "❌ Version mismatch" -ForegroundColor Red
        }
    } else {
        Write-Host ("setup.py             {0,-10} " -f "N/A") -NoNewline
        Write-Host "❌ Not found" -ForegroundColor Red
    }
} else {
    Write-Host ("setup.py             {0,-10} " -f "N/A") -NoNewline
    Write-Host "❌ File not found" -ForegroundColor Red
}

Write-Host "`n📊 Summary:" -ForegroundColor Yellow

# Count issues
$issues = 0
$total = 0
if ($gitVersion) {
    if ($pyprojectVersion -and $pyprojectVersion -ne $gitVersion) { $issues++ }
    if ($initVersion -and $initVersion -ne $gitVersion) { $issues++ }
    if ($setupVersion -and $setupVersion -ne $gitVersion) { $issues++ }
    $total = 3
}

if ($issues -eq 0) {
    Write-Host "✅ All versions are consistent" -ForegroundColor Green
} else {
    Write-Host "⚠️  Found $issues version inconsistencies out of $($total + 1) files" -ForegroundColor Yellow
    Write-Host "`n💡 Recommendations:" -ForegroundColor Blue
    Write-Host "   • Use build\manage_version\set_version.ps1 to update all versions"
    if ($gitTag) {
        Write-Host "   • Current release version appears to be: $gitTag"
    }
}

Write-Host "`n🛠️  Available commands:" -ForegroundColor Cyan
Write-Host "   • Update versions: build\manage_version\set_version.ps1 <version>"
Write-Host "   • Check again: build\manage_version\get_version.ps1"
Write-Host ""
