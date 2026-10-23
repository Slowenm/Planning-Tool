@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."

echo 演示排期（不读 Outlook，使用 examples\tasks_template.csv）...
call "%~dp0plan-work.bat" --tasks examples\tasks_template.csv --calendar none
echo.
echo 已生成 schedule.md 与 schedule.ics（在本文件夹根目录）
pause
