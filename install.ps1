# 🧩 Maze Installer
# Run: powershell -c "iwr -useb https://raw.githubusercontent.com/YOUR_USER/maze/main/install.ps1 | iex"

$ErrorActionPreference = "Stop"
$Host.UI.RawUI.ForegroundColor = "Yellow"
Write-Host "🧩 Maze - Installing..."
$Host.UI.RawUI.ForegroundColor = "White"

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "❌ Python not found. Install Python 3.8+ from https://python.org" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Python found: $($python.Source)" -ForegroundColor Green

python -m pip install --upgrade pip -q
python -m pip install yt-dlp rich --upgrade -q
Write-Host "✓ Dependencies installed" -ForegroundColor Green

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir
python -m pip install -e .
Write-Host "✓ Package installed" -ForegroundColor Green

$Host.UI.RawUI.ForegroundColor = "Green"
Write-Host "`n✅ Maze is ready! Open a NEW terminal and run:" -ForegroundColor Green
Write-Host "   mz https://youtube.com/watch?v=..." -ForegroundColor Cyan
Write-Host "   mz https://instagram.com/p/..." -ForegroundColor Cyan
Write-Host "   mz <url> --mute" -ForegroundColor Cyan
