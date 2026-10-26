@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0\.."
set "TOOL_ROOT=%CD%"
call "%TOOL_ROOT%\windows\internal\_tool_env.bat"
call "%TOOL_ROOT%\windows\internal\_prepend_conda_path.bat"

echo ===== 安装检查 Miniforge =====
echo 目录: %TOOL_ROOT%
echo.

if exist "%TOOL_ROOT%\.miniforge-base" (
  echo [OK] .miniforge-base:
  type "%TOOL_ROOT%\.miniforge-base"
) else (
  echo [--] 无 .miniforge-base — 运行 setup\Save-Miniforge-Path.bat
)
echo.

if exist "%TOOL_ROOT%\.env-mode" (
  echo [OK] .env-mode:
  type "%TOOL_ROOT%\.env-mode"
) else (
  echo [--] 无 .env-mode — 运行 Install-Miniforge.bat
)
echo.

where conda >nul 2>nul
if not errorlevel 1 (
  conda env list | findstr /i planning-tool
  if exist "%TOOL_ROOT%\.env-mode" (
    findstr /i /b "miniforge conda" "%TOOL_ROOT%\.env-mode" >nul 2>&1
    if not errorlevel 1 (
      set "PLANNING_TOOL_ROOT=%TOOL_ROOT%"
      set "PYTHONPATH=%TOOL_ROOT%"
      conda run -n planning-tool --no-capture-output python -m planning_tool.cli --help >nul 2>&1
      if errorlevel 1 (echo [失败] cli) else (echo [OK] python -m planning_tool.cli)
    )
  )
) else (
  echo [--] PATH 无 conda — Save-Miniforge-Path.bat
)
pause
