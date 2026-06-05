# Maze Universal Installer
# Works in CMD and PowerShell.
#
# CMD:       curl -sL https://raw.githubusercontent.com/subhradeepsarkae-ai/maze/main/install.ps1 | powershell -command -
# PowerShell: iwr -useb https://raw.githubusercontent.com/subhradeepsarkae-ai/maze/main/install.ps1 | iex
# Direct:     pip install git+https://github.com/subhradeepsarkae-ai/maze.git

$ErrorActionPreference = "Stop"
Write-Host "=== Maze - Installing ===" -ForegroundColor Yellow

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "[ERROR] Python not found. Install Python 3.8+ from https://python.org" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Python found: $($python.Source)" -ForegroundColor Green

python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org -q
python -m pip install git+https://github.com/subhradeepsarkae-ai/maze.git --upgrade --trusted-host pypi.org --trusted-host files.pythonhosted.org -q
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Installation failed" -ForegroundColor Red
    exit 1
}

$mz = Get-Command mz -ErrorAction SilentlyContinue
if (-not $mz) {
    Write-Host "[WARN] 'mz' command not found in PATH." -ForegroundColor Yellow
    Write-Host "       RESTART your terminal, then run 'mz --help'." -ForegroundColor White
} else {
    Write-Host "[OK] Maze installed at $($mz.Source)" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Maze is ready! ===" -ForegroundColor Green
Write-Host "Usage:" -ForegroundColor White
Write-Host "   mz https://youtube.com/watch?v=...           Download menu" -ForegroundColor Cyan
Write-Host "   mz https://youtube.com/watch?v=... --fast    480p (no menu)" -ForegroundColor Cyan
Write-Host "   mz https://youtube.com/watch?v=... --high    Best quality (no menu)" -ForegroundColor Cyan
Write-Host "   mz https://youtube.com/watch?v=... --mute    Video only, no audio" -ForegroundColor Cyan
Write-Host "   mz --clip --fast                            URL from clipboard" -ForegroundColor Cyan
Write-Host "   mz --help" -ForegroundColor Dim
