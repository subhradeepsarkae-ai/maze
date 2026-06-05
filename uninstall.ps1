# Maze Uninstaller
# Works in CMD and PowerShell.
#
# CMD:       curl -sL https://raw.githubusercontent.com/subhradeepsarkae-ai/maze/main/uninstall.ps1 | powershell -command -
# PowerShell: iwr -useb https://raw.githubusercontent.com/subhradeepsarkae-ai/maze/main/uninstall.ps1 | iex
# Direct:     pip uninstall maze -y

$ErrorActionPreference = "Continue"
Write-Host "=== Maze - Uninstalling ===" -ForegroundColor Yellow

$found = $false
python -m pip uninstall maze -y -q 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Maze package removed" -ForegroundColor Green
    $found = $true
}
python -m pip uninstall maze-maze -y -q 2>$null

if (-not $found) {
    Write-Host "[WARN] Maze was not installed via pip" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Green
Write-Host "Optional: Remove unused dependencies:" -ForegroundColor White
Write-Host "   pip uninstall yt-dlp rich -y" -ForegroundColor Cyan
