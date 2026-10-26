@echo off
chcp 65001 >nul 2>&1
setlocal EnableExtensions EnableDelayedExpansion
call "%~dp0_ensure_tool_root.bat"
call "%~dp0_prepend_conda_path.bat"
call "%~dp0_find_conda_base.bat"

if /i not "%~1"=="python" (
  echo [ERROR] Internal: _conda_run.bat python -m module ...
  exit /b 1
)
shift
rem NOTE: after shift, %%* may still include "python" on Windows — use %%1..%%9

set "PLANNING_TOOL_ROOT=%TOOL_ROOT%"
set "PYTHONPATH=%TOOL_ROOT%"

set "ENV_PY="
if defined CONDA_BASE set "ENV_PY=!CONDA_BASE!\envs\planning-tool\python.exe"
if defined ENV_PY if exist "!ENV_PY!" goto :run_direct

where conda >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Miniforge not found and planning-tool python missing.
  echo Run Fix-Miniforge-Path.bat and Install-Miniforge.bat from Miniforge Prompt.
  exit /b 1
)

conda env list | findstr /i /b "planning-tool " >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Conda env "planning-tool" not found. Run Install-Miniforge.bat
  conda env list
  exit /b 1
)

echo Using: conda run -n planning-tool python %1 %2 %3 %4 %5 %6 %7 %8 %9
conda run -n planning-tool --no-capture-output python %1 %2 %3 %4 %5 %6 %7 %8 %9
set "RC=%ERRORLEVEL%"
endlocal & exit /b %RC%

:run_direct
echo Using: !ENV_PY!
"!ENV_PY!" %1 %2 %3 %4 %5 %6 %7 %8 %9
set "RC=%ERRORLEVEL%"
endlocal & exit /b %RC%
