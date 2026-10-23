@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."

if "%~1"=="" (
  echo 用法: 将任务表拖到本脚本上，或：
  echo   run-with-outlook.bat D:\path\tasks.xlsx
  pause
  exit /b 1
)

echo 读取 Outlook 日历并排期: %~1
call "%~dp0plan-work.bat" --tasks "%~1" --calendar outlook --report schedule.md --ics schedule.ics
echo.
echo 完成。请双击 schedule.ics 导入 Outlook。
pause
