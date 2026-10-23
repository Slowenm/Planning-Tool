@echo off
title Planning-Tool Offline Install
cd /d "%~dp0"
call "%~dp0windows\install-offline.bat" --from-wrapper
echo.
pause
