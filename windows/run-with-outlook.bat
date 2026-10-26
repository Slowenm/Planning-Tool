@echo off
chcp 65001 >nul 2>&1
setlocal EnableExtensions
cd /d "%~dp0\.."

if "%~1"=="" (
  echo Usage: drag your tasks.xlsx onto Run-With-Outlook.bat
  echo   or: run-with-outlook.bat "D:\path\tasks.xlsx"
  pause
  exit /b 1
)

echo Scheduling with Outlook calendar: %~1
call "%~dp0plan-work.bat" --tasks "%~1" --calendar outlook --report schedule.md --ics schedule.ics
set RC=%ERRORLEVEL%
echo.
if %RC%==0 (
  echo Done. Open schedule.md to review, then double-click schedule.ics to import Outlook.
) else (
  echo Failed. Run Install-Miniforge.bat from Miniforge Prompt if needed.
)
pause
exit /b %RC%
