@echo off
cd /d "%~dp0"
call "%~dp0windows\_conda_activate_planning_tool.bat"
if errorlevel 1 (
  echo Run Install-Offline.bat from Anaconda Prompt first.
  pause
  exit /b 1
)
set "PYTHONPATH=%CD%"
call "%~dp0windows\_set_outlook_tz.bat"
python -m planning_tool.gui
pause
