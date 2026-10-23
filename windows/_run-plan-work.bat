@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."

set "MODE=venv"
if exist ".env-mode" (
  set /p MODE=<.env-mode
)

if /i "%MODE%"=="conda" goto :conda_run
goto :venv_run

:conda_run
where conda >nul 2>nul
if errorlevel 1 (
  echo [错误] 已选择 Conda 模式但未找到 conda 命令。请打开 "Anaconda Prompt" 运行 install-conda.bat
  exit /b 1
)
conda env list | findstr /i /b "planning-tool " >nul 2>nul
if errorlevel 1 (
  echo [错误] 未找到 conda 环境 planning-tool，请先双击 install-conda.bat
  exit /b 1
)
conda run -n planning-tool --no-capture-output plan-work %*
exit /b %ERRORLEVEL%

:venv_run
if not exist .venv\Scripts\activate.bat (
  echo 首次使用，正在安装依赖（venv）...
  call "%~dp0install.bat"
  if errorlevel 1 exit /b 1
)
call .venv\Scripts\activate.bat
plan-work %*
exit /b %ERRORLEVEL%
