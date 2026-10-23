@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."

set "LOG=%CD%\install-last.log"
echo === Planning-Tool install-conda %DATE% %TIME% ===>> "%LOG%"
echo 日志同时写入: %LOG%

where conda >nul 2>nul
if errorlevel 1 (
  echo [错误] 当前窗口找不到 conda。>> "%LOG%"
  echo [错误] 当前窗口找不到 conda。
  echo 请从开始菜单打开 **Anaconda Prompt** 或 **Miniconda Prompt**，
  echo 然后在该窗口执行：
  echo   cd /d "%CD%"
  echo   windows\install-conda.bat
  echo 或直接双击解压目录下的 Install-Conda.bat
  pause
  exit /b 1
)

echo [1/3] 创建/更新 Conda 环境 planning-tool（Python 3.11）...
echo [1/3] conda env...>> "%LOG%"
conda env list | findstr /i /b "planning-tool " >nul 2>nul
if errorlevel 1 (
  conda create -n planning-tool python=3.11 -y
  if errorlevel 1 (
    echo [错误] conda create 失败。>> "%LOG%"
    echo [错误] conda create 失败。
    pause
    exit /b 1
  )
) else (
  echo 环境 planning-tool 已存在，跳过 create。
)

echo [2/3] 在 planning-tool 环境中安装本项目（含 pywin32 / Outlook COM）...
echo [2/3] pip install...>> "%LOG%"
set "PIP_INDEX=--index-url https://pypi.org/simple"
conda run -n planning-tool --no-capture-output python -m pip install -U pip setuptools wheel %PIP_INDEX%
if errorlevel 1 (
  echo [错误] pip 升级失败。>> "%LOG%"
  echo [错误] pip 升级失败。
  pause
  exit /b 1
)
conda run -n planning-tool --no-capture-output pip install -e ".[outlook]" %PIP_INDEX%
if errorlevel 1 (
  echo [错误] pip 安装失败。>> "%LOG%"
  echo [错误] pip 安装失败。
  pause
  exit /b 1
)

echo [3/3] 验证 python -m planning_tool.cli ...
conda run -n planning-tool --no-capture-output python -m planning_tool.cli --help >nul 2>&1
if errorlevel 1 (
  echo [错误] 安装后仍无法运行 planning_tool.cli，请把 install-last.log 发给维护者。>> "%LOG%"
  echo [错误] 安装后仍无法运行 planning_tool.cli
  pause
  exit /b 1
)

echo conda> .env-mode
echo [3/3] 完成。已写入 .env-mode=conda>> "%LOG%"
echo [3/3] 完成。已写入 .env-mode=conda
echo 下一步: 双击 Run-Demo.bat 试跑
echo 之后可用 Run-With-Outlook.bat 读 Outlook 并排期
echo.
echo 也可在 Anaconda Prompt 中手动：
echo   conda activate planning-tool
echo   python -m planning_tool.cli --tasks examples\tasks_template.csv --calendar none
if /i not "%~1"=="--from-wrapper" pause
exit /b 0
