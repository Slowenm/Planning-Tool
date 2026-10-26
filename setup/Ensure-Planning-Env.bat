@echo off
chcp 65001 >nul 2>&1
title Check planning-tool conda env
cd /d "%~dp0\.."
set "TOOL_ROOT=%CD%"
call "%TOOL_ROOT%\windows\internal\_prepend_conda_path.bat"
call "%TOOL_ROOT%\windows\internal\_find_conda_base.bat"

echo Tool folder: %TOOL_ROOT%
echo CONDA_BASE=%CONDA_BASE%
echo.
if exist "%CONDA_BASE%\envs\planning-tool\python.exe" (
  echo [OK] planning-tool env exists.
  "%CONDA_BASE%\envs\planning-tool\python.exe" --version
  pause
  exit /b 0
)
echo [MISSING] planning-tool env — run Install-Miniforge.bat from Miniforge Prompt.
echo.
conda env list 2>nul
pause
exit /b 1
