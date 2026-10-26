@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0\.."
call "%~dp0_prepend_conda_path.bat"
where conda >nul 2>nul
if errorlevel 1 (
  echo [错误] 找不到 Miniforge / conda。
  echo 请先安装 Miniforge: https://github.com/conda-forge/miniforge
  echo 或在「Miniforge Prompt」中运行本脚本。
  exit /b 1
)
call "%~dp0_find_conda_base.bat"
if not defined CONDA_BASE (
  for /f "delims=" %%G in ('conda info --base 2^>nul') do set "CONDA_BASE=%%G"
)
if not defined CONDA_BASE exit /b 1
echo !CONDA_BASE!> "%CD%\.miniforge-base"
echo !CONDA_BASE!> "%CD%\.conda-base"
echo 已保存 Miniforge 路径到 .miniforge-base :
type "%CD%\.miniforge-base"
exit /b 0
