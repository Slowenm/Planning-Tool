@echo off
cd /d "%~dp0"
call "%~dp0windows\_tool_env.bat"
call "%~dp0windows\_bootstrap_conda_env.bat"
if errorlevel 1 (
  echo Run Install-Miniforge.bat first, or Save-Miniforge-Path.bat
  pause
  exit /b 1
)
call "%~dp0windows\_set_outlook_tz.bat"
python -m planning_tool.gui
pause
