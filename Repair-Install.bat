@echo off
title Planning-Tool 修复安装（Miniforge）
cd /d "%~dp0"
echo 在当前目录重新离线安装（不删除 planning-tool 环境）
echo 目录: %CD%
echo.
call "%~dp0windows\install-offline.bat" --from-wrapper
pause
