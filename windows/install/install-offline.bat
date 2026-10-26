@echo off
setlocal EnableExtensions EnableDelayedExpansion
call "%~dp0..\internal\_ensure_tool_root.bat"
cd /d "%TOOL_ROOT%"
call "%~dp0..\internal\_prepend_conda_path.bat"

set "WHEELS=%TOOL_ROOT%\offline\wheels"
set "LOG=%TOOL_ROOT%\install-last.log"
echo === install-offline %DATE% %TIME% ===>> "%LOG%"

if not exist "%WHEELS%\*.whl" (
  echo [ERROR] Missing offline\wheels\*.whl — use the ~9MB zip.
  pause
  exit /b 1
)

where conda >nul 2>nul
if errorlevel 1 (
  echo [ERROR] 找不到 Miniforge / conda。
  echo 请安装 Miniforge: https://github.com/conda-forge/miniforge/releases
  echo 或在 Miniforge Prompt 中运行 Install-Miniforge.bat
  pause
  exit /b 1
)

conda env list | findstr /i /b "planning-tool " >nul 2>nul
if errorlevel 1 (
  echo [1/5] Creating Miniforge env planning-tool ...
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
call "%~dp0..\internal\_conda_activate_planning_tool.bat"
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

echo [5/5] Register this project (offline) ...
call "%~dp0..\internal\_tool_env.bat"
python -m pip install --no-build-isolation --no-index --find-links "%WHEELS%" ".[outlook]"
set "PIP_PROJ=%ERRORLEVEL%"

echo miniforge> "%TOOL_ROOT%\.env-mode"
echo offline>> "%TOOL_ROOT%\.env-mode"
echo system> "%TOOL_ROOT%\.outlook-tz"

echo Verify import ...
python -c "import planning_tool.cli; print('import OK')"
if errorlevel 1 (
  echo [ERROR] planning_tool not importable from %TOOL_ROOT%.
  python -c "import planning_tool.cli"
  pause
  exit /b 1
)

if not "%PIP_PROJ%"=="0" (
  echo [WARN] pip install returned %PIP_PROJ% but import works; continuing.
)

call "%~dp0..\internal\_find_conda_base.bat"
if defined CONDA_BASE (
  echo !CONDA_BASE!> "%TOOL_ROOT%\.miniforge-base"
  echo !CONDA_BASE!> "%TOOL_ROOT%\.conda-base"
)

echo.
echo [OK] Offline install done. Next: Planning-Tool-GUI.bat or Run-Demo.bat
if /i not "%~1"=="--from-wrapper" pause
exit /b 0

:pip_fail
echo [ERROR] pip failed. Log: %LOG%
pause
exit /b 1
