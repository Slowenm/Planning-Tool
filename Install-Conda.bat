@echo off
cd /d "%~dp0"
title Planning-Tool Install (Conda)
call "%~dp0windows\install-conda.bat" --from-wrapper
set RC=%ERRORLEVEL%
echo.
if %RC%==0 (
  echo ========================================
  echo  安装流程已结束（成功）。请双击 Run-Demo.bat
  echo ========================================
) else (
  echo ========================================
  echo  安装可能失败，退出代码: %RC%
  echo  请查看: %~dp0install-last.log
  echo ========================================
)
echo.
pause
exit /b %RC%
