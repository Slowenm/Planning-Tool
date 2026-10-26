@echo off
rem Run python -m ... using planning-tool env ONLY (never PATH python.exe)
chcp 65001 >nul 2>&1
setlocal EnableExtensions EnableDelayedExpansion
call "%~dp0_ensure_tool_root.bat"
call "%~dp0_prepend_conda_path.bat"
call "%~dp0_find_conda_base.bat"

if not defined CONDA_BASE (
  echo [ERROR] Miniforge / conda not found.
  echo Install Miniforge, then run Install-Miniforge.bat from "Miniforge Prompt"
  echo Or run setup\Save-Miniforge-Path.bat after opening Miniforge Prompt.
  exit /b 1
)

set "ENV_PY=%CONDA_BASE%\envs\planning-tool\python.exe"
if not exist "!ENV_PY!" (
  echo [ERROR] Conda env "planning-tool" is not installed.
  echo Expected: !ENV_PY!
  echo.
  echo CONDA_BASE=!CONDA_BASE!
  where conda 2>nul
  echo.
  echo Environments named planning-tool:
  conda env list 2>nul | findstr /i planning-tool
  echo.
  echo Fix ^(required once per PC^):
  echo   1. Start menu - open "Miniforge Prompt"
  echo   2. cd /d "!TOOL_ROOT!"
  echo   3. Install-Miniforge.bat
  echo.
  echo If Miniforge is not under Program Files, delete .miniforge-base in the tool
  echo folder and run setup\Save-Miniforge-Path.bat from Miniforge Prompt.
  exit /b 1
)

if /i not "%~1"=="python" (
  echo [ERROR] Internal: _conda_run.bat python -m module ...
  exit /b 1
)
shift

set "PLANNING_TOOL_ROOT=%TOOL_ROOT%"
set "PYTHONPATH=%TOOL_ROOT%"
echo Using: !ENV_PY!
"!ENV_PY!" %*
set "RC=%ERRORLEVEL%"
endlocal & exit /b %RC%
