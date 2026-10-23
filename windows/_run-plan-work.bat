@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0\.."
call "%~dp0_prepend_conda_path.bat"

set "USE_CONDA=0"
set "MODE="

where conda >nul 2>nul
if not errorlevel 1 (
  conda env list | findstr /i /b "planning-tool " >nul 2>nul
  if not errorlevel 1 set "USE_CONDA=1"
)

if "%USE_CONDA%"=="0" if exist ".env-mode" (
  set /p MODE=<.env-mode
)
if "%USE_CONDA%"=="0" if /i "%MODE%"=="conda" set "USE_CONDA=1"

if "%USE_CONDA%"=="1" goto :conda_run

if exist ".venv\Scripts\activate.bat" goto :venv_run

echo [ERROR] No conda env "planning-tool" and no .venv.
echo Run Install-Offline.bat first (recommended on company PC).
exit /b 1

:conda_run
call "%~dp0_invoke_cli.bat" conda %*
exit /b %ERRORLEVEL%

:venv_run
call "%~dp0_invoke_cli.bat" venv %*
exit /b %ERRORLEVEL%
