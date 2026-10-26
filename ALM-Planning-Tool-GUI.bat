@echo off
cd /d "%~dp0"
set "TOOL_ROOT=%CD%"
call "%TOOL_ROOT%\windows\internal\_set_outlook_tz.bat"
call "%TOOL_ROOT%\windows\internal\_conda_run.bat" python -m alm_planning_tool.gui
set RC=%ERRORLEVEL%
if %RC% neq 0 (
  echo 请先 Install-Miniforge.bat 或 setup\Save-Miniforge-Path.bat
)
pause
exit /b %RC%
