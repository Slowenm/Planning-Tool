@echo off
cd /d "%~dp0"
call "%~dp0windows\_conda_activate_planning_tool.bat"
if errorlevel 1 (
  echo Open Anaconda Prompt, run Install-Offline.bat first.
  pause
  exit /b 1
)
set "PYTHONPATH=%CD%"
echo Reading Outlook calendar — keep Outlook open...
python -m planning_tool.outlook_test --output outlook-calendar-test.md
set RC=%ERRORLEVEL%
echo.
if %RC%==0 echo Open outlook-calendar-test.md in this folder.
pause
exit /b %RC%
