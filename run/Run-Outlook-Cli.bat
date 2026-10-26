@echo off
cd /d "%~dp0\.."
set "TOOL_ROOT=%CD%"
call "%TOOL_ROOT%\windows\internal\_tool_env.bat"
if "%~1"=="" (
  echo 把 tasks.xlsx 拖到此 bat 上
  pause
  exit /b 1
)
call "%TOOL_ROOT%\windows\internal\_bootstrap_conda_env.bat"
if errorlevel 1 (
  echo Install-Miniforge.bat 或 setup\Save-Miniforge-Path.bat
  pause
  exit /b 1
)
call "%TOOL_ROOT%\windows\internal\_set_outlook_tz.bat"
python -m planning_tool.cli --tasks "%~1" --calendar outlook --report schedule.md --ics schedule.ics
if errorlevel 1 pause
exit /b %ERRORLEVEL%
