@echo off
cd /d "%~dp0\.."
set "TOOL_ROOT=%CD%"
echo TOOL_ROOT=%TOOL_ROOT%
echo.
echo --- conda / env ---
where conda 2>nul
conda env list 2>nul | findstr /i planning-tool
echo.
echo --- python via conda run planning-tool ---
call "%TOOL_ROOT%\windows\internal\_conda_run.bat" python -c "import sys; print(sys.executable); print(sys.version)"
call "%TOOL_ROOT%\windows\internal\_conda_run.bat" python -c "import planning_tool.cli; print('import OK')"
call "%TOOL_ROOT%\windows\internal\_conda_run.bat" python -m planning_tool.cli --help
pause
