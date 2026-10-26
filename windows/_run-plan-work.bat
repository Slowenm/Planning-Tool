@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0\.."
call "%~dp0_prepend_conda_path.bat"

where conda >nul 2>nul
if errorlevel 1 (
  echo [ERROR] 找不到 Miniforge。请安装 Miniforge 后运行 Install-Miniforge.bat
  echo 或双击 Save-Miniforge-Path.bat
  exit /b 1
)

conda env list | findstr /i /b "planning-tool " >nul 2>nul
if errorlevel 1 (
  echo [ERROR] 未找到 conda 环境 planning-tool。请先运行 Install-Miniforge.bat
  exit /b 1
)

call "%~dp0_invoke_cli.bat" conda %*
exit /b %ERRORLEVEL%
