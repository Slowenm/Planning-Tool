@echo off
cd /d "%~dp0"
set "TOOL_ROOT=%CD%"
call "%TOOL_ROOT%\windows\internal\_set_outlook_tz.bat"
call "%TOOL_ROOT%\windows\internal\_conda_run.bat" python -m planning_tool.gui
set RC=%ERRORLEVEL%
if %RC% neq 0 (
  echo.
  echo 若提示 ModuleNotFoundError: 请先 Install-Miniforge.bat
  echo 若 python 路径像公司 Python3.8: 必须用 Miniforge 环境，勿改系统 PATH 里的 python
)
pause
exit /b %RC%
