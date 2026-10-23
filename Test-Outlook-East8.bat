@echo off
rem Use when COM times are already wall-clock in UTC+8
cd /d "%~dp0"
set "PLANNING_OUTLOOK_NAIVE_TZ=asia_shanghai"
call "%~dp0Test-Outlook.bat"
