@echo off
call "%~dp0_ensure_tool_root.bat"
set "PLANNING_TOOL_ROOT=%TOOL_ROOT%"
set "PYTHONPATH=%TOOL_ROOT%"
cd /d "%TOOL_ROOT%"
exit /b 0
