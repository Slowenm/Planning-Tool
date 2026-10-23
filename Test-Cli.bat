@echo off
cd /d "%~dp0"
call windows\_tool_env.bat
call windows\_conda_activate_planning_tool.bat
if errorlevel 1 (
  echo Activate failed. Use Anaconda Prompt.
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
