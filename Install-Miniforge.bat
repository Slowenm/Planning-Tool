@echo off
chcp 65001 >nul 2>&1
title Planning-Tool 安装（Miniforge）
cd /d "%~dp0"
set "TOOL_ROOT=%CD%"
echo.
echo 本工具通过 Miniforge 运行（环境 planning-tool）
echo 安装包: https://github.com/conda-forge/miniforge/releases
echo.
call "%TOOL_ROOT%\windows\install\install-offline.bat" --from-wrapper
set RC=%ERRORLEVEL%
echo.
if %RC%==0 (
  echo OK — 下一步: Planning-Tool-GUI.bat 或 Run-Demo.bat
) else (
  echo 失败 exit %RC% — Miniforge Prompt 中重试，或查看 install-last.log
)
echo.
pause
exit /b %RC%
