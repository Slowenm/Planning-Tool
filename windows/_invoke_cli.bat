@echo off
setlocal EnableExtensions
rem Usage: call _invoke_cli.bat conda|venv [args...]
set "RUNTIME=%~1"
shift

if /i "%RUNTIME%"=="conda" (
  call "%~dp0_conda_activate_planning_tool.bat"
  if errorlevel 1 (
    echo [ERROR] activate planning-tool failed. Run Install-Offline.bat or Install-Conda.bat
    exit /b 1
  )
  set "PYTHONPATH=%CD%"
  python -m planning_tool.cli %*
  exit /b %ERRORLEVEL%
)

if /i "%RUNTIME%"=="venv" (
  call .venv\Scripts\activate.bat
  python -m planning_tool.cli %*
  exit /b %ERRORLEVEL%
)

echo [ERROR] unknown runtime: %RUNTIME%
exit /b 1
