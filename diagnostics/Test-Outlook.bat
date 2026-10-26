@echo off
cd /d "%~dp0\.."
set "TOOL_ROOT=%CD%"
call "%TOOL_ROOT%\windows\internal\_tool_env.bat"
call "%TOOL_ROOT%\windows\internal\_bootstrap_conda_env.bat"
if errorlevel 1 (
  echo Install-Miniforge.bat first.
  pause
  exit /b 1
)
call "%TOOL_ROOT%\windows\internal\_set_outlook_tz.bat"
echo PLANNING_OUTLOOK_NAIVE_TZ=%PLANNING_OUTLOOK_NAIVE_TZ%
python -m planning_tool.outlook_test --output "%TOOL_ROOT%\outlook-calendar-test.md"
set RC=%ERRORLEVEL%
if %RC%==0 echo 报告: %TOOL_ROOT%\outlook-calendar-test.md
pause
exit /b %RC%
