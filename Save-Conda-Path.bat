@echo off
title Save conda path for double-click runs
cd /d "%~dp0"
where conda >nul 2>nul
if errorlevel 1 (
  echo Open this from Anaconda Prompt, then run Save-Conda-Path.bat again.
  pause
  exit /b 1
)
for /f "delims=" %%G in ('conda info --base') do echo %%G> .conda-base
echo Saved conda base to .conda-base:
type .conda-base
echo You can now double-click Run-With-Outlook.bat
pause
