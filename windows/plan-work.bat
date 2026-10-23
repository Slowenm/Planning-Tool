@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."

if not exist .venv\Scripts\activate.bat (
  echo 首次使用，正在安装依赖...
  call "%~dp0install.bat"
  if errorlevel 1 exit /b 1
)

call .venv\Scripts\activate.bat
plan-work %*
set ERR=%ERRORLEVEL%
if %ERR% neq 0 pause
exit /b %ERR%
