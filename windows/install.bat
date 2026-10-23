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
  if errorlevel 1 (
    echo [错误] 创建 .venv 失败。
    pause
    exit /b 1
  )
)

echo [2/3] 安装依赖（含 Outlook COM / pywin32）...
call .venv\Scripts\activate.bat
set "PIP_INDEX=--index-url https://pypi.org/simple"
python -m pip install -U pip setuptools wheel %PIP_INDEX%
call "%~dp0_tool_env.bat"
pip install ".[outlook]" %PIP_INDEX%
if errorlevel 1 (
  echo [错误] 安装失败。
  pause
  exit /b 1
)

echo venv> .env-mode
echo [3/3] 完成（.env-mode=venv）。可双击 run-demo.bat 试跑，或用 plan-work.bat 排期。
echo 若你平时用 Anaconda，请改用 windows\install-conda.bat。
pause
exit /b 0
