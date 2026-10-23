@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."

set "WHEELS=%CD%\offline\wheels"
set "LOG=%CD%\install-last.log"
echo === install-offline %DATE% %TIME% ===>> "%LOG%"

if not exist "%WHEELS%\*.whl" (
  echo [ERROR] Missing offline\wheels\*.whl — use the ~9MB v0.1.6+ zip.
  pause
  exit /b 1
)

where conda >nul 2>nul
if errorlevel 1 (
  echo [ERROR] conda not found. Open Anaconda Prompt and run Install-Offline.bat again.
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

echo [3/5] Offline pip: setuptools, wheel ...
python -m pip install --no-index --find-links "%WHEELS%" setuptools wheel
if errorlevel 1 goto :pip_fail

echo [4/5] Offline pip: openpyxl, icalendar, tzdata, pywin32 ...
python -m pip install --no-index --find-links "%WHEELS%" openpyxl icalendar tzdata pywin32
if errorlevel 1 goto :pip_fail

echo [5/5] Register this project (offline) ...
python -m pip install --no-build-isolation --no-index --find-links "%WHEELS%" -e ".[outlook]"
if errorlevel 1 (
  echo [WARN] editable install skipped; using PYTHONPATH mode.
)

echo conda> .env-mode
echo offline>> .env-mode

set "PYTHONPATH=%CD%"
python -m planning_tool.cli --help >nul 2>&1
if errorlevel 1 (
  echo [ERROR] planning_tool.cli still not runnable.
  pause
  exit /b 1
)

echo.
echo [OK] Offline install done. Double-click Run-Demo.bat next.
if /i not "%~1"=="--from-wrapper" pause
exit /b 0

:pip_fail
echo [ERROR] pip failed. See messages above. Log: %LOG%
pause
exit /b 1
