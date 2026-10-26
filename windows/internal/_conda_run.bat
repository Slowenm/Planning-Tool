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

set "PLANNING_TOOL_ROOT=%TOOL_ROOT%"
set "PYTHONPATH=%TOOL_ROOT%"

set "ENV_PY="
if defined CONDA_BASE set "ENV_PY=!CONDA_BASE!\envs\planning-tool\python.exe"
if defined ENV_PY if exist "!ENV_PY!" goto :run_direct

rem Fallback: env may live under another Miniforge; use conda run
where conda >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Miniforge not found and planning-tool python missing.
  echo Expected: %CONDA_BASE%\envs\planning-tool\python.exe
  echo.
  echo Open "Miniforge Prompt", cd to tool folder, run:
  echo   Fix-Miniforge-Path.bat
  echo   Install-Miniforge.bat
  exit /b 1
)

conda env list | findstr /i /b "planning-tool " >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Conda env "planning-tool" not found. Run Install-Miniforge.bat
  conda env list
  exit /b 1
)

echo Using: conda run -n planning-tool python ...
conda run -n planning-tool --no-capture-output python %*
set "RC=%ERRORLEVEL%"
endlocal & exit /b %RC%

:run_direct
echo Using: !ENV_PY!
"!ENV_PY!" %*
set "RC=%ERRORLEVEL%"
endlocal & exit /b %RC%
