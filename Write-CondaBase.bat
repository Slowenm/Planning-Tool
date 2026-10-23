@echo off
title Write .conda-base (same as Save-Conda-Path)
cd /d "%~dp0"
where conda >nul 2>nul
if errorlevel 1 (
  echo Run from Anaconda Prompt.
  pause
  exit /b 1
)
for /f "delims=" %%G in ('conda info --base') do echo %%G> .conda-base
echo Saved .conda-base:
type .conda-base
pause
