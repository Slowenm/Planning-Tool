@echo off
chcp 65001 >nul 2>&1
title Planning-Tool 离线安装
cd /d "%~dp0\.."
set "TOOL_ROOT=%CD%"
call "%TOOL_ROOT%\windows\install\install-offline.bat" --from-wrapper
set RC=%ERRORLEVEL%
echo.
if %RC%==0 echo OK — Planning-Tool-GUI.bat / Run-Demo.bat
if not %RC%==0 echo FAILED exit %RC%
pause
exit /b %RC%
