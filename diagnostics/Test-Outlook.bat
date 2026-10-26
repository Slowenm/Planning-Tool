@echo off
cd /d "%~dp0\.."
set "TOOL_ROOT=%CD%"
call "%TOOL_ROOT%\windows\internal\_set_outlook_tz.bat"
echo PLANNING_OUTLOOK_NAIVE_TZ=%PLANNING_OUTLOOK_NAIVE_TZ%
call "%TOOL_ROOT%\windows\internal\_conda_run.bat" python -m planning_tool.outlook_test --output "%TOOL_ROOT%\outlook-calendar-test.md"
set RC=%ERRORLEVEL%
if %RC%==0 echo 报告: %TOOL_ROOT%\outlook-calendar-test.md
pause
exit /b %RC%
