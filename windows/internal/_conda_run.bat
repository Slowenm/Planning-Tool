@echo off
rem Run a command inside conda env planning-tool (avoids wrong python on PATH)
rem Usage: call _conda_run.bat python -m planning_tool.cli --help
setlocal EnableExtensions EnableDelayedExpansion
call "%~dp0_ensure_tool_root.bat"
call "%~dp0_prepend_conda_path.bat"

where conda >nul 2>nul
if errorlevel 1 (
  echo [ERROR] 找不到 Miniforge / conda。请安装 Miniforge 或运行 setup\Save-Miniforge-Path.bat
  exit /b 1
)

conda env list | findstr /i /b "planning-tool " >nul 2>nul
if errorlevel 1 (
  echo [ERROR] 未找到 conda 环境 planning-tool。请先双击 Install-Miniforge.bat
  exit /b 1
)

set "PLANNING_TOOL_ROOT=%TOOL_ROOT%"
set "PYTHONPATH=%TOOL_ROOT%"
conda run -n planning-tool --no-capture-output %*
set "RC=%ERRORLEVEL%"
endlocal & exit /b %RC%
