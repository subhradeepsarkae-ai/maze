# Maze Uninstaller
# Works in CMD and PowerShell.
#
# CMD:       curl -sL https://raw.githubusercontent.com/subhradeepsarkae-ai/maze/main/uninstall.ps1 | powershell -command -
# PowerShell: iwr -useb https://raw.githubusercontent.com/subhradeepsarkae-ai/maze/main/uninstall.ps1 | iex
# Direct:     pip uninstall maze -y

$ErrorActionPreference = "Stop"
Write-Host "=== Maze - Uninstalling ===" -ForegroundColor Yellow

python -m pip uninstall maze -y -q 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Maze uninstalled" -ForegroundColor Green
} else {
    Write-Host "[WARN] Maze was not installed or pip not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Green
Write-Host "Optional: Remove dependencies if no longer needed:" -ForegroundColor White
Write-Host "   pip uninstall yt-dlp rich -y" -foregroundcolor Cyan
