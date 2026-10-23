@echo off
title Planning-Tool Repair (Conda pip only)
cd /d "%~dp0"
echo 仅重新执行 pip install -e （不删除 planning-tool 环境）
echo 目录: %CD%
echo.
where conda >nul 2>nul
if errorlevel 1 (
  echo [错误] 找不到 conda，请在本窗口先运行 Anaconda 的 activate 或使用 Anaconda Prompt
  pause
  exit /b 1
)
call "%~dp0windows\install-conda.bat" --from-wrapper
pause
