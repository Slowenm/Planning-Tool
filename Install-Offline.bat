@echo off
chcp 65001 >nul 2>&1
title Planning-Tool Offline Install
cd /d "%~dp0"
call "%~dp0windows\install-offline.bat" --from-wrapper
set RC=%ERRORLEVEL%
echo.
if %RC%==0 (
  echo ========================================
  echo  OK - next: double-click Run-Demo.bat
  echo ========================================
) else (
  echo ========================================
  echo  FAILED exit code %RC%
  echo ========================================
)
echo.
pause
exit /b %RC%
