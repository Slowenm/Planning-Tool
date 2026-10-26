@echo off
setlocal EnableExtensions EnableDelayedExpansion
call "%~dp0_ensure_tool_root.bat"
call "%~dp0_prepend_conda_path.bat"
call "%~dp0_conda_activate_planning_tool.bat" %*
set "RC=%ERRORLEVEL%"
endlocal & exit /b %RC%
