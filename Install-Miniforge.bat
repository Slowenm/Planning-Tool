@echo off
chcp 65001 >nul 2>&1
title Planning-Tool 安装（Miniforge）
cd /d "%~dp0"
echo.
echo 本工具仅通过 **Miniforge** 的 Python/conda 运行（环境名: planning-tool）
echo 若尚未安装 Miniforge: https://github.com/conda-forge/miniforge/releases
echo 推荐: 开始菜单打开 **Miniforge Prompt**，再双击本脚本；或直接双击（已装 Miniforge 时）
echo.
call "%~dp0windows\install-offline.bat" --from-wrapper
set RC=%ERRORLEVEL%
echo.
if %RC%==0 (
  echo ========================================
  echo  OK — 下一步: Planning-Tool-GUI.bat 或 Run-Demo.bat
  echo ========================================
) else (
  echo ========================================
  echo  失败 exit %RC% — 请在 Miniforge Prompt 中重试，或查看 install-last.log
  echo ========================================
)
echo.
pause
exit /b %RC%
