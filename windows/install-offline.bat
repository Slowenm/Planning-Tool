@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."

set "WHEELS=%CD%\offline\wheels"
set "LOG=%CD%\install-last.log"
echo === install-offline %DATE% %TIME% ===>> "%LOG%"

if not exist "%WHEELS%\*.whl" (
  echo [错误] 未找到 offline\wheels\*.whl
  echo 请使用带 offline 依赖的完整包（Release 里的 -offline-full 或含 wheels 的 zip）
  pause
  exit /b 1
)

where conda >nul 2>nul
if errorlevel 1 (
  echo [错误] 需要 Anaconda Prompt（找不到 conda）
  pause
  exit /b 1
)

conda env list | findstr /i /b "planning-tool " >nul 2>nul
if errorlevel 1 (
  echo [1/4] 创建 conda 环境 planning-tool ...
  conda create -n planning-tool python=3.11 -y
  if errorlevel 1 pause & exit /b 1
) else (
  echo [1/4] 使用已有环境 planning-tool
)

echo [2/4] 离线安装 setuptools / wheel ...
conda run -n planning-tool --no-capture-output python -m pip install --no-index --find-links "%WHEELS%" setuptools wheel
if errorlevel 1 pause & exit /b 1

echo [3/4] 离线安装 openpyxl / icalendar / tzdata / pywin32 ...
conda run -n planning-tool --no-capture-output python -m pip install --no-index --find-links "%WHEELS%" openpyxl icalendar tzdata pywin32
if errorlevel 1 (
  echo [错误] 依赖安装失败，请确认 wheels 与 Python 3.11 win64 匹配
  pause
  exit /b 1
)

echo [4/4] 注册本项目（无需联网）...
conda run -n planning-tool --no-capture-output python -m pip install --no-build-isolation --no-index --find-links "%WHEELS%" -e ".[outlook]"
if errorlevel 1 (
  echo [--] editable 安装失败，改用 PYTHONPATH 模式...
  echo conda> .env-mode
  echo offline>> .env-mode
  goto :verify
)
echo conda> .env-mode
echo offline>> .env-mode

:verify
conda run -n planning-tool -e "PYTHONPATH=%CD%" --no-capture-output python -m planning_tool.cli --help >nul 2>&1
if errorlevel 1 (
  echo [错误] 仍无法运行 planning_tool.cli
  pause
  exit /b 1
)

echo [完成] 离线安装成功。请双击 Run-Demo.bat
if /i not "%~1"=="--from-wrapper" pause
exit /b 0
