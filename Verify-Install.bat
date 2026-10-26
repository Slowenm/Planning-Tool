@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
call "%~dp0windows\_tool_env.bat"
call "%~dp0windows\_prepend_conda_path.bat"

echo ===== Planning-Tool 安装检查（Miniforge）=====
echo 目录: %CD%
echo.

if exist ".miniforge-base" (
  echo [OK] .miniforge-base:
  type .miniforge-base
) else if exist ".conda-base" (
  echo [OK] .conda-base:
  type .conda-base
) else (
  echo [--] 未找到 .miniforge-base — 双击 Save-Miniforge-Path.bat 或重装 Install-Miniforge.bat
)
echo.

if exist ".env-mode" (
  echo [OK] .env-mode:
  type .env-mode
) else (
  echo [--] 未找到 .env-mode — 请运行 Install-Miniforge.bat
)
echo.

where conda >nul 2>nul
if not errorlevel 1 (
  echo [..] planning-tool 环境:
  conda env list | findstr /i planning-tool
  if exist ".env-mode" (
    findstr /i /b "miniforge conda" .env-mode >nul 2>&1
    if not errorlevel 1 (
      set "PLANNING_TOOL_ROOT=%CD%"
      set "PYTHONPATH=%CD%"
      conda run -n planning-tool --no-capture-output python -m planning_tool.cli --help >nul 2>&1
      if errorlevel 1 (
        echo [失败] 无法运行 cli — 请 Repair-Install.bat
      ) else (
        echo [OK] python -m planning_tool.cli 可用
      )
    )
  )
) else (
  echo [--] 此窗口 PATH 中无 conda — 若已装 Miniforge，运行 Save-Miniforge-Path.bat 后重试
)

if exist "install-last.log" (
  echo.
  echo install-last.log 最后 5 行:
  powershell -NoProfile -Command "Get-Content -Path 'install-last.log' -Tail 5 -ErrorAction SilentlyContinue"
)

echo.
echo 正常则双击 Planning-Tool-GUI.bat 或 Run-Demo.bat
pause
