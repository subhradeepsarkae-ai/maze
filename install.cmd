@echo off
REM Maze Universal Installer for CMD
REM ---------------------------------
REM Direct: pip install git+https://github.com/subhradeepsarkae-ai/maze.git

setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1

echo === Maze - Installing ===

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Install Python 3.8+ from https://python.org
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do echo [OK] %%i

python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org -q
python -m pip install git+https://github.com/subhradeepsarkae-ai/maze.git --upgrade --trusted-host pypi.org --trusted-host files.pythonhosted.org -q
if %errorlevel% neq 0 (
    echo [ERROR] Installation failed
    exit /b 1
)

where mz >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARN] 'mz' command not found in PATH.
    echo        RESTART your terminal, then run 'mz --help'.
) else (
    for /f "tokens=*" %%i in ('where mz') do echo [OK] Maze installed at %%i
)

echo.
echo === Maze is ready! ===
echo Usage:
echo   mz https://youtube.com/watch?v=...           Download menu
echo   mz https://youtube.com/watch?v=... --fast    480p (no menu)
echo   mz https://youtube.com/watch?v=... --high    Best quality (no menu)
echo   mz https://youtube.com/watch?v=... --mute    Video only, no audio
echo   mz --clip --fast                            URL from clipboard
echo   mz --help
