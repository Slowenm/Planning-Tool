@echo off
cd /d "%~dp0"
set "TOOL_ROOT=%CD%"
call "%TOOL_ROOT%\windows\internal\_tool_env.bat"
call "%TOOL_ROOT%\windows\internal\_bootstrap_conda_env.bat"
if errorlevel 1 (
  echo 请先运行 Install-Miniforge.bat，或 setup\Save-Miniforge-Path.bat
  pause
  exit /b 1
)
call "%TOOL_ROOT%\windows\internal\_set_outlook_tz.bat"
python -m planning_tool.gui
pause
