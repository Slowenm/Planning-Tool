@echo off
rem Sets TOOL_ROOT to portable package root (folder with planning_tool\ and pyproject.toml)
if defined TOOL_ROOT if exist "%TOOL_ROOT%\planning_tool\cli.py" exit /b 0
cd /d "%~dp0..\.."
set "TOOL_ROOT=%CD%"
exit /b 0
