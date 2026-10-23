@echo off
if errorlevel 1 (
  echo.
  echo [失败] 请向上滚动查看报错；也可打开项目根目录的 install-last.log（若存在）
  pause
  exit /b 1
)
exit /b 0
