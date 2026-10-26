@echo off
rem Online install via Miniforge (use install-offline.bat when PyPI is blocked)
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0\.."
call "%~dp0_prepend_conda_path.bat"

set "LOG=%CD%\install-last.log"
echo === Planning-Tool install-miniforge-online %DATE% %TIME% ===>> "%LOG%"

where conda >nul 2>nul
if errorlevel 1 (
  echo [错误] 找不到 Miniforge / conda。
  echo 请安装 Miniforge 或在 Miniforge Prompt 中运行 Install-Miniforge.bat
  pause
  exit /b 1
)

echo [1/3] 创建/更新 Miniforge 环境 planning-tool（Python 3.11）...
conda env list | findstr /i /b "planning-tool " >nul 2>nul
if errorlevel 1 (
  conda create -n planning-tool python=3.11 -y
  if errorlevel 1 (
    echo [错误] conda create 失败。
    pause
    exit /b 1
  )
)

echo [2/3] pip 安装（需能访问 pypi.org）...
set "PIP_INDEX=--index-url https://pypi.org/simple"
conda run -n planning-tool --no-capture-output python -m pip install -U pip setuptools wheel %PIP_INDEX%
call "%~dp0_tool_env.bat"
conda run -n planning-tool --no-capture-output pip install ".[outlook]" %PIP_INDEX%
if errorlevel 1 (
  echo [错误] pip 失败。内网请改用 Install-Miniforge.bat（离线 wheels）
  pause
  exit /b 1
)

echo [3/3] 验证...
set "PLANNING_TOOL_ROOT=%CD%"
set "PYTHONPATH=%CD%"
conda run -n planning-tool --no-capture-output python -m planning_tool.cli --help >nul 2>&1
if errorlevel 1 (
  echo [错误] 安装后无法运行 planning_tool.cli
  pause
  exit /b 1
)

echo miniforge> .env-mode
echo online>> .env-mode
call "%~dp0_find_conda_base.bat"
if defined CONDA_BASE (
  echo !CONDA_BASE!> "%CD%\.miniforge-base"
  echo !CONDA_BASE!> "%CD%\.conda-base"
)
echo [OK] 完成。下一步 Run-Demo.bat 或 Planning-Tool-GUI.bat
if /i not "%~1"=="--from-wrapper" pause
exit /b 0
