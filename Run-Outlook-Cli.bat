@echo off
cd /d "%~dp0"
call "%~dp0windows\_tool_env.bat"
if "%~1"=="" (
  echo Drag your tasks.xlsx onto this file.
  pause
  exit /b 1
)
call "%~dp0windows\_bootstrap_conda_env.bat"
if errorlevel 1 (
  echo Run Install-Miniforge.bat or Save-Miniforge-Path.bat
  pause
  exit /b 1
)
call "%~dp0windows\_set_outlook_tz.bat"
python -m planning_tool.cli --tasks "%~1" --calendar outlook --report schedule.md --ics schedule.ics
if errorlevel 1 pause
exit /b %ERRORLEVEL%
