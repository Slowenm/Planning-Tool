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
  echo [错误] 已选择 Conda 模式但未找到 conda。请用 Anaconda Prompt 运行 Install-Conda.bat
  exit /b 1
)
conda env list | findstr /i /b "planning-tool " >nul 2>nul
if errorlevel 1 (
  echo [错误] 未找到 conda 环境 planning-tool，请先运行 Install-Conda.bat
  exit /b 1
)
call "%~dp0_invoke_cli.bat" conda %*
exit /b %ERRORLEVEL%

:venv_run
if not exist .venv\Scripts\activate.bat (
  echo 首次使用，正在安装依赖（venv）...
  call "%~dp0install.bat"
  if errorlevel 1 exit /b 1
)
call "%~dp0_invoke_cli.bat" venv %*
exit /b %ERRORLEVEL%
