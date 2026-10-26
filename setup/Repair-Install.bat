@echo off
title 修复安装
cd /d "%~dp0\.."
set "TOOL_ROOT=%CD%"
echo 重新离线安装（目录: %TOOL_ROOT%）
call "%TOOL_ROOT%\windows\install\install-offline.bat" --from-wrapper
pause
