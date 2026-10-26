@echo off
setlocal EnableExtensions EnableDelayedExpansion
call "%~dp0..\internal\_ensure_tool_root.bat"
cd /d "%TOOL_ROOT%"
call "%~dp0..\internal\_prepend_conda_path.bat"

where conda >nul 2>nul
if errorlevel 1 (
  echo [ERROR] 找不到 Miniforge。请运行 Install-Miniforge.bat
  echo 或 setup\Save-Miniforge-Path.bat
  exit /b 1
)

conda env list | findstr /i /b "planning-tool " >nul 2>nul
if errorlevel 1 (
  echo [ERROR] 未找到环境 planning-tool。请先 Install-Miniforge.bat
  exit /b 1
)

call "%~dp0_invoke_cli.bat" conda %*
exit /b %ERRORLEVEL%
