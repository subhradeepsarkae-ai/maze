@echo off
REM Maze Uninstaller for CMD
REM -------------------------
REM Direct: pip uninstall maze -y

setlocal
chcp 65001 >nul 2>&1

echo === Maze - Uninstalling ===

set FOUND=0
pip uninstall maze -y -q 2>nul
if %errorlevel% equ 0 (
    echo [OK] Maze package removed
    set FOUND=1
)
pip uninstall maze-maze -y -q 2>nul

if %FOUND% equ 0 (
    echo [WARN] Maze was not installed via pip
)

echo.
echo === Done ===
echo Optional: Remove unused dependencies:
echo   pip uninstall yt-dlp rich -y
