@echo off
setlocal EnableExtensions
call "%~dp0..\internal\_ensure_tool_root.bat"
cd /d "%TOOL_ROOT%"

echo 演示排期（不读 Outlook，examples\tasks_template.csv）...
call "%~dp0plan-work.bat" --tasks examples\tasks_template.csv --calendar none
set RC=%ERRORLEVEL%
echo.
if %RC%==0 (
  echo OK: schedule.md and schedule.ics in %TOOL_ROOT%
) else (
  echo FAILED exit %RC%. Try diagnostics\Test-Cli.bat
)
pause
exit /b %RC%
