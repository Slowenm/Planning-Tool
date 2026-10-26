@echo off
setlocal EnableExtensions EnableDelayedExpansion
call "%~dp0_ensure_tool_root.bat"
cd /d "%TOOL_ROOT%"
call "%~dp0_prepend_conda_path.bat"
where conda >nul 2>nul
if errorlevel 1 (
  echo [错误] 找不到 Miniforge / conda。
  echo 请先安装 Miniforge: https://github.com/conda-forge/miniforge/releases
  echo 或在「Miniforge Prompt」中运行 setup\Save-Miniforge-Path.bat
  exit /b 1
)
call "%~dp0_find_conda_base.bat"
if not defined CONDA_BASE (
  for /f "delims=" %%G in ('conda info --base 2^>nul') do set "CONDA_BASE=%%G"
)
if not defined CONDA_BASE exit /b 1
echo !CONDA_BASE!> "%TOOL_ROOT%\.miniforge-base"
echo !CONDA_BASE!> "%TOOL_ROOT%\.conda-base"
echo 已保存 Miniforge 路径到 .miniforge-base :
type "%TOOL_ROOT%\.miniforge-base"
exit /b 0
