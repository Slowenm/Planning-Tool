@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."

where python >nul 2>nul
if errorlevel 1 (
  echo [错误] 未找到 Python。请先安装 Python 3.10 或更高版本：https://www.python.org/downloads/
  echo 安装时勾选 "Add python.exe to PATH"。
  pause
  exit /b 1
)

echo [1/3] 创建虚拟环境 .venv ...
if not exist .venv\Scripts\python.exe (
  python -m venv .venv
  if errorlevel 1 exit /b 1
)

echo [2/3] 安装依赖（含 Outlook COM / pywin32）...
call .venv\Scripts\activate.bat
python -m pip install -U pip setuptools wheel
pip install -e ".[outlook]"
if errorlevel 1 (
  echo [错误] 安装失败。
  pause
  exit /b 1
)

echo [3/3] 完成。可双击 run-demo.bat 试跑，或用 plan-work.bat 排期。
pause
exit /b 0
