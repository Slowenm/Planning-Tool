@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."

set "WHEELS=%CD%\offline\wheels"
set "LOG=%CD%\install-last.log"
echo === install-offline %DATE% %TIME% ===>> "%LOG%"

if not exist "%WHEELS%\*.whl" (
  echo [ERROR] Missing offline\wheels\*.whl — use the ~9MB zip.
  pause
  exit /b 1
)

where conda >nul 2>nul
if errorlevel 1 (
  echo [ERROR] conda not found. Open Miniforge / Miniconda / Anaconda Prompt.
  pause
  exit /b 1
)

conda env list | findstr /i /b "planning-tool " >nul 2>nul
if errorlevel 1 (
  echo [1/5] Creating conda env planning-tool ...
  conda create -n planning-tool python=3.11 -y
  if errorlevel 1 (
    echo [ERROR] conda create failed.
    pause
    exit /b 1
  )
) else (
  echo [1/5] Using existing env planning-tool
)

echo [2/5] Activating planning-tool ...
call "%~dp0_conda_activate_planning_tool.bat"
if errorlevel 1 (
  echo [ERROR] Could not activate planning-tool.
  pause
  exit /b 1
)

echo Using Python:
where python
python --version

echo [3/5] Offline pip: setuptools, wheel ...
python -m pip install --no-index --find-links "%WHEELS%" setuptools wheel
if errorlevel 1 goto :pip_fail

echo [4/5] Offline pip: openpyxl, icalendar, tzdata, pywin32 ...
python -m pip install --no-index --find-links "%WHEELS%" openpyxl icalendar tzdata pywin32
if errorlevel 1 goto :pip_fail

echo [5/5] Register this project (offline, non-editable — 整包移动后请在本目录重跑安装) ...
call "%~dp0_tool_env.bat"
python -m pip install --no-build-isolation --no-index --find-links "%WHEELS%" ".[outlook]"
set "PIP_PROJ=%ERRORLEVEL%"

echo conda> .env-mode
echo offline>> .env-mode
echo system> "%CD%\.outlook-tz"

echo Verify import (from this folder) ...
python -c "import planning_tool.cli; print('import OK')"
if errorlevel 1 (
  echo [ERROR] planning_tool not importable from %CD%. Details:
  python -c "import planning_tool.cli"
  pause
  exit /b 1
)

if not "%PIP_PROJ%"=="0" (
  echo [WARN] pip install returned %PIP_PROJ% but import works; continuing.
)

for /f "delims=" %%G in ('conda info --base 2^>nul') do echo %%G> "%CD%\.conda-base"

echo.
echo [OK] Offline install done. Next: Run-Demo.bat
if /i not "%~1"=="--from-wrapper" pause
exit /b 0

:pip_fail
echo [ERROR] pip failed. Log: %LOG%
pause
exit /b 1
