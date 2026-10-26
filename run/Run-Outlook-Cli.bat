@echo off
cd /d "%~dp0\.."
set "TOOL_ROOT=%CD%"
if "%~1"=="" (
  echo 把 tasks.xlsx 拖到此 bat 上
  pause
  exit /b 1
)
call "%TOOL_ROOT%\windows\internal\_set_outlook_tz.bat"
call "%TOOL_ROOT%\windows\internal\_conda_run.bat" python -m planning_tool.cli --tasks "%~1" --calendar outlook --report schedule.md --ics schedule.ics
if errorlevel 1 pause
exit /b %ERRORLEVEL%
