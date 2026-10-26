@echo off
title 保存 Miniforge 路径（便于双击 bat）
cd /d "%~dp0"
call "%~dp0windows\_save_miniforge_base.bat"
set RC=%ERRORLEVEL%
if %RC% neq 0 pause
exit /b %RC%
