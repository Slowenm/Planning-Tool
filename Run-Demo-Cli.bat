@echo off
cd /d "%~dp0"
call "%~dp0windows\_conda_activate_planning_tool.bat"
if errorlevel 1 (
  echo Run from Anaconda Prompt after Install-Offline.bat
  pause
  exit /b 1
)
set "PYTHONPATH=%CD%"
python -m planning_tool.cli --tasks examples\tasks_template.csv --calendar none --report schedule.md --ics schedule.ics
if errorlevel 1 pause
exit /b %ERRORLEVEL%
