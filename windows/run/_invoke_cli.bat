@echo off
setlocal EnableExtensions
rem Usage: call _invoke_cli.bat conda [args for planning_tool.cli...]
set "RUNTIME=%~1"
shift

if /i not "%RUNTIME%"=="conda" (
  echo [ERROR] 仅支持 Miniforge conda 运行。
  exit /b 1
)

call "%~dp0..\internal\_ensure_tool_root.bat"
call "%~dp0..\internal\_set_outlook_tz.bat"
call "%~dp0..\internal\_conda_run.bat" python -m planning_tool.cli %*
exit /b %ERRORLEVEL%
