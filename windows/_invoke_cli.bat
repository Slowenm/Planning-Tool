@echo off
setlocal EnableExtensions
rem Usage: call _invoke_cli.bat conda|venv [args...]
set "RUNTIME=%~1"
shift

set "ROOT=%CD%"
if exist "%ROOT%\planning_tool\cli.py" goto :root_ok
if exist "%ROOT%\..\planning_tool\cli.py" set "ROOT=%ROOT%\.." & cd /d "%ROOT%"
:root_ok

set "ACT=%~dp0_conda_activate_planning_tool.bat"
if not exist "%ACT%" set "ACT=%ROOT%\windows\_conda_activate_planning_tool.bat"

if /i "%RUNTIME%"=="conda" (
  if not exist "%ACT%" (
    echo [ERROR] missing _conda_activate_planning_tool.bat
    exit /b 1
  )
  call "%ACT%"
  if errorlevel 1 (
    echo [ERROR] activate planning-tool failed. Run Install-Offline.bat
    exit /b 1
  )
  set "PLANNING_TOOL_ROOT=%ROOT%"
  set "PYTHONPATH=%ROOT%"
  call "%~dp0_set_outlook_tz.bat"
  python -m planning_tool.cli %*
  exit /b %ERRORLEVEL%
)

if /i "%RUNTIME%"=="venv" (
  call "%ROOT%\.venv\Scripts\activate.bat"
  python -m planning_tool.cli %*
  exit /b %ERRORLEVEL%
)

echo [ERROR] unknown runtime: %RUNTIME%
exit /b 1
