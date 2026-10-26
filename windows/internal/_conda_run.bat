@echo off
rem Run python -m ... using planning-tool env ONLY (never PATH python.exe)
rem Usage: call _conda_run.bat python -m planning_tool.gui
setlocal EnableExtensions EnableDelayedExpansion
call "%~dp0_ensure_tool_root.bat"
call "%~dp0_prepend_conda_path.bat"
call "%~dp0_find_conda_base.bat"

if not defined CONDA_BASE (
  echo [ERROR] 找不到 Miniforge。请安装 Miniforge 或 setup\Save-Miniforge-Path.bat
  exit /b 1
)

set "ENV_PY=%CONDA_BASE%\envs\planning-tool\python.exe"
if not exist "!ENV_PY!" (
  echo [ERROR] 未找到: !ENV_PY!
  echo 请先双击 Install-Miniforge.bat 创建 planning-tool 环境
  exit /b 1
)

echo !ENV_PY! | findstr /i "Python38\\" >nul 2>&1
if not errorlevel 1 (
  echo [ERROR] 解析到的 Python 路径异常，请检查 .miniforge-base
  exit /b 1
)

if /i not "%~1"=="python" (
  echo [ERROR] 内部用法: _conda_run.bat python -m module ...
  exit /b 1
)
shift

set "PLANNING_TOOL_ROOT=%TOOL_ROOT%"
set "PYTHONPATH=%TOOL_ROOT%"
echo Using: !ENV_PY!
"!ENV_PY!" %*
set "RC=%ERRORLEVEL%"
endlocal & exit /b %RC%
