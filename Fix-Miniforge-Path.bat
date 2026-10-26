@echo off
chcp 65001 >nul 2>&1
title Fix .miniforge-base
cd /d "%~dp0"
set "TOOL_ROOT=%CD%"

where conda >nul 2>nul
if errorlevel 1 (
  echo Open this file from "Miniforge Prompt", not plain cmd.
  pause
  exit /b 1
)

echo Current conda base:
for /f "delims=" %%G in ('conda info --base 2^>nul') do (
  echo %%G
  echo %%G> "%TOOL_ROOT%\.miniforge-base"
  echo %%G> "%TOOL_ROOT%\.conda-base"
)
echo.
echo Wrote .miniforge-base in:
echo   %TOOL_ROOT%
type "%TOOL_ROOT%\.miniforge-base"
echo.
echo planning-tool env:
conda env list | findstr /i planning-tool
echo.
conda run -n planning-tool --no-capture-output python -c "import sys; print('[OK]', sys.executable)" 2>nul
if errorlevel 1 echo If failed, run Install-Miniforge.bat
pause
