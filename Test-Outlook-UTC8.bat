@echo off
rem Use when COM times are UTC but you schedule in East 8 (China)
cd /d "%~dp0"
set "PLANNING_OUTLOOK_NAIVE_TZ=utc"
call "%~dp0Test-Outlook.bat"
