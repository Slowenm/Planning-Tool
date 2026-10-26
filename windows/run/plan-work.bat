@echo off
setlocal EnableExtensions
call "%~dp0_run-plan-work.bat" %*
set ERR=%ERRORLEVEL%
if %ERR% neq 0 pause
exit /b %ERR%
