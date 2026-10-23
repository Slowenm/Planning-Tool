@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."

where conda >nul 2>nul
if errorlevel 1 (
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
conda env list | findstr /i /b "planning-tool " >nul 2>nul
if errorlevel 1 (
  conda create -n planning-tool python=3.11 -y
  if errorlevel 1 exit /b 1
) else (
  echo 环境 planning-tool 已存在，跳过 create。
)

echo [2/3] 在 planning-tool 环境中安装本项目（含 pywin32 / Outlook COM）...
conda run -n planning-tool --no-capture-output python -m pip install -U pip setuptools wheel
conda run -n planning-tool --no-capture-output pip install -e ".[outlook]"
if errorlevel 1 (
  echo [错误] pip 安装失败。
  pause
  exit /b 1
)

echo conda> .env-mode
echo [3/3] 完成。已写入 .env-mode=conda
echo 之后请用 run-demo.bat / plan-work.bat / run-with-outlook.bat（会自动走 Conda）。
echo.
echo 也可在 Anaconda Prompt 中手动：
echo   conda activate planning-tool
echo   plan-work --tasks examples\tasks_template.csv --calendar none
pause
exit /b 0
