@echo off
REM Maze Uninstaller
REM Works in CMD. PowerShell: iwr -useb https://raw.githubusercontent.com/subhradeepsarkae-ai/maze/main/uninstall.ps1 | iex
REM Direct: pip uninstall maze -y

echo === Maze - Uninstalling ===

pip uninstall maze -y -q 2>nul
if %errorlevel% equ 0 (
    echo [OK] Maze uninstalled
) else (
    echo [WARN] Maze was not installed or pip not found
)

echo.
echo === Done ===
echo Optional: Remove dependencies if no longer needed:
echo   pip uninstall yt-dlp rich -y
