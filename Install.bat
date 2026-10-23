@echo off
cd /d "%~dp0"
title Planning-Tool Install (venv)
call "%~dp0windows\install.bat"
set RC=%ERRORLEVEL%
echo.
if %RC%==0 (
  echo 安装成功。请双击 Run-Demo.bat
) else (
  echo 安装可能失败，退出代码: %RC%
)
echo.
pause
exit /b %RC%
