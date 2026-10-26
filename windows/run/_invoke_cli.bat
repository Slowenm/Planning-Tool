@echo off
setlocal EnableExtensions
rem Usage: call _invoke_cli.bat conda [args...]
set "RUNTIME=%~1"
shift

call "%~dp0..\internal\_ensure_tool_root.bat"
cd /d "%TOOL_ROOT%"

if /i not "%RUNTIME%"=="conda" (
  echo [ERROR] 仅支持 Miniforge conda 运行。
  exit /b 1
)

call "%~dp0..\internal\_conda_activate_planning_tool.bat"
if errorlevel 1 (
  echo [ERROR] activate planning-tool failed. Run Install-Miniforge.bat
  exit /b 1
)
set "PLANNING_TOOL_ROOT=%TOOL_ROOT%"
set "PYTHONPATH=%TOOL_ROOT%"
call "%~dp0..\internal\_set_outlook_tz.bat"
python -m planning_tool.cli %*
exit /b %ERRORLEVEL%
