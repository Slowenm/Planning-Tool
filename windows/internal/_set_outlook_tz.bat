@echo off
call "%~dp0_ensure_tool_root.bat"
set "PLANNING_OUTLOOK_NAIVE_TZ=system"
if exist "%TOOL_ROOT%\.outlook-tz" (
  set /p PLANNING_OUTLOOK_NAIVE_TZ=<"%TOOL_ROOT%\.outlook-tz"
)
exit /b 0
