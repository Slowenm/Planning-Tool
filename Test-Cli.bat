@echo off
cd /d "%~dp0"
call windows\_tool_env.bat
call windows\_bootstrap_conda_env.bat
if errorlevel 1 (
  echo Failed. Run Install-Miniforge.bat or Save-Miniforge-Path.bat
  pause
  exit /b 1
)
echo Python:
where python
python --version
echo.
python -c "import planning_tool.cli; print('import OK')"
python -m planning_tool.cli --help
echo.
echo If you see help text above, run Run-Demo.bat
pause
