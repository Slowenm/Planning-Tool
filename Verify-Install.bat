@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ===== Planning-Tool 安装检查 =====
echo 目录: %CD%
echo.

if exist ".env-mode" (
  echo [OK] .env-mode 存在:
  type .env-mode
) else (
  echo [--] 未找到 .env-mode，可能尚未安装成功
)
echo.

where conda >nul 2>nul
if errorlevel 1 (
  echo [--] 当前窗口未检测到 conda（若用 venv 可忽略）
) else (
  echo [..] conda 环境 planning-tool:
  conda env list | findstr /i planning-tool
  if exist ".env-mode" (
    set /p MODE=<.env-mode
    if /i "!MODE!"=="conda" (
      echo [..] 尝试运行 plan-work --help ...
      conda run -n planning-tool --no-capture-output plan-work --help >nul 2>&1
      if errorlevel 1 (echo [失败] planning-tool 里找不到 plan-work) else (echo [OK] plan-work 可用)
    )
  )
)

if exist ".venv\Scripts\plan-work.exe" (
  echo [OK] .venv 中已安装 plan-work
)

echo.
echo 若显示 [OK]，请双击 Run-Demo.bat 试跑。
echo.
pause
