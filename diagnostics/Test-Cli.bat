@echo off
cd /d "%~dp0\.."
set "TOOL_ROOT=%CD%"
call "%TOOL_ROOT%\windows\internal\_tool_env.bat"
call "%TOOL_ROOT%\windows\internal\_bootstrap_conda_env.bat"
if errorlevel 1 (
  echo 失败: Install-Miniforge.bat 或 setup\Save-Miniforge-Path.bat
  pause
  exit /b 1
)
where python
python --version
python -c "import planning_tool.cli; print('import OK')"
python -m planning_tool.cli --help
pause
