@echo off
cd /d "%~dp0"
if "%~1"=="" (
  echo Drag your tasks.xlsx onto this file.
  pause
  exit /b 1
)
call "%~dp0windows\_conda_activate_planning_tool.bat"
if errorlevel 1 (
  echo Run from Anaconda Prompt after Install-Offline.bat
  pause
  exit /b 1
)
set "PYTHONPATH=%CD%"
call "%~dp0windows\_set_outlook_tz.bat"
python -m planning_tool.cli --tasks "%~1" --calendar outlook --report schedule.md --ics schedule.ics
if errorlevel 1 pause
exit /b %ERRORLEVEL%
