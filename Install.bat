@echo off
chcp 65001 >nul 2>&1
title Planning-Tool 安装
cd /d "%~dp0"
echo.
echo 本工具通过 **Miniforge** 运行，不再使用独立 Python venv / Anaconda。
echo.
echo 1. 若未安装 Miniforge，请先安装:
echo    https://github.com/conda-forge/miniforge/releases
echo.
echo 2. 然后双击 **Install-Miniforge.bat**（或 Install-Offline.bat，相同流程）
echo.
pause
exit /b 0
