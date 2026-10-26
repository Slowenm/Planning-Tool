@echo off
cd /d "%~dp0"
call "%~dp0windows\_tool_env.bat"
call "%~dp0windows\_bootstrap_conda_env.bat"
if errorlevel 1 (
  echo Install Miniforge, then run Install-Miniforge.bat
  pause
  exit /b 1
)
call "%~dp0windows\_set_outlook_tz.bat"
echo Reading Outlook (PLANNING_OUTLOOK_NAIVE_TZ=%PLANNING_OUTLOOK_NAIVE_TZ%) — keep Outlook open...
python -m planning_tool.outlook_test --output outlook-calendar-test.md
set RC=%ERRORLEVEL%
echo.
if %RC%==0 echo Open outlook-calendar-test.md in this folder.
pause
exit /b %RC%
