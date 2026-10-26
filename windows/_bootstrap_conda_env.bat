@echo off
rem Prepend Miniforge to PATH (.miniforge-base) then activate planning-tool
setlocal EnableExtensions EnableDelayedExpansion
call "%~dp0_prepend_conda_path.bat"
call "%~dp0_conda_activate_planning_tool.bat" %*
set "RC=%ERRORLEVEL%"
endlocal & exit /b %RC%
