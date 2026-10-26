@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0\.."
set "TOOL_ROOT=%CD%"
where conda >nul 2>nul
if errorlevel 1 (
  echo Open from Miniforge Prompt.
  pause
  exit /b 1
)
for /f "delims=" %%G in ('conda info --base') do (
  echo %%G> "%TOOL_ROOT%\.miniforge-base"
  echo %%G> "%TOOL_ROOT%\.conda-base"
)
echo Saved:
type "%TOOL_ROOT%\.miniforge-base"
pause
