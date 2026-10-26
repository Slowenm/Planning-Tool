@echo off
chcp 65001 >nul 2>&1
setlocal EnableExtensions
call "%~dp0..\internal\_ensure_tool_root.bat"
cd /d "%TOOL_ROOT%"

if "%~1"=="" (
  echo 用法: 把 tasks.xlsx 拖到 run\Run-With-Outlook.bat 或根目录 Run-With-Outlook.bat
  pause
  exit /b 1
)

echo Scheduling with Outlook: %~1
call "%~dp0plan-work.bat" --tasks "%~1" --calendar outlook --report schedule.md --ics schedule.ics
set RC=%ERRORLEVEL%
echo.
if %RC%==0 (
  echo Done. Open schedule.md, double-click schedule.ics to import Outlook.
) else (
  echo Failed. Run Install-Miniforge.bat if needed.
)
pause
exit /b %RC%
