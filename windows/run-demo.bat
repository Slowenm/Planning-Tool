@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."

echo 演示排期（不读 Outlook，使用 examples\tasks_template.csv）...
call "%~dp0plan-work.bat" --tasks examples\tasks_template.csv --calendar none
set RC=%ERRORLEVEL%
echo.
if %RC%==0 (
  echo OK: schedule.md and schedule.ics in project folder.
) else (
  echo FAILED exit code %RC%. Try Test-Cli.bat or python -m planning_tool.cli ...
)
pause
exit /b %RC%
