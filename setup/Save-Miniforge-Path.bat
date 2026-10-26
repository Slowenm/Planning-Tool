@echo off
title 保存 Miniforge 路径
cd /d "%~dp0\.."
set "TOOL_ROOT=%CD%"
call "%TOOL_ROOT%\windows\internal\_save_miniforge_base.bat"
set RC=%ERRORLEVEL%
if %RC% neq 0 pause
exit /b %RC%
