@echo off
setlocal EnableExtensions
cd /d "%~dp0"
call "%~dp0windows\_tool_env.bat"

echo ===== Planning-Tool 安装检查 =====
echo 目录: %CD%
echo.

if exist ".env-mode" (
  echo [OK] .env-mode 存在，内容为:
  type .env-mode
) else (
  echo [--] 未找到 .env-mode — 可能尚未安装成功，请重新运行 Install-Conda.bat
)
echo.

where conda >nul 2>nul
if not errorlevel 1 (
  echo [..] conda 中的 planning-tool 环境:
  conda env list | findstr /i planning-tool
  if exist ".env-mode" (
    findstr /i "^conda" .env-mode >nul 2>&1
    if not errorlevel 1 (
      set "PLANNING_TOOL_ROOT=%CD%"
      set "PYTHONPATH=%CD%"
      conda run -n planning-tool --no-capture-output python -m planning_tool.cli --help >nul 2>&1
      if errorlevel 1 (
        echo [失败] 无法运行 python -m planning_tool.cli — 请双击 Repair-Install.bat
      ) else (
        echo [OK] python -m planning_tool.cli 可用（bat 脚本会自动用这个入口）
      )
    )
  )
) else (
  echo [--] 此窗口未检测到 conda（若只用 .venv 可忽略上一段）
)

if exist ".venv\Scripts\plan-work.exe" (
  echo [OK] .venv 中已安装 plan-work
)

if exist "install-last.log" (
  echo.
  echo 最近一次安装日志最后 5 行:
  powershell -NoProfile -Command "Get-Content -Path 'install-last.log' -Tail 5 -ErrorAction SilentlyContinue"
)

echo.
echo 若上面有 [OK]，请双击 Run-Demo.bat 试跑。
echo.
pause
