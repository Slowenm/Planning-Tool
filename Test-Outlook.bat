@echo off
cd /d "%~dp0"
call "%~dp0windows\_conda_activate_planning_tool.bat"
if errorlevel 1 (
  echo Open Anaconda Prompt, run Install-Offline.bat first.
  pause
  exit /b 1
)
set "PYTHONPATH=%CD%"
call "%~dp0windows\_set_outlook_tz.bat"
echo Reading Outlook (PLANNING_OUTLOOK_NAIVE_TZ=%PLANNING_OUTLOOK_NAIVE_TZ%) — keep Outlook open...
python -m planning_tool.outlook_test --output outlook-calendar-test.md
set RC=%ERRORLEVEL%
echo.
if %RC%==0 echo Open outlook-calendar-test.md in this folder.
pause
exit /b %RC%
