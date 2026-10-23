@echo off
setlocal EnableExtensions
rem Usage: call _invoke_cli.bat conda|venv [args...]
set "RUNTIME=%~1"
shift

if /i "%RUNTIME%"=="conda" (
  rem 离线安装或未 editable 时，保证能 import 本项目
  conda run -n planning-tool -e "PYTHONPATH=%CD%" --no-capture-output python -m planning_tool.cli %*
  exit /b %ERRORLEVEL%
)

if /i "%RUNTIME%"=="venv" (
  call .venv\Scripts\activate.bat
  python -m planning_tool.cli %*
  exit /b %ERRORLEVEL%
)

echo [错误] 未知运行时: %RUNTIME%
exit /b 1
