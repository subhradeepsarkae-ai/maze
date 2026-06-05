# Maze Universal Installer
# Run: powershell -c "iwr -useb https://raw.githubusercontent.com/subhradeepsarkae-ai/maze/main/install.ps1 | iex"

$ErrorActionPreference = "Stop"
$Host.UI.RawUI.ForegroundColor = "Yellow"
Write-Host "=== Maze - Installing ==="
$Host.UI.RawUI.ForegroundColor = "White"

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "[ERROR] Python not found. Install Python 3.8+ from https://python.org" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Python found: $($python.Source)" -ForegroundColor Green

python -m pip install --upgrade pip -q
Write-Host "[OK] pip upgraded" -ForegroundColor Green

python -m pip install git+https://github.com/subhradeepsarkae-ai/maze.git --upgrade -q
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Installation failed" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Maze installed" -ForegroundColor Green

$aria2 = Get-Command aria2c -ErrorAction SilentlyContinue
if (-not $aria2) {
    Write-Host "[INFO] Installing aria2c for faster downloads..." -ForegroundColor Yellow
    try {
        winget install aria2.aria2 --accept-package-agreements | Out-Null
        Write-Host "[OK] aria2c installed (restart terminal to use it)" -ForegroundColor Green
    } catch {
        Write-Host "[WARN] Could not install aria2c. Download manually: https://aria2.github.io" -ForegroundColor Yellow
    }
}

$Host.UI.RawUI.ForegroundColor = "Green"
Write-Host ""
Write-Host "=== Maze is ready! ===" -ForegroundColor Green
Write-Host "RESTART your terminal, then run:" -ForegroundColor White
Write-Host "   mz https://youtube.com/watch?v=..." -ForegroundColor Cyan
Write-Host "   mz https://instagram.com/p/..." -ForegroundColor Cyan
Write-Host "   mz <url> --mute" -ForegroundColor Cyan
