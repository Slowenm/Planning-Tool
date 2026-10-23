@echo off
rem Call after: cd /d "%~dp0"  (tool root)  OR  cd /d "%~dp0\.."  (from windows\)
set "PLANNING_TOOL_ROOT=%CD%"
set "PYTHONPATH=%CD%"
exit /b 0
